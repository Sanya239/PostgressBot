import psycopg2


class DataBasePeeker:
    # init
    def __init__(self, database, host, user, password):
        self.conn = psycopg2.connect(database=database,
                                     host=host,
                                     user=user,
                                     password=password)
        print("Connection established")
        self.online = True

    def __del__(self):
        self.conn.close()

# interface methods
    def peek(self) -> int:
        with self.conn.cursor() as crs:
            crs.execute("SELECT * FROM public.\"SomeTable\"")
            f = crs.fetchone()
            print(f)
            crs.execute("select current_timestamp - query_start as runtime, datname, usename,"+
                        " query from pg_stat_activity where query != '<IDLE>' order by 1 desc;")
            (state) = crs.fetchone()
            print(state)

        return 0

    def fix(self, option_code):
        pass
