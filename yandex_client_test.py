from ywordstast_client import YWordstatClient



def _build_core_worker(semantic_core_id: int, run_id: int, input_q: mp.Queue) -> None:
    redis_conf = RedisConf(
        host='redis',
        db=ACCS_DB,
        password='Eingae2muo'
    )
    ws_client = YWordstatClient(redis_conf=redis_conf)
    loop = asyncio.get_event_loop()

    def get_conn() -> connection:
        conn: connection = psycopg2.connect(PG_CONN_STR)
        conn.autocommit = True
        return conn

    conn = get_conn()
    conn.autocommit = True

    def close_client() -> None:
        try:
            loop.run_until_complete(ws_client.close())
        except Exception:
            logger.error(traceback.format_exc())

    for anchors in iter(input_q.get, 'STOP'):
        amount = len(anchors)
        anchors_ids = {q[1]: q[0] for q in anchors}
        done = False
        for _ in range(3):
            try:
                results = loop.run_until_complete(ws_client.query(anchors_ids.keys()))
            except Exception:
                logger.error(traceback.format_exc())
                close_client()
                ws_client = YWordstatClient()
                continue
            try:
                insert_data = []
                for anchor, res in results.items():
                    anchor_id = anchors_ids[anchor]
                    for query, freq in res['phrases'].items():
                        insert_data.append((query, freq, anchor_id))
                _insert_queries(conn, semantic_core_id, insert_data)
                with conn.cursor() as cur:
                    cur.execute('''
                        UPDATE anchor_queries
                        SET processed = TRUE
                        WHERE id in %s
                    ''', (tuple(anchors_ids.values()),))
                    cur.execute('''
                        UPDATE wordstat_runs
                        SET n_queries = n_queries + %s
                        WHERE id = %s
                    ''', (len(insert_data), run_id))
            except Exception:
                logger.error(traceback.format_exc())
                try:
                    conn.close()
                except Exception:
                    pass
                conn = get_conn()
                continue
            done = True
            break
        if not done:
            logger.error('Too many erros. Stopping worker...')
            close_client()
            return
    try:
        loop.run_until_complete(close_client)
    except Exception:
        pass