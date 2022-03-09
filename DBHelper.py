import sqlite3
import logging

# table names
table_data = "data"
table_bp = "bannedProcesses"

# column names
column_name = "name"
column_time = "time"
column_user = "user"


class DBHelper(object):
    class __DBHelper:
        def __init__(self, dbname="db.sqlite"):
            self.__setLogger()

            self.dbname = dbname
            try:
                self.conn = sqlite3.connect(dbname)
            except sqlite3.Error as e:
                self.logger.critical('local database initialisation error: "%s"', e)

            self.__setup()

        def __setup(self):
            # Create table for data
            stmt = "CREATE TABLE IF NOT EXISTS " + table_data + " (" \
                   + column_name + " Text, " \
                   + column_time + " Integer)"
            self.conn.execute(stmt)

            # Create table for banned Processes
            stmt = "CREATE TABLE IF NOT EXISTS " + table_bp + " (" \
                   + column_name + " Text, " \
                   + column_user + " Text, CONSTRAINT unq UNIQUE (" \
                   + column_name + ", " + column_user + "))"
            self.conn.execute(stmt)

            self.conn.commit()

        def __setLogger(self):
            # create a logger
            self.logger = logging.getLogger('dblogger')
            # set logger level
            self.logger.setLevel(logging.WARNING)
            # or set one of the following level
            # logger.setLevel(logging.ERROR)
            # logger.setLevel(logging.CRITICAL)
            # logger.setLevel(logging.INFO)
            # logger.setLevel(logging.DEBUG)

            handler = logging.FileHandler('logs/dblog.log')
            # create a logging format
            formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        def readData(self, time):
            return self.__read(table_data, column_name, column_time, time)

        def writeData(self, time, processName):
            self.__write(table_data, column_name, column_time, processName, time)

        def deleteData(self, time):
            stmt = "DELETE FROM " + table_data + " WHERE " + column_time + " = (?)"
            args = (time,)
            self.conn.execute(stmt, args)
            self.conn.commit()

        def readBP(self, userName):
            return self.__read(table_bp, column_name, column_user, userName)

        def writeBP(self, processName, userName):
            self.__write(table_bp, column_name, column_user, processName, userName)

        def deleteBP(self, processName, userName):
            stmt = "DELETE FROM " + table_bp + " WHERE " + column_name + " = (?) AND " + column_user + " = (?)"
            args = (processName, userName,)
            self.conn.execute(stmt, args)
            self.conn.commit()

        def __read(self, table, col1, col2, val):
            stmt = "SELECT " + col1 + " FROM " + table + " WHERE " + col2 + " = (?)"
            args = (val,)
            return [x[0] for x in self.conn.execute(stmt, args)]

        def __write(self, table, col1, col2, val1, val2):
            stmt = "INSERT INTO " + table + " (" + col1 + ", " + col2 + ") VALUES (?, ?)"
            args = (val1, val2,)
            try:
                self.conn.execute(stmt, args)
                self.conn.commit()
            except sqlite3.Error as e:
                self.logger.error('An Error occurred while adding ' + str(val1)
                                  + ' into database: ' + ''.join(e.args))

    instance = None

    def __new__(cls, *args, **kwargs):
        if not DBHelper.instance:
            DBHelper.instance = DBHelper.__DBHelper()
        return DBHelper.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
