#!/usr/bin/env python3

from database import Database as db
from utils import *

class User:

    def __init__(self, db_file) -> None:
        self.db = db(db_file)
        self.insurance_offered = self._insurance_offered()

    def get_my_info(self):
        self.id
        query = ''' SELECT jmeno, prijmeni, datum_narozeni, telefon
                    FROM klienti
                    WHERE klienti_id = ?'''

    def db_close(self):
        self.db.db_close()

    def _chck_insurance(self):
        while True:
            num = input('Zadej id pojištění: ')
            if num.isnumeric():
                if int(num) in list(self.insurance_offered.keys()):
                    return num
                else:
                    print('Zadané id pojištění neexistuje.')
            else:
                print('Musí být čísleníá hodnota.')

    def _insurance_offered(self) -> dict:
        '''Return dictionary with offered insurance'''
        query = 'SELECT smlouvy_id, nazev FROM smlouvy'
        result = self.db.get_values(query)
        result = {i[0]:i[1] for i in result}
        return result

    def _chck_client_id(self) -> str:
        while True:
            client_id = input('Zadejte id klienta: ')
            if client_id.isnumeric():
                check = self.get_client_by_id(client_id)
                if check != None:
                    return client_id
            else:
                print('Hodnota muí být číslo!')
                continue

    def get_types_of_insurence(self):
        query = 'SELECT smlouvy_id, nazev FROM smlouvy'
        result = self.db.get_values(query)
        self._print_returned_vals(result)

    def _print_returned_vals(self, result):
        [print('\t   \t   '.join(map(str, i))) for i in result]


