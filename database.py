#!/usr/bin/env python3

import sqlite3 as _sqlite3
from sqlite3 import Error as SQLError
from table_templates import DATA_SMLOUVY
import testovaci_data

class Database:
    def __init__(self, db_file) -> None:
        self.db_file = db_file
        self.__conn = self.__create_connection(self.db_file)
        self.__cur = self.__conn.cursor()
        #When a new connection is made, SQLite implicitly sets PRAGMA foreign_keys = OFF.
        self.execute('PRAGMA foreign_keys = ON')
        self.commit()
        if self.__create_tables():
            self.__add_admin()
            self.__add_val_to_tables(testing_data=True)
            self.commit()

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

# queries
    def execute(self, *args: list):
        '''Executes SQL query'''
        self.__cur.execute(*args)

    def get_values(self, *args):
        '''Gets values from SQL query'''
        self.__cur.execute(*args)
        values = self.__cur.fetchall()
        return values

    def __execute_many(self, *args):
        self.__cur.executemany(*args)

# create tables
    def __create_tables(self):
        '''If the tables do not exist in the database, it creates them.'''
        tables = self.__cur.execute("SELECT name FROM sqlite_master")
        if tables.fetchone() == None:
            from table_templates import tables_sql
            try:
                for query in tables_sql:
                    self.__cur.execute(query)
                self.commit()
                return True
            except SQLError as err:
                print(err)
        else:
            return False

    def __add_admin(self):
        from utils import get_hash

        '''Adding frist administrator with passwd where admin ID = admin@admin.cz'''
        print('Totho je první spuštění aplikace. Je potřeba nastavit jméno a heslo pro administrátora.')
        admin_email = 'admin@admin.cz'
        passwd_hash = get_hash(admin_email)
        self.execute('INSERT INTO users_auth(users_id, hash_passwd, admin) VALUES(?,?,1)' ,[admin_email, passwd_hash])
        self.commit()

#add testing data
    def __add_val_to_tables(self, testing_data= False):
        '''Inserts predefined data into the tables.'''
        self.__execute_many('INSERT INTO smlouvy(nazev, popis) VALUES(?,?)' ,DATA_SMLOUVY)
        self.__execute_many('INSERT INTO users_auth(users_id, hash_passwd) VALUES(?,?)' ,testovaci_data.DATA_USERS)
        if testing_data:
            print('Toto je testovací verze, do databáze jsou nahrány testovací data.')
            from testovaci_data import DATA_KLIENTI
            self.__execute_many('INSERT INTO klienti(jmeno, prijmeni, datum_narozeni, telefon, email) VALUES(?,?,?,?,?)', DATA_KLIENTI)
            self.__execute_many('INSERT INTO klienti_smlouvy (klient_id, smlouva_id, datum_zalozeni, datum_ukonceni) VALUES(?,?,?,?)', testovaci_data.DATA_KLIENTI_SMLOUVY)
        self.commit()