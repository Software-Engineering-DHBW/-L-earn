"""
Defines the database and all database functions
"""
import os
import sqlite3
import logging
import pandas as pd
from datetime import datetime

import Learn

# table names
table_data = "data"
table_bp = "bannedProcesses"

# column names
column_pName = "name"
column_date = "date"
column_runtime = "runtime"
column_user = "user"
column_limittime = "limittime"


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
                   f"{column_runtime} Integer)"
            self.conn.execute(stmt)

            # Create table for banned Processes
            stmt = f"CREATE TABLE IF NOT EXISTS {table_bp} (" \
                   f"{column_pName} Text, " \
                   f"{column_limittime} INTEGER, " \
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

            if not os.path.isdir('logs'):
                os.makedirs('logs')
            handler = logging.FileHandler(os.path.join("logs", "dblog.log"))
            # create a logging format
            formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        # Methods for data table
        def readData(self, date):
            # get all saved processes and times for specified date
            try:
                self.conn = sqlite3.connect(self.dbname)
            except sqlite3.Error as e:
                self.logger.critical('local database initialisation error: "%s"', e)

            stmt = f"SELECT * FROM {table_data} WHERE {column_date} = (?)"
            args = (date,)
            query = self.conn.execute(stmt, args)
            print(query.description)
            cols = [column[0] for column in query.description]
            results = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
            results['date'] = results['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
            return results

        def readAllData(self):
            # get all saved processes and times
            try:
                self.conn = sqlite3.connect(self.dbname)
            except sqlite3.Error as e:
                self.logger.critical('local database initialisation error: "%s"', e)

            stmt = "SELECT * FROM " + table_data
            query = self.conn.execute(stmt)
            cols = [column[0] for column in query.description]
            results = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
            results['date'] = results['date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').date())
            return results

        def updateData(self, date, time, processName):
            # update time of existing entry
            try:
                self.conn = sqlite3.connect(self.dbname)
            except sqlite3.Error as e:
                self.logger.critical('local database initialisation error: "%s"', e)

            stmt = f"SELECT {column_runtime} FROM {table_data} WHERE {column_pName} = (?) AND {column_date} = (?)"
            args = (processName, date,)
            result = self.conn.execute(stmt, args).fetchall()
            if len(result) != 0:
                stmt = f"UPDATE {table_data} SET {column_runtime} = (?) WHERE {column_pName} = (?) AND {column_date} = (?)"
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
            # save process, date and time
            try:
                self.conn = sqlite3.connect(self.dbname)
            except sqlite3.Error as e:
                self.logger.critical('local database initialisation error: "%s"', e)

            stmt = f"SELECT rowid FROM {table_data} WHERE {column_pName} = (?) AND {column_date} = (?)"
            args = (processName, date,)
            data = self.conn.execute(stmt, args).fetchall()

            # if there is no entry insert
            # else update time
            if len(data) == 0:
                stmt = f"INSERT INTO {table_data} ({column_pName}, {column_runtime}, {column_date}) VALUES (?, ?, ?)"
                args = (processName, time, date,)
                self.__write(stmt, args, processName, table_data)
            else:
                self.updateData(date, time, processName)

        def deleteData(self, processName, date):
            self.__delete(table_data, column_pName, column_date, processName, date)

        # Methods for bannedProcesses table
        def readBP(self, userName):
            # get all saved limits
            try:
                self.conn = sqlite3.connect(self.dbname)
            except sqlite3.Error as e:
                self.logger.critical('local database initialisation error: "%s"', e)

            stmt = f"SELECT {column_pName}, {column_limittime} FROM {table_bp} WHERE {column_user} = (?)"
            args = (userName,)
            query = self.conn.execute(stmt, args)
            cols = [column[0] for column in query.description]
            results = pd.DataFrame.from_records(data=query.fetchall(), columns=cols)
            return results

        def writeBP(self, processName, limittime, userName):
            # save new limit
            try:
                self.conn = sqlite3.connect(self.dbname)
            except sqlite3.Error as e:
                self.logger.critical('local database initialisation error: "%s"', e)

            stmt = f"INSERT INTO {table_bp} ({column_pName}, {column_limittime}, {column_user}) VALUES (?, ?, ?)"
            args = (processName, limittime, userName,)
            self.__write(stmt, args, processName, table_bp)

        def deleteBP(self, processName, userName):
            # delete limit
            self.__delete(table_bp, column_pName, column_user, processName, userName)

        # Methods for both tables
        def __write(self, stmt, args, processName, table):
            # write in database
            try:
                self.conn = sqlite3.connect(self.dbname)
            except sqlite3.Error as e:
                self.logger.critical('local database initialisation error: "%s"', e)

            try:
                self.conn.execute(stmt, args)
                self.conn.commit()
                self.logger.info(f'Added {processName} into table ' + table)
            except sqlite3.Error as e:
                self.logger.error('An Error occurred while adding ' + processName
                                  + f' into table {table}: ' + ''.join(e.args))

        def __delete(self, table, col1, col2, val1, val2):
            # delete from database
            try:
                self.conn = sqlite3.connect(self.dbname)
            except sqlite3.Error as e:
                self.logger.critical('local database initialisation error: "%s"', e)

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
