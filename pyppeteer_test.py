import asyncio
from pyppeteer import launch
import sys

from pyppeteer import launch, connect
from pyppeteer.page import Page
from pyppeteer.element_handle import ElementHandle
from pyppeteer.errors import NetworkError, TimeoutError, PyppeteerError
from pyppeteer_stealth import stealth
args = ['--no-sandbox']
user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36')
WINDOW_SIZE = (1366, 768)
viewport = {'width': WINDOW_SIZE[0], 'height': WINDOW_SIZE[1]}

LOGIN_URL = ('https://passport.yandex.ru/auth/list?origin=direct&'
             'retpath=https://direct.yandex.ru/')



from datetime import datetime, timedelta
# from dataclasses import dataclass
import json
import logging
import os
from random import random, randrange
import sys
import time
from traceback import format_exc
from typing import Optional, Tuple, Union, Iterable
from uuid import uuid4

# import pandas as pd

from pyppeteer import launch, connect
from pyppeteer.page import Page
from pyppeteer.element_handle import ElementHandle
from pyppeteer.errors import NetworkError, TimeoutError, PyppeteerError
from pyppeteer_stealth import stealth
PG_CONN_STR = 'user=postgres password=eipohCa4Ie host=localhost port=5433'
# import redis
import psycopg2

