import psycopg2
import datetime


class DataBasePeeker:
    # init
    def __init__(self, database, host, user, password):
        self.database = database
        self.max_query_time = 1
        self.max_process_time = 60
        self.longest_process = 0
        self.max_long_processes = 2
        self.long_query_pids = []
        self.long_process_pids = []
        self._conn = psycopg2.connect(database=database,
                                      host=host,
                                      user=user,
                                      password=password)
        print("Connection established")

    def __del__(self):
        self._conn.close()

    # interface methods
    def peek(self):
        with self._conn.cursor() as crs:
            crs.execute("select clock_timestamp() - query_start as qruntime," +
                        " clock_timestamp() - backend_start as bruntime, pid, datname, usename, query, state" +
                        " from pg_stat_activity" +
                        " where query_start is not null" +
                        " and pid <> pg_backend_pid()" +
                        " order by 1 desc;")
            stats = crs.fetchall()
            report = ""
            self.long_query_pids = []
            self.long_process_pids = []
            for stat in stats:
                #print(stat)
                self.check_query_running_time(stat)
                self.check_process_running_time(stat)
            report += self.overall_report()
            report += self.query_running_report()
            report += self.process_running_report()
            report += self.check_max_process_time()
            return report

    def fix(self, option_code):
        if option_code == 1:
            return self.term_long_queries()
        if option_code == 2:
            return self.term_long_processes()
        if option_code == 3:
            return self.checkpoint()

    # internal methods
    def check_max_process_time(self):
        return "current max process time is {}\n".format(self.longest_process)

    def check_query_running_time(self, stat):
        (qtime, btime, pid, datname, usename, query, state) = stat
        process_time = qtime.total_seconds()
        if state != 'active':
            return
        if process_time > self.max_query_time:
            #print("LOG: query in process " + str(pid) + " is running for " + str(process_time))
            self.long_query_pids.append(pid)

    def check_process_running_time(self, stat):
        self.longest_process = 0
        (time, btime, pid, datname, usename, query, state) = stat
        #print(stat)
        process_time = btime.total_seconds()
        if process_time > self.longest_process:
            self.longest_process = process_time
        if process_time > self.max_process_time:
            #print("LOG: process " + str(pid) + " is running for " + str(process_time))
            self.long_process_pids.append(pid)

    def query_running_report(self):
        return "{} process queries exceeding maximum query time\n".format(len(self.long_query_pids))

    def process_running_report(self):
        return "{} processes exceeding maximum process time\n".format(len(self.long_process_pids))

    def overall_report(self):
        if (len(self.long_process_pids) <= self.max_long_processes and
                len(self.long_query_pids) <= self.max_long_processes):
            return "Database stable\n"
        return "Database failures detected\n"

    def term_long_queries(self):
        cnt = 0
        for pid in self.long_query_pids:
            with self._conn.cursor() as crs:
                crs.execute("select pg_terminate_backend(%s)", (pid, ))
                (success) = crs.fetchone()
                if success:
                    #print("LOG: process " + str(pid) + " termianted")
                    cnt += 1
        return "terminated {} processes\n".format(cnt)

    def term_long_processes(self):
        cnt = 0
        for pid in self.long_process_pids:
            with self._conn.cursor() as crs:
                crs.execute("select pg_terminate_backend(%s)", (pid,))
                (success) = crs.fetchone()
                if success:
                    # print("LOG: process " + str(pid) + " termianted")
                    cnt += 1
        return "terminated {} processes\n".format(cnt)

    def checkpoint(self):
        with self._conn.cursor() as crs:
            crs.execute("checkpoint")
        return "checkpoint created\n"