class Admin(User):

    def __init__(self, db_file) -> None:
        super().__init__(db_file)

    def add_new_client(self):
        try:
            print('Přidání nového klienta.\n')
            jmeno = input("Zadejte jméno: ").capitalize()
            prijmeni = input("Zadejte příjmení: ").capitalize()
            print('Datum narození.')
            datum_narozeni = self._chck_date(lower=True, chck_today=True, return_date=True)
            telefoni_cislo = self._insert_mobile_number()
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
        except KeyboardInterrupt:
            pass

    def get_all_clients(self):
        query = '''SELECT * FROM klienti'''
        result = self.db.get_values(query)
        result = self._get_age_in_result(result)
        self._print_returned_vals(result)
        return result

    def get_client_detail(self):
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

    def get_client_by_id(self, id, print_val=False):
        query = f'''SELECT klienti_id ,jmeno, prijmeni, datum_narozeni, telefon
                    FROM klienti
                    WHERE klienti_id = ?'''
        result = self.db.get_values(query, [id])
        if result == []:
            print('Zadané id neexistuje')
            return None
        else:
            if print_val:
                self._print_returned_vals(result)
            return result

    def get_my_info(self):
        return 'Jsi administrátor pojišťovny a nemáš účet.'

    def edit_client_record(self):
        client_id = self._chck_client_id()
        column_names = self._get_col_names_klienti()
        values = self.get_client_by_id(client_id)[0]
        for i in range(1,len(values)):
            print(i,column_names[i], '->', values[i])
        val_id = self._edit_client_record_val_id(column_names)
        set_value = self._edit_client_record_value(val_id)
        query = f"UPDATE klienti SET {column_names[int(val_id)]} = (?) WHERE klienti_id = {client_id}"
        self.db.execute(query, [set_value])
        self.db.commit()

    def _edit_client_record_value(self, val_id):
        while True:
            value = input('Zadej změněnou hodnotu: ')
            if val_id == '3':
                value = self._chck_date(date=value, lower=True, chck_today=True, return_date=True)
                if value:
                    return value
                else:
                    print('Nemůžeš být starší než dnešní den.')
                    continue
            if val_id == '4' and val_id.isnumeric() and 12 >= len(val_id) >= 9:
                return value
            else:
                return value.capitalize()

    def _edit_client_record_val_id(self, column_names):
        while True:
            val_id = input('Zadej id hodnoty pro změnu: ')
            if val_id.isnumeric():
                if int(val_id) not in range(1,len(column_names)):
                    print('Zadaná špatná hodnota id')
                    continue
                else:
                    return val_id

    def assign_new_insurance(self):
        '''Assignment of insurance to a client'''
        client_id = self._chck_client_id()
        type_insurance_id = self._chck_insurance()
        print('Datum počátku platnosti pojištění. Datum >= dnes:')
        start_date = self._chck_date(chck_today=True)
        print('Datum ukončení pojištění. Datum > dnes')
        end_date = self._chck_date(compare=True)
        data = [client_id, type_insurance_id, start_date, end_date]
        [print(i, end='\t') for i in data]
        check_values = input('\nJsou zané hodnoty správně? (A = potvrzení, Enter pro zrušení): ')
        if check_values == 'A':
            query = '''INSERT INTO klienti_smlouvy (
                                                    klient_id,
                                                    smlouva_id,
                                                    datum_zalozeni,
                                                    datum_ukonceni)
                        VALUES(?,?,?,?)'''
            self.db.execute(query, data)
            self.db.commit()
        else:
            print('Požadavek byl zrušen.')

    def get_all_clients_with_insurance(self):
        query = '''SELECT k.jmeno, k.prijmeni, s.nazev, ks.datum_zalozeni, ks.datum_ukonceni 
                    FROM klienti as k
                    JOIN klienti_smlouvy as ks ON   k.klienti_id =ks.klient_id
                    JOIN smlouvy as s ON s.smlouvy_id = ks.smlouva_id
                    ORDER BY prijmeni;'''
        result = self.db.get_values(query)
        self._print_returned_vals(result)

    def remove_client_insurence(self):
        pass

    def edit_insurance_of_client(self):
        pass



    def get_types_of_insurence_by_id(self, val):
        query = 'SELECT smlouvy_id, nazev FROM smlouvy WHERE smlouvy_id = ?'
        result = self.db.get_values(query, [val])
        self._print_returned_vals(result)

    @warning
    def remove_client(self):
        klient_id = input('Zadej id klienta pro smazání záznamu: ')
        if klient_id != '' and klient_id.isnumeric():
            klient_record = self.get_client_by_id(klient_id)
            if klient_record != None:
                print('Opravdu chcete smazat?: ')
                answer = input('Napiště A pro ano, nebo Enter pro zrušení: ')
                if answer == "A":
                    query = "DELETE FROM klienti WHERE klienti_id = ?"
                    self.db.execute(query, str(klient_id))
                    self.db.commit()
                    print('Záznam smazán!')
                    return True
                else:
                    print('Transakce zrušena.')
            else:
                print("Žádný záznam nevyhovuje zadanemu ID klienta.")

    def _get_col_names_klienti(self):
        query = "SELECT c.name FROM pragma_table_info('klienti') c"
        query_result = self.db.get_values(query)
        result = [i[0] for i in query_result]
        return result

    def _get_age_in_result(self, result):
        for i, j in enumerate(result):
            result[i] = list(result[i])
            result[i][3] = get_age(result[i][3])
        return result

    def _chck_date(self, date=None, chck_today=False, compare=False, lower=False, return_date=False):
        '''Checks the correct date format'''
        while True:
            if date == None:
                date = input('Zadej datum ve tvaru rok-měsíc-den: ')
            chck = chck_date_format(date)
            if chck != None:
                if chck_today:
                    today = get_today()
                    usr_time = to_datetime_format(date)
                    if lower:
                        time_dif = compare_time(today, usr_time, compare=True)
                        if time_dif < 0:
                            if return_date:
                                return date
                            print(f'{time_dif} dní.')
                            return True
                        else:
                            print('Datum musí být nižší bež je dnešní den.')
                            date = None
                            continue
                    if compare:
                        time_dif = compare_time(today, usr_time, compare=True)
                        if time_dif > 0:
                            print(f'{time_dif} dní.')
                            return date
                    if compare_time(today, usr_time):
                        return date
                    else:
                        print('Datum musí být větší nebo rovno dnešnímu datu!')
                        date = None
                        continue
                return date
            date = None

    def _insert_mobile_number(self):
        while True:
            number = input('Zadej telefoní číslo 6-9 čísel: ')
            if number.isnumeric() and 9 <= len(number) <= 12:
                return number
            else:
                continue

def test():
    admin = Admin('pojistovna.db')
    #admin.assign_new_insurance()       #OK
    #admin.get_types_of_insurence()      #OK
    admin.edit_client_record()          #OK
    #admin._chck_client_id()
    admin.add_new_client()
    #admin.get_all_clients()
    ##admin.get_client_detail()
    #admin.remove_client()
    admin.get_all_clients()
    admin.db.db_close()

#test()