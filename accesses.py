#!/usr/bin/env python3

from webbrowser import get
from database import Database as db
from utils import *

class User:
    '''The class is intended for user access to data.'''
    def __init__(self, db_file:str) -> None:
        self.db = db(db_file)
        self.insurance_offered = self._insurance_offered()

    def __str__(self) -> str:
        return 'User id ...'

    def __repr__(self) -> str:
        return 'User id...'

    def get_my_info(self):
        '''The method should return information associated with the
            instance and its link in tables(Client info, detail of valid contracts).'''
        self.id
        query = ''' SELECT jmeno, prijmeni, datum_narozeni, telefon
                    FROM klienti
                    WHERE klienti_id = ?'''

    def db_close(self)-> None:
        '''Closes the connection to the database.'''
        self.db.db_close()

    def _chck_insurance_id(self)-> int:
        '''Checks whether there is an id of the insurance offered.'''
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
        '''Checks the existence of the id_client in the database.'''
        while True:
            client_id = input('Zadejte id klienta: ')
            if client_id.isnumeric():
                check = self.get_client_by_id(client_id)
                if check != None:
                    return client_id
            else:
                print('Hodnota muí být číslo!')
                continue

    def get_types_of_insurance(self)-> list:
        '''It prints the names of the provided insurances into the terminal'''
        query = 'SELECT smlouvy_id, nazev FROM smlouvy'
        result = self.db.get_values(query)
        self._print_returned_vals(result)
        return result

    def _print_returned_vals(self, result:list)-> print:
        [print('\t   \t   '.join(map(str, i))) for i in result]

