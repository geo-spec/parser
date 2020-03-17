#!/usr/bin/env python3

# websockets==6.0

import asyncio
from datetime import datetime, timedelta
from dataclasses import dataclass
import json
import logging
import os
from random import random
import sys
import time
from traceback import format_exc
from typing import Optional, Tuple, Union, Iterable
from uuid import uuid4

import pandas as pd

from pyppeteer import launch, connect
from pyppeteer.page import Page
from pyppeteer.element_handle import ElementHandle
from pyppeteer.errors import NetworkError, TimeoutError, PyppeteerError
from pyppeteer_stealth import stealth

import redis

from websockets.exceptions import ConnectionClosed


LOGIN_URL = ('https://passport.yandex.ru/auth/list?origin=direct&'
             'retpath=https://direct.yandex.ru/')

DIRECT_WORDSTAT_URL = ('https://direct.yandex.ru/registered/main.pl?checkboxes=1&'
                       'cmd=wordstat&from_forecast=1&tm=&geo=0')

WORDSTAT_URL = ('https://direct.yandex.ru/registered/main.pl?checkboxes=1&'
                       'cmd=wordstat&from_forecast=1&tm=&geo=0')

user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) '
              'AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9')

ACC_LOCK_TTL = 3600
ACCS_KEY = 'accounts'
ACCS_BANNED_KEY = 'accounts_banned'
CAPTCHA_KEY = 'captcha'
ACCS_DB = 1

WINDOW_SIZE = (1366, 768)
viewport = {'width': WINDOW_SIZE[0], 'height': WINDOW_SIZE[1]}

COOKIES_DIR = os.path.join(os.path.dirname(__file__), 'cookies')
COOKIES_PATH_TMPLT = os.path.join(COOKIES_DIR, '{}.json')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PARSE_WORDSTAT_TABLE_F = '''
    rows => rows.map(row => {
        const j_row = $(row);
        const query = j_row.find('a.b-phrase-link__link').text();
        const count = j_row.find('td.b-word-statistics__td-number').text().replace(/\xa0/gi, '');
        return [query, count];
    })
'''


@dataclass
class ProxyConf:
    host: str
    username: str
    password: str

    @classmethod
    def from_dict(cls, proxy_dict: dict) -> 'ProxyConf':
        return ProxyConf(
            host=proxy_dict['host'],
            username=proxy_dict['username'],
            password=proxy_dict['password']
        )

    @classmethod
    def from_json(cls, proxy_json: str) -> 'ProxyConf':
        return cls.from_dict(json.loads(proxy_json))


@dataclass
class Account:
    login: str
    password: str
    phone: str
    cookies: Optional[dict] = None
    proxy: Union[ProxyConf, str, None] = None

    def to_dict(self) -> dict:
        acc_info = {
            'login': self.login,
            'password': self.password,
            'phone': self.phone,
            'cookies': self.cookies,
        }
        if isinstance(self.proxy, ProxyConf):
            acc_info['proxy'] = self.proxy.host
        else:
            acc_info['proxy'] = self.proxy
        return acc_info

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    @classmethod
    def from_dict(cls, acc_dict: dict) -> 'Account':
        return cls(
            login=acc_dict['login'],
            password=acc_dict['password'],
            phone=acc_dict['phone'],
            proxy=acc_dict.get('proxy'),
            cookies=acc_dict.get('cookies')
        )

    @classmethod
    def from_json(cls, acc_json: str) -> 'Account':
        return cls.from_dict(json.loads(acc_json))


@dataclass
class RedisConf:
    host: str = '127.0.0.1'
    port: int = 6379
    db: int = ACCS_DB
    password: Optional[str] = None


DEFAULT_REDIS_CONF = RedisConf(
    host='demo.revoluterra.ru',
    db=ACCS_DB,
    password='Eingae2muo'
)


async def parse_wordstat_page(page: Page) -> Tuple[list, list]:
    phrases_div, assoc_div = await asyncio.gather(
        page.waitForSelector('div.b-word-statistics__including-phrases', {'visible': True}),
        page.waitForSelector('div.b-word-statistics__phrases-associations', {'visible': True})
    )
    phrases, assocs = await asyncio.gather(
        phrases_div.JJeval('tr + tr', PARSE_WORDSTAT_TABLE_F),
        assoc_div.JJeval('tr + tr', PARSE_WORDSTAT_TABLE_F)
    )
    return phrases, assocs


async def clear_input_text(page: Page, input_node: ElementHandle):
    await page.keyboard.down('ControlLeft')
    await input_node.press('A')
    await page.keyboard.up('ControlLeft')
    await input_node.press('Backspace')


