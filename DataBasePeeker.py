import psycopg2


class DataBasePeeker:
    # init
    def __init__(self):
        self.conn = psycopg2.connect(database="db_name",
                                     host="dp_host",
                                     user="db_user",
                                     password="dp_pass")
        self.cursor = self.conn.cursor()

    # interface methods
    def peek(self) -> int:
        self.cursor.execute("SELECT * FROM pg_stat_activity")
        stats = self.cursor.fetchone()
        print(stats)
        return 0

    def fix(self, option_code):
        pass