class Admin(User):
    '''
    The class provides administration of the insurance company database.
    '''

    def __init__(self, db_file) -> None:
        super().__init__(db_file)

    def __str__(self) -> str:
        return f'Admin pro {self.db}'

    def __repr__(self) -> str:
        return f'Admin pro {self.db}'

    def add_new_client(self)->print:
        '''Adds a new client to the database.'''
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

    def get_all_clients(self)->list:
        '''Returns a list of all records in the clients table.'''
        query = '''SELECT * FROM klienti'''
        result = self.db.get_values(query)
        result = self._get_age_in_result(result)
        self._print_returned_vals(result)
        return result

    def get_client_by_name(self)-> list:
        '''Returns all data from the table klienti for a specific client by
        first and last name. '''
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

    def get_client_by_id(self, id:str, print_val=False)->list:
        '''Returns all data from the clients table according to the client id.'''
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

    def get_my_info(self)->str:
        '''The method should return information associated with
            the instance and its link in tables.'''
        return 'Jsi administrátor pojišťovny a nemáš účet.'

    def edit_client_record(self)->None:
        '''Editing a client record.'''
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

    def _edit_client_record_value(self, val_id:str)->str:
        '''Additional function for Edit client record - get values'''
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

    def _edit_client_record_val_id(self, column_names:list)->str:
        '''Additional function for Edit client record. - get id for table'''
        while True:
            val_id = input('Zadej id hodnoty pro změnu: ')
            if val_id.isnumeric():
                if int(val_id) not in range(1,len(column_names)):
                    print('Zadaná špatná hodnota id')
                    continue
                else:
                    return val_id

    def assign_new_insurance(self)->print:
        '''Assignment of insurance to a client'''
        client_id = self._chck_client_id()
        self.get_client_by_id(client_id,print_val=True)
        [print(i[0],i[1]) for i in self.insurance_offered.items()]
        type_insurance_id = self._chck_insurance_id()
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

    def get_all_clients_with_insurance(self)->print:
        '''It prints all clients with insurance to the terminal.'''
        query = '''SELECT k.klienti_id, k.jmeno, k.prijmeni, s.nazev, ks.datum_zalozeni, ks.datum_ukonceni
                    FROM klienti as k
                    JOIN klienti_smlouvy as ks ON   k.klienti_id =ks.klient_id
                    JOIN smlouvy as s ON s.smlouvy_id = ks.smlouva_id
                    ORDER BY prijmeni;'''
        result = self.db.get_values(query)
        self._print_returned_vals(result)

    def get_client_with_contracts(self, print_val=False):
        client_id = self._chck_client_id()
        get_client_records = self.get_client_by_id(client_id, print_val=print_val)
        get_client_contracts = self.get_client_contracts(client_id, print_vals= print_val)
        return (client_id, get_client_records, get_client_contracts)

    #decorator for editing contracts
    def actions_client_insurance(func):
        '''Decorator for editing or deleting contracts assigned to clients'''
        def wrapper(self):
            values = self.get_client_with_contracts(print_val=True)
            client_id = values[0]
            get_client_contracts = values[2]
            if not None in values:
                ins_ids = [i[0] for i in get_client_contracts]
                insurance_id = input('Zadej id smlouvy: ')
                if insurance_id.isnumeric() and int(insurance_id) in ins_ids:
                    check_values = input('\nChcete provést změny?(A = potvrzení, Enter pro zrušení): ')
                    if check_values == 'A':
                        func(self, client_id, insurance_id)
                    else:
                        print('Akce zrušena.')
                else:
                    print('Id smlouvy nevyhovuje.')
        return wrapper

    @actions_client_insurance
    def remmove_client_insurance(self, client_id, insurance_id ):
        '''Removes the insurance policy from the client's list of contracts'''
        query = 'DELETE FROM klienti_smlouvy WHERE klient_id = ? AND klienti_smlouvy_id = ?'
        self.db.execute(query, [client_id, insurance_id])
        self.db.commit()

    @actions_client_insurance
    def edit_client_insurance(self, client_id, insurance_id):
        '''The method edits insurance dates. Start or end of insurance. To change the
            insurance to another type, you must create the insurance again.'''
        contracts = self.get_client_contracts(id=client_id)
        for i in contracts:
            if i[0] == int(insurance_id):
                [print(j, end='\t') for j in i]
        print('\nZadej datum založení.')
        start_date = self._chck_date(chck_today=True)
        print('Zadej datum ukončení.')
        while True:
            end_date = self._chck_date(compare=True)
            if compare_two_times(start_date, end_date):
                break
            else:
                print('Datum ukončení musí být větší než datum založení.')
        query = '''UPDATE klienti_smlouvy SET datum_zalozeni = ? , datum_ukonceni = ?
                    WHERE klienti_smlouvy_id = ?;'''
        self.db.execute(query, [start_date, end_date, insurance_id])
        self.db.commit()

    def get_client_contracts(self, id=None, print_vals = False):
        if id == None:
            id = self._chck_client_id()
        query_contracts = '''SELECT ks.klienti_smlouvy_id, s.nazev, ks.datum_zalozeni, ks.datum_ukonceni
                            FROM klienti_smlouvy as ks
                            JOIN smlouvy as s ON s.smlouvy_id = ks.smlouva_id
                            WHERE ks.klient_id = ?;'''
        contracts = self.db.get_values(query_contracts, [id])
        if contracts == []:
            print('Zadaný klient nemá žádná pojištění.')
            return None
        if print_vals:
            self._print_returned_vals(contracts)
        return contracts



    def get_types_of_insurance_by_id(self, val:str)->print:
        '''Prints the names of the offered insurances into the terminal according to the id'''
        query = 'SELECT smlouvy_id, nazev FROM smlouvy WHERE smlouvy_id = ?'
        result = self.db.get_values(query, [val])
        self._print_returned_vals(result)

    @warning
    def remove_client(self)->bool:
        '''Removes the user from the records.
            Along with the client record, contracts from
            the clients_contracts table are deleted.'''
        klient_id = input('Zadej id klienta pro smazání záznamu: ')
        if klient_id != '' and klient_id.isnumeric():
            klient_record = self.get_client_by_id(klient_id, print_val=True)
            if klient_record != None:
                self.get_client_contracts(klient_id, print_vals=True)
                print('Opravdu chcete smazat?: ')
                answer = input('Napiště A pro ano, nebo Enter pro zrušení: ')
                if answer == "A":
                    query = "DELETE FROM klienti WHERE klienti_id = ?"
                    self.db.execute(query, [klient_id])
                    self.db.commit()
                    print('Záznam smazán!')
                    return True
                else:
                    print('Transakce zrušena.')
            else:
                print("Žádný záznam nevyhovuje zadanemu ID klienta.")

    def _get_col_names_klienti(self)->list:
        '''Gets the column names in the clients table'''
        query = "SELECT c.name FROM pragma_table_info('klienti') c"
        query_result = self.db.get_values(query)
        result = [i[0] for i in query_result]
        return result

    def _get_age_in_result(self, result:list)->list:
        '''Method for obtaining age. Uses a feature in utils.'''
        for i, j in enumerate(result):
            result[i] = list(result[i])
            result[i][3] = get_age(result[i][3])
        return result

    def _chck_date(self, date=None, chck_today=False, compare=False, lower=False, return_date=False):
        '''Method for verifying the correctness of the specified date. Uses functions from utils.
            compare = compares if the given date is higher than today's date.
            lower = like compare but keeps track of the lower date value
            return_date = u lower returns the date'''
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

    def _insert_mobile_number(self)->str:
        '''Method for verifying the correctness of the entered phone number.'''
        while True:
            number = input('Zadej telefoní číslo 6-9 čísel: ')
            if number.isnumeric() and 9 <= len(number) <= 12:
                return number
            else:
                continue

def test():
    '''Service function for testing'''
    admin = Admin('pojistovna.db')

    admin.db.db_close()

#test()