class CaptchaError(Exception):
    pass


class YWordstatClient:
    def __init__(self, redis_conf: Optional[RedisConf] = None,
                 headless: bool = True, block: bool = True):
        self._yacc = None
        self._lock_ts = None
        self._page = None
        self._n_rqs = 0
        self.block = block
        self.headless = False
        redis_conf = redis_conf or DEFAULT_REDIS_CONF
        self.redis = redis.StrictRedis(
            host=redis_conf.host,
            port=redis_conf.port,
            db=redis_conf.db,
            password=redis_conf.password,
            decode_responses=True
        )
        self._id = str(uuid4())

    def acc_lock_key(self) -> Optional[str]:
        if self._yacc is None:
            return None
        return 'lock_' + self._yacc.login

    def acquire_account_impl(self, change: bool = False) -> bool:
        if self._yacc is not None:
            if change:
                self.release_account()
            else:
                return self.check_account()
        accounts = self.redis.hgetall(ACCS_KEY)
        if accounts is None:
            return False
        for login, acc_info in accounts.items():
            logger.info(acc_info)
            key = 'lock_' + login
            if not self.redis.setnx(key, self._id):
                continue
            if self.redis.sismember(ACCS_BANNED_KEY, login):
                self.redis.delete(key)
                continue
            self._lock_ts = datetime.now()
            self.redis.expire(key, ACC_LOCK_TTL)
            yacc = Account.from_json(acc_info)
            if yacc.proxy is not None:
                try:
                    proxy_json = self.redis.hget('proxies', yacc.proxy)
                    yacc.proxy = ProxyConf.from_json(proxy_json)
                except Exception:
                    logger.error('Unabe to get proxy "{}"'.format(yacc.proxy))
                    self.redis.delete(key)
                    continue
            else:
                logger.error('Account "{}" has no proxy'.format(login))
                self.redis.delete(key)
                continue
            self._yacc = yacc
            return True
        logger.info('Accounts not found')
        return False

    def mark_captcha(self):
        if self._yacc is None:
            return
        # key = self.acc_lock_key()

        # def _mark_captcha(pipeline) -> bool:
        #     if pipeline.get(key) != self._id:
        #         return False
        #     pipeline.sadd(CAPTCHA_KEY, self._yacc.login)
        #     return True

        # if self.redis.transaction(_mark_captcha, key, CAPTCHA_KEY,
        #                           value_from_callable=True):
        #     self.release_account()
        self.redis.hincrby(CAPTCHA_KEY, self._yacc.login)

    def mark_banned(self):
        if self._yacc is None:
            return
        self.redis.sadd(ACCS_BANNED_KEY, self._yacc.login)

    def release_account(self):
        if self._yacc is None:
            return
        key = self.acc_lock_key()

        def _del_key(pipeline):
            if pipeline.get(key) == self._id:
                pipeline.delete(key)

        self.redis.transaction(_del_key, key)

    def save_cookies(self):
        assert self._yacc.cookies is not None
        key = self.acc_lock_key()
        acc_info = self._yacc.to_dict()
        acc_json = json.dumps(acc_info)

        def _update_cookies(pipeline):
            if pipeline.get(key) != self._id:
                raise RuntimeError('Accout owner changed!')
            pipeline.hset(ACCS_KEY, self._yacc.login, acc_json)

        self.redis.transaction(_update_cookies, key, ACCS_KEY,
                               value_from_callable=True)

    def check_account(self) -> bool:
        logger.info('checking account...')
        if self._yacc is None:
            logger.info('self._yacc is None')
            return False
        key = self.acc_lock_key()

        logger.info('Key {}'.format(key))

        def _update_ttl(pipeline):
            if pipeline.get(key) != self._id:
                logger.info('Id changed')
                return False
            logger.info('Id not changed')
            pipeline.expire(key, ACC_LOCK_TTL)
            return True

        return self.redis.transaction(_update_ttl, key,
                                      value_from_callable=True)

    def list_accs(self, free: bool = True, acquired: bool = True) -> list:
        accounts = self.redis.hgetall(ACCS_KEY)
        if accounts is None or not (free or acquired):
            return []
        result = []
        for name, info in accounts.items():
            info = json.loads(info)
            exists = self.redis.exists(name)
            if (exists and acquired) or (not exists and free):
                result.append(info)
        return result

    def add_acc(self, acc: Account) -> bool:
        return self.redis.hsetnx(ACCS_KEY, acc.login, acc.to_json())

    async def _login(self):
        page = self._page
        assert page
        assert self._yacc

        await page.goto(LOGIN_URL)

        login_field, login_btn = await asyncio.gather(
            page.waitForSelector('#passp-field-login', {'visible': True}),
            page.waitForSelector('div.passp-sign-in-button > button.passp-form-button', {'visible': True})
        )
        # await login_btn.screenshot({'path': 'btn.png'})
        await asyncio.sleep(1)
        await login_field.type(self._yacc.login)
        await asyncio.sleep(1)
        await asyncio.gather(
            login_btn.click(),
            page.waitForNavigation()
        )
        # await page.screenshot({'path': 'login.png'})

        pwd_field, login_btn = await asyncio.gather(
            page.waitForSelector('#passp-field-passwd', {'visible': True}),
            page.waitForSelector('div.passp-sign-in-button > button.passp-form-button', {'visible': True})
        )
        await asyncio.sleep(1)
        await pwd_field.type(self._yacc.password)
        await asyncio.sleep(1)
        await asyncio.gather(
            login_btn.click(),
            page.waitForNavigation()
        )
        await asyncio.sleep(1)
        try:
            if await page.evaluate('() => $(\'span.button2__text:contains("Да, это мой номер")\').length !== 0'):
                btn = await page.waitForSelector('button.button2_type_submit')
                await asyncio.gather(
                    btn.click(),
                    page.waitForNavigation()
                )
            else:
                phone_field = await page.querySelector('#passp-field-phone')
                if phone_field:
                    btn = await page.querySelector('button.button2_type_submit')
                    await phone_field.type(self._yacc.phone)
                    asyncio.sleep(1)
                    await asyncio.gather(
                        btn.click(),
                        page.waitForNavigation()
                    )
        except NetworkError:
            # ???
            pass
        # await page.screenshot({'path': 'pwd.png'})
        await page.waitForSelector('img[alt="Директ"]', {'visible': True})
        # await page.screenshot({'path': 'logged.png'})
        self._yacc.cookies = await page.cookies()
        self.save_cookies()
        logger.info('Login successful')

    async def acquire_account(self):
        if self.block:
            while True:
                if self.acquire_account_impl():
                    break
                await asyncio.sleep(10)
        else:
            if not self.acquire_account_impl():
                raise RuntimeError('No account available')

    async def get_page(self, new: bool = False) -> Page:
        if self._page is not None:
            if new or self._page.isClosed():
                try:
                    self.close()
                except Exception:
                    logger.error(format_exc())
                self._page = None
            else:
                await self.acquire_account()
                return self._page

        await self.acquire_account()

        args = ['--no-sandbox']
        proxy = self._yacc.proxy
        if proxy is not None:
            logger.info('User proxy {} {} {}'.format(proxy.host, proxy.username, proxy.password))
            args.append('--proxy-server={}'.format(proxy.host))
        browser = await launch({'headless': self.headless, 'args': args})
        page = (await browser.pages())[0]
        await stealth(page)
        await page.setUserAgent(user_agent)
        await page.setViewport(viewport)
        if proxy is not None:
            await page.authenticate({'username': proxy.username,
                                     'password': proxy.password})
        self._page = page
        if self._yacc.cookies is not None:
            await page.setCookie(*self._yacc.cookies)
        else:
            await self._login()
        try:
            await page.goto('https://wordstat.yandex.ru/?direct=1')
        except Exception:
            logger.error(format_exc())
            logger.error('Connection error! (Check proxy) -  {}'.format(proxy))
            raise RuntimeError('Connection error! (Check proxy) - {}'.format(proxy))

        # await page.screenshot({'path': 'logs/wordstat.png'})
        await asyncio.sleep(2)
        await self.reconnect()
        return self._page

    async def query(self, queries: Union[str, Iterable[str]]) -> dict:
        ts = datetime.now()
        f_path = 'results_tmp_{}.json'.format(ts)
        if isinstance(queries, str):
            queries = [queries]
        result = {}
        try:
            for i, q in enumerate(queries, start=1):
                q = q.strip()
                if not q:
                    continue
                for j in range(3):
                    try:
                        phrases, asscocs = await self._query(q)
                        break
                    except (asyncio.IncompleteReadError,
                            asyncio.InvalidStateError,
                            asyncio.TimeoutError,
                            ConnectionClosed,
                            PyppeteerError):
                        logger.error(format_exc())
                        if j == 2:
                            raise
                        try:
                            await self.reconnect()
                        except Exception:
                            await self.get_page(new=True)
                result[q] = {
                    'phrases': phrases,
                    'asscocs': asscocs,
                }
                # with open(f_path, 'w') as f:
                #     json.dump(result, f, indent=4, ensure_ascii=False)
                # with open(f_path + '_', 'w') as f:
                #     json.dump(result, f, indent=4, ensure_ascii=False)
                elapsed = (datetime.now() -  ts).total_seconds()
                logger.info('#{} Elapsed {} s. Speed {} q/min'.format(i, elapsed, i / elapsed * 60))
        except Exception as e:
            logger.error('Exception: {}'.format(e))
            logger.error(format_exc())
            await self._try_save_error_page()
            raise
        return result

    async def _try_save_error_page(self):
        if self._page is None:
            return
        try:
            ts = datetime.now()
            await self._page.screenshot({'path': 'error_{}.png'.format(ts)})
            html = await self._page.evaluate("() => $('html').html()")
            with open('error_{}.html'.format(ts), 'w') as f:
                f.write(html)
        except Exception as e:
            logger.error(e)

    async def _query(self, query: str) -> Tuple[list, list]:
        logger.info('Processing query "{}"'.format(query))
        page = await self.get_page()
        query_field, submit_btn = await asyncio.gather(
            page.waitForSelector('input[name="text"].b-form-input__input'),
            page.waitForSelector('input.b-form-button__input')
        )
        await clear_input_text(page, query_field)
        # await asyncio.sleep(1)
        await query_field.type(query)
        # await asyncio.sleep(1)
        try:
            await asyncio.gather(
                submit_btn.click(),
                page.waitForResponse('https://wordstat.yandex.ru/stat/words')
            )
        except TimeoutError:
            logger.info('Timeout waiting for https://wordstat.yandex.ru/stat/words')

        pages_data = []
        i = 1

        while True:
            logger.info('Processing page {}'.format(i))
            try:
                pages_data.append(await parse_wordstat_page(page))
            except TimeoutError:
                logger.error(format_exc())
                if await page.evaluate('() => ($(\'.b-history__query:contains("Неверно задан запрос")\').length !== 0)'):
                    logger.info('Page: Неверно задан запрос')
                    break
                for _ in range(3):
                    if await page.evaluate('() => $(".captcha").length !== 0'):
                        self.mark_captcha()
                        raise CaptchaError()
                    if await page.evaluate('() => $(\'span.b-form-button__simple:contains("Try again")\').length === 0'):
                        break
                    btn = await page.querySelector('span.b-form-button_type_simple[role="button"]')
                    await asyncio.gather(
                        btn.click(),
                        page.waitForNavigation()
                    )
                    asyncio.sleep(1)
            self._n_rqs += 1
            if i == 41:
                break
            i += 1
            await page.waitForSelector('div.b-pager', {'visible': True})
            last_page = False
            for _ in range(2):
                next_btn = await page.querySelector('a.b-pager__next')
                if not next_btn:
                    if await page.querySelector('span.b-pager__next'):
                        last_page = True
                    else:
                        await asyncio.sleep(0.5)
                        continue
                await page.mouse.move(random(), random())
                break
            if last_page:
                break
            try:
                await asyncio.gather(
                    next_btn.click(),
                    page.waitForResponse('https://wordstat.yandex.ru/stat/words')
                )
            except TimeoutError:
                logger.info('Timeout waiting for https://wordstat.yandex.ru/stat/words')
            await asyncio.sleep(0.1)
        phrases = dict(d for page in pages_data for d in page[0])
        asscocs = dict(d for page in pages_data for d in page[1])
        return phrases, asscocs

    async def reconnect(self):
        if self._page is None:
            return
        page = self._page
        url = page.target.url
        ws_endpoint = page.browser.wsEndpoint
        try:
            await page.browser.disconnect()
            await asyncio.sleep(2)
        except Exception:
            logger.error(format_exc())
        browser = await connect({'browserWSEndpoint': ws_endpoint})
        for page in (await browser.pages()):
            if page.target.url == url:
                self._page = page
                return

    async def close(self):
        if self._yacc is not None:
            self.release_account()
            self._yacc = None
        if self._page is not None:
            try:
                await self._page.browser.close()
            except Exception:
                logger.error(format_exc())
            self._page = None

    def __del__(self):
        if self._yacc is not None:
            self.release_account()
            self._yacc = None

