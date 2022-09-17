#!/usr/bin/env python3
from curses.ascii import isalnum
import re
from traceback import print_tb
from webbrowser import get
from database import Database as db
from utils import *


class User:

    def __init__(self, db_file) -> None:
        self.db = db(db_file)

    def get_my_info(self):
        self.id
        query = ''' SELECT jmeno, prijmeni, datum_narozeni, telefon
                    FROM klienti
                    WHERE klienti_id = ?'''

    def db_close(self):
        self.db.db_close()

class Admin(User):

    def __init__(self, db_file) -> None:
        super().__init__(db_file)

    def add_new_client(self):
        print('Přidání nového klienta.\n')
        jmeno = input("Zadejte jméno: ").capitalize()
        prijmeni = input("Zadejte příjmení: ").capitalize()
        datum_narozeni = input('Zadejte datum narození formát rok-měsíc-den:')
        telefoni_cislo = input('Zadejte telefoní číslo: ')
        vals = (jmeno, prijmeni, datum_narozeni, telefoni_cislo)
        vals = [i.strip() for i in vals]
        print(vals)
        verification = input('Pro potvrzení napište A, nebo jen zmačkněte Enter pro zrušení: ')
        if verification == 'A':
            query = '''INSERT INTO klienti (jmeno, prijmeni, datum_narozeni, telefon) VALUES (?,?,?,?)'''
            self.db.execute(query, vals)
            self.db.commit()
            print('Záznam byl úspěšně přidán.')
        else:
            print('Záznam nebyl přidán.')

    def get_all_clients(self):
        query = '''SELECT * FROM klienti'''
        result = self.db.get_values(query)
        result = self._get_age_in_result(result)
        self._print_returned_vals(result)
        return result

    def get_client_by_name(self):
        jmeno = input('Zadejte hledané jméno: ')
        prijmeni = input('Zadejte hledané příjmneí: ')
        vals = (jmeno, prijmeni)
        query = f'''SELECT klienti_id ,jmeno, prijmeni, datum_narozeni, telefon
                    FROM klienti
                    WHERE jmeno LIKE ? AND prijmeni LIKE ?'''
        result = self.db.get_values(query,vals)
        if len(result) > 0:
            result = self._get_age_in_result(result)
            self._print_returned_vals(result)
            return result
        else:
            print('Vámi zadaný požadavek nevyhovuje žádnému záznamu.')

    def get_client_by_id(self, id):
        query = f'''SELECT klienti_id ,jmeno, prijmeni, datum_narozeni, telefon
                    FROM klienti
                    WHERE klienti_id = ?'''
        result = self.db.get_values(query, str(id))
        self._print_returned_vals(result)
        return result

    def get_my_info(self):
        return 'Jsi administrátor pojišťovny a nemáš účet.'

    def edit_client_record(self):
        try:
            id_zaznamu = input('Zadej id záznamu který chceš změnit: ')
            column_names = self._get_col_names_klienti()
            target = self.get_client_by_id(id_zaznamu)[0]
            [print(column_names[i], '=', target[i]) for i in range(1,len(target))]
            col_name = input('Zadej nazev sloupku pro změnu(např: jmeno): ')
            set_value = input('Zadej hodnotu pro změnu: ')
            if col_name == 'telefon' and not set_value.isnumeric():
                raise ValueError
            elif col_name == 'datum_narozeni':
                chck = check_date(set_value)
                print(chck)
            if id_zaznamu.isnumeric() and col_name in column_names:
                query = f"UPDATE klienti SET {col_name} = (?) WHERE klienti_id = {id_zaznamu}"
                self.db.execute(query, [set_value])
                self.db.commit()
        except ValueError:
            print('Zadána špatná hodnota.')



    def _get_col_names_klienti(self):
        query = "SELECT c.name FROM pragma_table_info('klienti') c"
        query_result = self.db.get_values(query)
        result = [i[0] for i in query_result]
        return result


    @warning
    def remove_client(self):
        klient_id = input('Zadej id klienta pro smazání záznamu: ')
        if klient_id != '' and klient_id.isnumeric():
            if len(self.get_client_by_id(klient_id)) > 0:
                print('Opravdu chcete smazat?: ')
                answer = input('Napiště A pro ano, nebo Enter pro zrušení: ')
                if answer == "A":
                    query = "DELETE FROM klienti WHERE klienti_id = ?"
                    self.db.execute(query, str(klient_id))
                    self.db.commit()
                    return True
                else:
                    print('Transakce zrušena.')
            else:
                print("Žádný záznam nevyhovuje zadanemu ID klienta.")

    def _print_returned_vals(self, result):
        [print('\t'.join(map(str, i))) for i in result]

    def _get_age_in_result(self, result):
        for i, j in enumerate(result):
            result[i] = list(result[i])
            result[i][3] = get_age(result[i][3])
        return result

#admin = Admin('pojistovna.db')
#admin.edit_client_record()
##admin.add_new_client()
#admin.get_all_clients()
#print()
##admin.get_client_by_name()
#admin.remove_client()
#admin.get_all_clients()
#admin.db.db_close()