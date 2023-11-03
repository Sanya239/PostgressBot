import psycopg2


class DataBasePeeker:
    # init
    def __init__(self):
        self.conn = psycopg2.connect(database="db_name",
                                     host="dp_host",
                                     user="db_user",
                                     password="dp_pass",
                                     port="db_port")
        self.cursor = self.conn.cursor()

    # interface methods
    def peek(self) -> int:
        return 0

    def fix(self, option_code):
        pass