# $('.captcha').length !== 0

async def _test1_impl(conn: 'sqlite3.Connection', run_id: str) -> None:
    client = YWordstatClient(DEFAULT_REDIS_CONF, headless=True)
    while True:
        with conn:
            rows = conn.execute('''
                SELECT query FROM queries
                WHERE results IS NULL
                LIMIT 20'''
            )
            queries = [row[0] for row in rows]
        if not queries:
            logger.info('All queries processed!')
            break
        try:
            results = await client.query(queries)
        except CaptchaError:
            with conn:
                conn.execute('''
                    UPDATE acc_stats
                    SET account = ?,
                        updated_at = ?,
                        captcha = 1
                    WHERE id = ?''',
                    (client._yacc.login, time.time(), run_id)
                )
            raise
        with conn:
            for query, res in results.items():
                conn.execute('''
                    UPDATE queries
                    SET results = ?
                    WHERE query = ?
                ''', (json.dumps(res), query))
            conn.execute('''
                UPDATE acc_stats
                SET n_processed = n_processed + ?,
                    account = ?,
                    updated_at = ?
                WHERE id = ?''',
                (len(results), client._yacc.login, time.time(), run_id)
            )


def _test1():
    import sqlite3
    conn = sqlite3.connect('test1.db')
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS queries (
                query TEXT PRIMARY KEY NOT NULL,
                results TEXT
            );'''
        )
        conn.execute('''
            CREATE TABLE IF NOT EXISTS acc_stats (
                id TEXT PRIMARY KEY NOT NULL,
                account TEXT,
                n_processed INTEGER NOT NULL DEFAULT 0,
                started_at REAL NOT NULL,
                updated_at REAL NOT NULL,
                captcha INTEGER NOT NULL DEFAULT 0
            );'''
        )
    # df = pd.read_excel('товары для дома.xlsx', sheet_name='Загруженные ключевые слова')
    # with conn:
    #     conn.executemany('''
    #         INSERT OR IGNORE INTO queries (query)
    #         VALUES (?)
    #     ''', df.values)
    # del df
    with conn:
        run_id = str(uuid4())
        ts = time.time()
        conn.execute('''
            INSERT INTO acc_stats (id, started_at, updated_at)
            VALUES (?, ?, ?);''',
            (run_id, ts, ts)
        )
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_test1_impl(conn, run_id))
    conn.close()


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        exit(-1)
    first_arg = sys.argv[1]
    if first_arg == 'test1':
        _test1()
    # r_client = redis.StrictRedis(
    #     host=DEFAULT_REDIS_CONF.host,
    #     db=DEFAULT_REDIS_CONF.db,
    #     password=DEFAULT_REDIS_CONF.password)
    # y_accs = [
    #     Account('korshunovaklara10@yandex.ru', '35evFD69l92j', '+79231180497',
    #             proxy=ProxyConf('193.233.149.187:42440', 'stiHSYrX0C', 'storm.di')),
    #     Account('l.vovpahom78@yandex.ru', 'hG6089o16v2g', '+79261846019',
    #             proxy=ProxyConf('193.233.149.187:42440', 'stiHSYrX0C', 'storm.di')),
    # ]
    # for acc in y_accs:
    #     acc_info = acc.to_dict()
    #     acc_json = json.dumps(acc_info)
    #     r_client.hset(ACCS_KEY, acc.login, acc_json)


    # assert len(sys.argv) > 1
    # if len(sys.argv) == 3 and sys.argv[1] == '-f':
    #     df = pd.read_csv(sys.argv[2])
    #     # df.to_csv('input_{}.csv'.format(datetime.now()), index=False)
    #     queries = df['query']
    # else:
    #     queries = sys.argv[1:]
    # logger.info('Need to get {} queries'.format(len(queries)))
    # loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    # batches = [queries[i:i+50] for i in range(0, len(queries), 50)]
    # results = {}
    # f_path = 'results_tmp_{}.json'.format(datetime.now())
    # for batch in batches:
    #     while True:
    #         try:
    #             result = loop.run_until_complete(client.query(batch))
    #             results.update(result)
    #             with open(f_path, 'w') as f:
    #                 json.dump(results, f, indent=4, ensure_ascii=False)
    #             with open(f_path + '_', 'w') as f:
    #                 json.dump(results, f, indent=4, ensure_ascii=False)
    #             break
    #         except Exception:
    #             logger.error(format_exc())
    #             try:
    #                 loop.run_until_complete(client.close())
    #             except Exception:
    #                 pass
    #             client._page = None
    # with open('results_{}.json'.format(datetime.now()), 'w') as f:
    #     json.dump(results, f, indent=4, ensure_ascii=False)
    # loop.run_until_complete(client.close())
