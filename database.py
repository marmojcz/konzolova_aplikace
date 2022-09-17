#!/usr/bin/env python3

from ast import arg
import sqlite3 as _sqlite3
from sqlite3 import Error as SQLError
from webbrowser import get

class Database:
    def __init__(self, db_file) -> None:
        self.db_file = db_file
        self.__conn = self.__create_connection(self.db_file)
        self.__cur = self.__conn.cursor()
        self.__create_tables()

    def __str__(self) -> str:
        return f'Databáze {self.db_file}.'

    def __repr__(self) -> str:
        return f'{self.db_file}'

    def __create_connection(self, db_file):
        '''Create database connection. Default to RAM.'''
        __conn = None
        try:
            __conn = _sqlite3.connect(db_file)
            return __conn
        except SQLError as e:
            print(e)
        return __conn

    def commit(self):
        '''Save changes to database.'''
        self.__conn.commit()

    def db_close(self):
        '''Close database connection.'''
        self.__conn.close()

#queries
    def execute(self, *args:list):
        self.__cur.execute(*args)


    def get_values(self, *args):
        self.__cur.execute(*args)
        values = self.__cur.fetchall()
        return values

#create tables
    def __create_tables(self):
        '''If the tables do not exist in the database, it creates them.'''
        tables = self.__cur.execute("SELECT name FROM sqlite_master")
        if tables.fetchone() == None:
            from table_templates import tables_sql
            try:
                for query in tables_sql:
                    self.__cur.execute(query)
                self.commit()
            except SQLError as err:
                print(err)

#db = Database('pojistovna.db')
