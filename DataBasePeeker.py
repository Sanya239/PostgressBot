import psycopg2
import random


class DataBasePeeker:
    # init
    def __init__(self):
        self.name = "name"
        #self.conn = psycopg2.connect(database="bebebe",host="localhost",user="Sanya",password="6667")
        #self.cursor = self.conn.cursor()
        print("Database created")

    # interface methods
    def peek(self) -> int:
        #self.cursor.execute("SELECT * FROM pg_stat_activity")
        #stats = self.cursor.fetchone()
        #print(stats)
        if(random.randint(1,10)<4):
            return 1
        return 0

    def fix(self, option_code):
        pass