from websockets.exceptions import ConnectionClosed
cookie = [{'name': 'i', 'value': 'VtcwfRkC4FOkWCcB5otW46enEMQ53dtrRLKjOX7Rv2b6oJv3mk3lW6bAAEzaU9ZHy8iqgn573oyubIZDOM9j+So6lhs=', 'domain': '.yandex.ru', 'path': '/', 'expires': 1899458407, 'size': 93, 'httpOnly': True, 'secure': True, 'session': False}, {'name': 'L', 'value': 'XF1RRgRSTlx7SHRgVmJHZmcDWlZacEpbNQocFV5HJw==.1584098406.14169.320019.29eb3133d01ef238dc162cd2cb691d3d', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.527204, 'size': 102, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'ys', 'value': 'udn.cDpnZW90aXBz', 'domain': '.yandex.ru', 'path': '/', 'expires': -1, 'size': 18, 'httpOnly': False, 'secure': True, 'session': True}, {'name': 'sessionid2', 'value': '3:1584098406.5.0.1584098406510:hHc51A:48.1|196471750.0.2|213903.769795.gjqxJLCYU5pimafWMbUFV9R4Khs', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.527146, 'size': 108, 'httpOnly': True, 'secure': True, 'session': False}, {'name': 'ymex', 'value': '1899458401.yrts.1584098401#1899458401.yrtsi.1584098401', 'domain': '.yandex.ru', 'path': '/', 'expires': 1615634401.14406, 'size': 58, 'httpOnly': False, 'secure': True, 'session': False}, {'name': '_ym_wasSynced', 'value': '%7B%22time%22%3A1584098401147%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D', 'domain': '.yandex.ru', 'path': '/', 'expires': 1584202081, 'size': 107, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'gdpr', 'value': '0', 'domain': '.yandex.ru', 'path': '/', 'expires': -1, 'size': 5, 'httpOnly': False, 'secure': False, 'session': True}, {'name': 'mda', 'value': '0', 'domain': '.yandex.ru', 'path': '/', 'expires': 1646306401, 'size': 4, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_visorc_784657', 'value': 'b', 'domain': '.yandex.ru', 'path': '/', 'expires': 1584100201, 'size': 18, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_d', 'value': '1584098401', 'domain': '.yandex.ru', 'path': '/', 'expires': 1615634401, 'size': 15, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_uid', 'value': '15840984011037852822', 'domain': '.yandex.ru', 'path': '/', 'expires': 1615634401, 'size': 27, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'yuidss', 'value': '375002081584098400', 'domain': '.yandex.ru', 'path': '/', 'expires': 1899458401.144043, 'size': 24, 'httpOnly': False, 'secure': True, 'session': False}, {'name': 'yp', 'value': '1899458406.udn.cDpnZW90aXBz', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.527179, 'size': 29, 'httpOnly': False, 'secure': True, 'session': False}, {'name': '_ym_isad', 'value': '2', 'domain': '.yandex.ru', 'path': '/', 'expires': 1584170401, 'size': 9, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'Session_id', 'value': '3:1584098406.5.0.1584098406510:hHc51A:48.1|196471750.0.2|213903.694161.RIKCx8TRKA7g2rD-wXbfQdWaYoo', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.527111, 'size': 108, 'httpOnly': True, 'secure': True, 'session': False}, {'name': 'yandex_login', 'value': 'geotips', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.527217, 'size': 19, 'httpOnly': False, 'secure': True, 'session': False}, {'name': 'yandexuid', 'value': '375002081584098400', 'domain': '.yandex.ru', 'path': '/', 'expires': 1899458401.14402, 'size': 27, 'httpOnly': False, 'secure': True, 'session': False}]
cookie = [{'name': 'i', 'value': 'PwOucaHat1J8CXfksa5s7YZvis4INabTaK2I1sPNq44N80IZKY5MeG4D1UUbPX47CQNTE10O39oy4n7BNOZCny4fDQo=', 'domain': '.yandex.ru', 'path': '/', 'expires': 1899467943, 'size': 93, 'httpOnly': True, 'secure': True, 'session': False}, {'name': 'L', 'value': 'XF1RRgRSTlx7SHRgVmlNbWEEWFZZcUBZNQocFV5HJw==.1584107942.14169.391126.0dd9b61efa0dcce28a1e04bb8c93d8af', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.484203, 'size': 102, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'ys', 'value': 'udn.cDpnZW90aXBz', 'domain': '.yandex.ru', 'path': '/', 'expires': -1, 'size': 18, 'httpOnly': False, 'secure': True, 'session': True}, {'name': 'sessionid2', 'value': '3:1584107942.5.0.1584107942494:CTjesA:6.1|196471750.0.2|213907.520767.2f9yRtrCuiLoVPN3PblSCQ5jCj8', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.484033, 'size': 107, 'httpOnly': True, 'secure': True, 'session': False}, {'name': 'ymex', 'value': '1899467937.yrts.1584107937', 'domain': '.yandex.ru', 'path': '/', 'expires': 1615643937.359148, 'size': 30, 'httpOnly': False, 'secure': True, 'session': False}, {'name': '_ym_wasSynced', 'value': '%7B%22time%22%3A1584107937360%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D', 'domain': '.yandex.ru', 'path': '/', 'expires': 1584211617, 'size': 107, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'gdpr', 'value': '0', 'domain': '.yandex.ru', 'path': '/', 'expires': -1, 'size': 5, 'httpOnly': False, 'secure': False, 'session': True}, {'name': 'mda', 'value': '0', 'domain': '.yandex.ru', 'path': '/', 'expires': 1646315937, 'size': 4, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_visorc_784657', 'value': 'b', 'domain': '.yandex.ru', 'path': '/', 'expires': 1584109737, 'size': 18, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_d', 'value': '1584107937', 'domain': '.yandex.ru', 'path': '/', 'expires': 1615643937, 'size': 15, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_uid', 'value': '1584107937285461052', 'domain': '.yandex.ru', 'path': '/', 'expires': 1615643937, 'size': 26, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'yuidss', 'value': '255208111584107936', 'domain': '.yandex.ru', 'path': '/', 'expires': 1899467937.359139, 'size': 24, 'httpOnly': False, 'secure': True, 'session': False}, {'name': 'yp', 'value': '1899467942.udn.cDpnZW90aXBz', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.484127, 'size': 29, 'httpOnly': False, 'secure': True, 'session': False}, {'name': '_ym_isad', 'value': '2', 'domain': '.yandex.ru', 'path': '/', 'expires': 1584179937, 'size': 9, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'Session_id', 'value': '3:1584107942.5.0.1584107942494:CTjesA:6.1|196471750.0.2|213907.584641.n_6aBvvYa7LmcPhONHX00u6OetM', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.483948, 'size': 107, 'httpOnly': True, 'secure': True, 'session': False}, {'name': 'yandex_login', 'value': 'geotips', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.484242, 'size': 19, 'httpOnly': False, 'secure': True, 'session': False}, {'name': 'yandexuid', 'value': '255208111584107936', 'domain': '.yandex.ru', 'path': '/', 'expires': 1899467937.35912, 'size': 27, 'httpOnly': False, 'secure': True, 'session': False}]
cookie = [{'name': 'i', 'value': 'B4Rq1xRE7REPEFhp6gOf5NUPouslfr6yuuF8kkZg00a4K3pFyE3iR07mHow1gCRXk5YQi0Zr2QoOKB8iA07IcRNSCO8=', 'domain': '.yandex.ru', 'path': '/', 'expires': 1899468666, 'size': 93, 'httpOnly': True, 'secure': True, 'session': False}, {'name': 'L', 'value': 'XF1RRg1SSlp8S3JlVGVFZGEPV1NWdkFYNQAfDkFeOgQ0VFptZw==.1584108665.14169.350380.79b6c5180f870e145ab139b258654b1d', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.863607, 'size': 110, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'ys', 'value': 'udn.cDpnb2xvdmluaXNhajgz', 'domain': '.yandex.ru', 'path': '/', 'expires': -1, 'size': 26, 'httpOnly': False, 'secure': True, 'session': True}, {'name': 'sessionid2', 'value': '3:1584108665.5.0.1584108665774:CTjesA:1d.1|892202102.0.2|213909.654895._GODsvk4wlfFYCSAPDowpJqU7K8', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.86355, 'size': 108, 'httpOnly': True, 'secure': True, 'session': False}, {'name': 'ymex', 'value': '1899468660.yrts.1584108660#1899468660.yrtsi.1584108660', 'domain': '.yandex.ru', 'path': '/', 'expires': 1615644660.387122, 'size': 58, 'httpOnly': False, 'secure': True, 'session': False}, {'name': '_ym_wasSynced', 'value': '%7B%22time%22%3A1584108660389%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D', 'domain': '.yandex.ru', 'path': '/', 'expires': 1584212340, 'size': 107, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'gdpr', 'value': '0', 'domain': '.yandex.ru', 'path': '/', 'expires': -1, 'size': 5, 'httpOnly': False, 'secure': False, 'session': True}, {'name': 'mda', 'value': '0', 'domain': '.yandex.ru', 'path': '/', 'expires': 1646316660, 'size': 4, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_visorc_784657', 'value': 'b', 'domain': '.yandex.ru', 'path': '/', 'expires': 1584110460, 'size': 18, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_d', 'value': '1584108660', 'domain': '.yandex.ru', 'path': '/', 'expires': 1615644660, 'size': 15, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_uid', 'value': '1584108660510375538', 'domain': '.yandex.ru', 'path': '/', 'expires': 1615644660, 'size': 26, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'yuidss', 'value': '604344511584108659', 'domain': '.yandex.ru', 'path': '/', 'expires': 1899468660.387106, 'size': 24, 'httpOnly': False, 'secure': True, 'session': False}, {'name': 'yp', 'value': '1899468665.udn.cDpnb2xvdmluaXNhajgz', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.863571, 'size': 37, 'httpOnly': False, 'secure': True, 'session': False}, {'name': '_ym_isad', 'value': '2', 'domain': '.yandex.ru', 'path': '/', 'expires': 1584180660, 'size': 9, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'Session_id', 'value': '3:1584108665.5.0.1584108665774:CTjesA:1d.1|892202102.0.2|213909.309723.ldE339xV6-wIqj1Zqr4jqPBTtVY', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.86353, 'size': 108, 'httpOnly': True, 'secure': True, 'session': False}, {'name': 'yandex_login', 'value': 'golovinisaj83', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.863617, 'size': 25, 'httpOnly': False, 'secure': True, 'session': False}, {'name': 'yandexuid', 'value': '604344511584108659', 'domain': '.yandex.ru', 'path': '/', 'expires': 1899468660.387088, 'size': 27, 'httpOnly': False, 'secure': True, 'session': False}]

cookie = [{'name': 'i', 'value': 'Z0xqE+WeAtGHGlpDkxQNqPcmZM3kg8nbOrkF+qjMwbDUsc7jKeZFlLcYYH+hW+EyWUFIDfuBUyf6Rjt/NSYsuiNnUgI=', 'domain': '.yandex.ru', 'path': '/', 'expires': 1899733925, 'size': 93, 'httpOnly': True, 'secure': True, 'session': False}, {'name': 'yp', 'value': '1586965895.ygu.1#1600141900.szm.1%3A1920x1080%3A2000x768#1899733923.udn.cDpib2wuc2hha292YWx5dWRtaWxhNDc%3D', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.951452, 'size': 108, 'httpOnly': False, 'secure': True, 'session': False}, {'name': 'L', 'value': 'AHYGV3ZQdkhucA9edUQOfEAEV19HTVoHIRYVGztQMy4CDwcpOCcdXiwcUF9B.1584373923.14172.335573.1aae6db6a46192a30ce2e79d38e13bf2', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.951555, 'size': 118, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'cycada', 'value': 'UgdK77rpC7PjoTTpar4RClMuK7Fgx0AiEmGw/MxGYqU=', 'domain': '.yandex.ru', 'path': '/', 'expires': 1585583530, 'size': 50, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'ys', 'value': 'c_chck.190838080#udn.cDpib2wuc2hha292YWx5dWRtaWxhNDc%3D', 'domain': '.yandex.ru', 'path': '/', 'expires': -1, 'size': 57, 'httpOnly': False, 'secure': True, 'session': True}, {'name': 'sessionid2', 'value': '3:1584373923.5.0.1584373923917:783cTQ:6.1|880982969.0.2|214059.623947.38CzelppcwXILv3KuC5SLpFrjFs', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.951359, 'size': 107, 'httpOnly': True, 'secure': True, 'session': False}, {'name': 'mda', 'value': '0', 'domain': '.yandex.ru', 'path': '/', 'expires': 1678981897.582982, 'size': 4, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'Session_id', 'value': '3:1584373923.5.0.1584373923917:783cTQ:6.1|880982969.0.2|214059.276795.kDal21R0LCIgUuh0-QS6uYTFqgc', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.951301, 'size': 107, 'httpOnly': True, 'secure': True, 'session': False}, {'name': 'yc', 'value': '1584633099.zen.cach%3A1584377495', 'domain': '.yandex.ru', 'path': '/', 'expires': 1585583499, 'size': 34, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'zm', 'value': 'm-white_bender.webp.css-https%3As3home-static_k6S7IjoBbCK05jwm1xDstLiuf-s%3Al', 'domain': '.yandex.ru', 'path': '/', 'expires': 1585583498, 'size': 79, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_isad', 'value': '2', 'domain': '.yandex.ru', 'path': '/', 'expires': 1584445898, 'size': 9, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'font_loaded', 'value': 'YSv1', 'domain': 'yandex.ru', 'path': '/', 'expires': 1899733898.032284, 'size': 15, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_visorc_784657', 'value': 'b', 'domain': '.yandex.ru', 'path': '/', 'expires': 1584375716, 'size': 18, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_visorc_50377519', 'value': 'b', 'domain': '.yandex.ru', 'path': '/', 'expires': 1584375699, 'size': 20, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_d', 'value': '1584373898', 'domain': '.yandex.ru', 'path': '/', 'expires': 1615909897, 'size': 15, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'ymex', 'value': '1899733897.yrts.1584373897', 'domain': '.yandex.ru', 'path': '/', 'expires': 1615909897.48053, 'size': 30, 'httpOnly': False, 'secure': True, 'session': False}, {'name': '_ym_wasSynced', 'value': '%7B%22time%22%3A1584373897825%2C%22params%22%3A%7B%22eu%22%3A0%7D%2C%22bkParams%22%3A%7B%7D%7D', 'domain': '.yandex.ru', 'path': '/', 'expires': 1584477577, 'size': 107, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'gdpr', 'value': '0', 'domain': '.yandex.ru', 'path': '/', 'expires': 1615909926, 'size': 5, 'httpOnly': False, 'secure': False, 'session': False}, {'name': '_ym_uid', 'value': '158437389897455215', 'domain': '.yandex.ru', 'path': '/', 'expires': 1615909897, 'size': 25, 'httpOnly': False, 'secure': False, 'session': False}, {'name': 'my', 'value': 'YwA=', 'domain': '.yandex.ru', 'path': '/', 'expires': 1899733899.863544, 'size': 6, 'httpOnly': False, 'secure': True, 'session': False}, {'name': 'yandex_login', 'value': 'bol.shakovalyudmila47', 'domain': '.yandex.ru', 'path': '/', 'expires': 2147483647.951596, 'size': 33, 'httpOnly': False, 'secure': True, 'session': False}, {'name': 'yandexuid', 'value': '7327588111584373895', 'domain': '.yandex.ru', 'path': '/', 'expires': 1899733897.480444, 'size': 28, 'httpOnly': False, 'secure': True, 'session': False}, {'name': 'yabs-frequency', 'value': '/4/0000000000000000/7Q0_RJmw8OY4Sd0yEY5yyZrjF3ed/', 'domain': '.yandex.ru', 'path': '/', 'expires': 1593013897.503155, 'size': 63, 'httpOnly': False, 'secure': True, 'session': False}, {'name': 'yuidss', 'value': '7327588111584373895', 'domain': '.yandex.ru', 'path': '/', 'expires': 1899733897.480489, 'size': 25, 'httpOnly': False, 'secure': True, 'session': False}, {'name': 'yandex_gid', 'value': '213', 'domain': '.yandex.ru', 'path': '/', 'expires': 1586965895.415305, 'size': 13, 'httpOnly': False, 'secure': True, 'session': False}]

offset = 4000
def get_queries():
    global offset
    with psycopg2.connect(PG_CONN_STR) as conn:

        with conn.cursor() as cur:
            cur.execute('''
                SELECT
                    query
                FROM queries
                LIMIT 20
                OFFSET {}
                -- WHERE core_id = %s
                    -- AND processed = FALSE
            '''.format(offset)) #, (semantic_core_id,))
            db_result = cur.fetchall()

        queries = []
        for data in db_result:
            queries.append(data[0])
        # print(queries[0][0])

        result ="\"\n\"!".join(queries)

        result = '"' + result.replace(" ", " !")  + '"'
        print(result)

        offset += 20


        return result





async def _login():
    # args.append('--proxy-server={}'.format('193.233.149.187:44769'))
    args.append('--proxy-server={}'.format('77.220.205.239:44769'))
    browser = await launch({'headless': False, 'args': args})
    page = (await browser.pages())[0]

    await stealth(page)
    await page.setUserAgent(user_agent)
    await page.setViewport(viewport)
    await page.authenticate({'username': '8mVwslYhZl',
                             'password': 'geotips'})


    assert page
    # assert _yacc

    await page.goto(LOGIN_URL)

    login_field, login_btn = await asyncio.gather(
        page.waitForSelector('#passp-field-login', {'visible': True}),
        page.waitForSelector('div.passp-sign-in-button > button.passp-form-button', {'visible': True})
    )
    # await login_btn.screenshot({'path': 'btn.png'})
    await asyncio.sleep(1)
    await login_field.type('golovinisaj83@yandex.ru')
    # await login_field.type('geotips')
    await asyncio.sleep(1)
    await asyncio.gather(
        login_btn.click(),
        page.waitForNavigation()
    )
    await page.screenshot({'path': 'login.png'})

    pwd_field, login_btn = await asyncio.gather(
        page.waitForSelector('#passp-field-passwd', {'visible': True}),
        page.waitForSelector('div.passp-sign-in-button > button.passp-form-button', {'visible': True})
    )
    await asyncio.sleep(1)
    await pwd_field.type('d5JCs39o3iK9')
    # await pwd_field.type('ramzes')

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
                await phone_field.type('+79319856833')
                await asyncio.sleep(1)
                await asyncio.gather(
                    btn.click(),
                    page.waitForNavigation()
                )
    except NetworkError:
        # ???
        pass
    # await page.screenshot({'path': 'pwd.png'})
    await page.waitForSelector('img[alt="Директ"]', {'visible': True})
    await page.screenshot({'path': 'logged.png'})

    cookies = await page.cookies()
    print(cookies)
    print('Login successful')


async def clear_input_text(page: Page, input_node: ElementHandle):
    await page.keyboard.down('ControlLeft')
    await input_node.press('A')
    await page.keyboard.up('ControlLeft')
    await input_node.press('Backspace')


async def main():
    await _login()
    #for i in range(1, 20):
    #    print(i)
    #   words = get_queries()

    sys.exit()
    # words = get_queries()
    words = ['рама']
    # sys.exit'()
    # browser = await launch()
    # page = await browser.newPage()
    # await page.goto('https://direct.yandex.ru/registered/main.pl?cmd=advancedForecast')
    # await page.screenshot({'path': 'example.png'})
    # await _login()

    # sys.exit()

    args.append('--proxy-server={}'.format('193.233.149.187:44769'))
    #args.append('--proxy-server={}'.format('77.220.205.239:44769'))

    browser = await launch({'headless': False, 'args': args})
    page = (await browser.pages())[0]
    await stealth(page)
    await page.setUserAgent(user_agent)
    await page.setViewport(viewport)
    await page.setCookie(*cookie)

    # await asyncio.sleep(60)


    await page.authenticate({'username': '8mVwslYhZl',
                             'password': 'geotips'})

    # await page.goto('https://www.google.com/search?q=check+ip&oq=check+ip&aqs=chrome..69i57j0l7.6686j0j1&sourceid=chrome&ie=UTF-8')
    await page.goto('https://yandex.ru/')
    await asyncio.sleep(20)
    cookies = await page.cookies()
    print(cookies)


    await page.goto('https://direct.yandex.ru/registered/main.pl?cmd=advancedForecast')
    await asyncio.sleep(3)

    await asyncio.sleep(1)
    await page.screenshot({'path': '1.png'})

    query_field, submit_btn = await asyncio.gather(
        page.waitForSelector('#ad-words'),
        page.waitForSelector('input.b-advanced-forecast__submit-button')
    )

    print(192)



    await clear_input_text(page, query_field)
    print(words)
    await query_field.type(words)



    print('драма')

    await page.screenshot({'path': '5555.png', 'fullPage': True})
    print('драма-2')
    # await submit_btn.click()
    print('драма - 3')
   # await page.screenshot({'path': '65555.png', 'fullPage': True})
    # await page.screenshot({'path': '5555.png', 'fullPage': True})
    await asyncio.gather(
        submit_btn.click(),
        page.waitForSelector('tbody.b-advanced-forecast__result-table__table-body')
    )
    print('sleep')

    await asyncio.sleep(30)

    for i in range(0, 20):
        print(i)
        words = get_queries()

        await page.mouse.move(randrange(1366), randrange(768))
        await page.goto('https://direct.yandex.ru/registered/main.pl?cmd=advancedForecast')
        await asyncio.sleep(3)

        await page.mouse.move(randrange(1366), randrange(768))
        await asyncio.sleep(1)


        query_field, submit_btn = await asyncio.gather(
            page.waitForSelector('#ad-words'),
            page.waitForSelector('input.b-advanced-forecast__submit-button')
        )



        await asyncio.sleep(2)
        await clear_input_text(page, query_field)
        await asyncio.sleep(5)
        await page.mouse.move(randrange(1366), randrange(768))
        await page.hover('#footer')
        await query_field.type(words)
        await asyncio.sleep(1)
        await asyncio.gather(
            submit_btn.click(),
            page.waitForSelector('tbody.b-advanced-forecast__result-table__table-body')
        )

        await page.mouse.move(random(), random())
        await asyncio.sleep(10)
        await page.screenshot({'path': 'result/wordstat{}.png'.format(datetime.now())})
        await asyncio.sleep(2)


    cookies = await page.cookies()
    print(cookies)

    await asyncio.sleep(60)
    await page.screenshot({'path': '4444.png'})













    sys.exit()

















    await clear_input_text(page, query_field)
    # await query_field.type(words)
    await page.click('input.b-advanced-forecast__submit-button')
    print(196)

    print('недвижимость')
    await page.screenshot({'path': '2.png', 'fullPage': True})
    await asyncio.gather(
        submit_btn.click(),
        page.waitForSelector('tbody.b-advanced-forecast__result-table__table-body')
    )
    print('sleep')
    await asyncio.sleep(3)
    await page.screenshot({'path': '3.png', 'fullPage': True})




    # await clear_input_text(page, query_field)
    # await query_field.type('драма')
    #
    # print('драма')
    # await asyncio.gather(
    #     submit_btn.click(),
    #     page.waitForSelector('tbody.b-advanced-forecast__result-table__table-body')
    # )
    # print('sleep')
    # await page.screenshot({'path': '4.png'})




    # a =  await asyncio.gather(
    #      page.waitForSelector('#ad-words'))
    # print(a)



    print(query_field)
    print(submit_btn)
    sys.exit()


    await browser.close()

asyncio.get_event_loop().run_until_complete(main())