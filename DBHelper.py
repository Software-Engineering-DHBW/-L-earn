import sqlite3
import logging

# table names
table_data = "data"
table_bp = "bannedProcesses"

# column names
column_pName = "processName"
column_date = "date"
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
            stmt = f"CREATE TABLE IF NOT EXISTS {table_data} (" \
                   f"{column_pName} Text, " \
                   f"{column_date} Text, " \
                   f"{column_time} Integer)"
            self.conn.execute(stmt)

            # Create table for banned Processes
            stmt = f"CREATE TABLE IF NOT EXISTS {table_bp} (" \
                   f"{column_pName} Text, " \
                   f"{column_user} Text, CONSTRAINT unq UNIQUE (" \
                   f"{column_pName} , {column_user}))"
            self.conn.execute(stmt)

            self.conn.commit()

        def __setLogger(self):
            # create a logger
            self.logger = logging.getLogger('dblogger')
            # set logger level
            self.logger.setLevel(logging.ERROR)
            # or set one of the following level
            # logger.setLevel(logging.CRITICAL)
            # logger.setLevel(logging.WARNING)
            # logger.setLevel(logging.INFO)
            # logger.setLevel(logging.DEBUG)

            handler = logging.FileHandler('logs/dblog.log')
            # create a logging format
            formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # Methods for data table
        def readData(self, date):
            stmt = f"SELECT {column_pName}, {column_time} FROM {table_data} WHERE {column_date} = (?)"
            args = (date,)
            return list(self.conn.execute(stmt, args))

        def readAllData(self):
            stmt = "SELECT * FROM " + table_data
            return list(self.conn.execute(stmt))

        def updateData(self, date, time, processName):
            stmt = f"SELECT {column_time} FROM {table_data} WHERE {column_pName} = (?) AND {column_date} = (?)"
            args = (processName, date,)
            result = self.conn.execute(stmt, args).fetchall()
            if len(result) != 0:
                time = result[0][0] + time
                stmt = f"UPDATE {table_data} SET {column_time} = (?) WHERE {column_pName} = (?) AND {column_date} = (?)"
                args = (time, processName, date,)
                try:
                    self.conn.execute(stmt, args)
                    self.conn.commit()
                    self.logger.info(f'Updated {processName} in table ' + table_data)
                except sqlite3.Error as e:
                    self.logger.error('An Error occurred while updating ' + processName
                                      + f' in table {table_data}: ' + ''.join(e.args))
            else:
                self.logger.warning(f'Entry for {processName} does not exist in table ' + table_data
                                    + ' and could not be updated')

        def writeData(self, date, time, processName):
            stmt = f"SELECT rowid FROM {table_data} WHERE {column_pName} = (?) AND {column_date} = (?)"
            args = (processName, date,)
            data = self.conn.execute(stmt, args).fetchall()

            # if there is no entry insert
            # else update time
            if len(data) == 0:
                stmt = f"INSERT INTO {table_data} ({column_pName}, {column_time}, {column_date}) VALUES (?, ?, ?)"
                args = (processName, time, date,)
                self.__write(stmt, args, processName, table_data)
            else:
                self.updateData(date, time, processName)

        def deleteData(self, processName, date):
            self.__delete(table_data, column_pName, column_date, processName, date)

        # Methods for bannedProcesses table
        def readBP(self, userName):
            stmt = f"SELECT {column_pName} FROM {table_bp} WHERE {column_user} = (?)"
            args = (userName,)
            return [x[0] for x in self.conn.execute(stmt, args)]

        def writeBP(self, processName, userName):
            stmt = f"INSERT INTO {table_bp} ({column_pName}, {column_user}) VALUES (?, ?)"
            args = (processName, userName,)
            self.__write(stmt, args, processName, table_bp)

        def deleteBP(self, processName, userName):
            self.__delete(table_bp, column_pName, column_user, processName, userName)

        # Methods for both tables
        def __write(self, stmt, args, processName, table):
            try:
                self.conn.execute(stmt, args)
                self.conn.commit()
                self.logger.info(f'Added {processName} into table ' + table)
            except sqlite3.Error as e:
                self.logger.error('An Error occurred while adding ' + processName
                                  + f' into table {table}: ' + ''.join(e.args))

        def __delete(self, table, col1, col2, val1, val2):
            stmt = f"DELETE FROM {table} WHERE {col1} = (?) AND {col2} = (?)"
            args = (val1, val2,)
            try:
                self.conn.execute(stmt, args)
                self.conn.commit()
                self.logger.info(f'Deleted {val1} from table ' + table)
            except sqlite3.Error as e:
                self.logger.error('An Error occurred while deleting ' + val1
                                  + f' from table {table}: ' + ''.join(e.args))

    instance = None

    def __new__(cls, *args, **kwargs):
        if not DBHelper.instance:
            DBHelper.instance = DBHelper.__DBHelper()
        return DBHelper.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
