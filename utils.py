#!/usr/bin/env python3
import hashlib
import datetime
from os import system as __system
from os import name as __name
from getpass import getpass

def cls() -> None:
    '''Clear console.'''
    __system('cls' if __name == 'nt' else 'clear')

def get_age(birthdate: str) -> int:
    '''It brings back the age. according to the specified date and the current date.
The format for inserting the date is datetime.date. (%Y-%m%-%d)'''
    birthdate = datetime.datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.date.today()
    one_or_zero = ((today.month, today.day) < (birthdate.month, birthdate.day))
    year_difference = today.year - birthdate.year
    age = year_difference - one_or_zero
    return age

def hash(passwd, salt) -> str:
    '''Return hash with salt'''
    return hashlib.sha256((passwd + salt).encode()).hexdigest()

def timestamp() -> str:
    '''Returns today's date string format.'''
    return datetime.date.strftime(datetime.date.today(), "%Y-%m-%d")

def get_today() -> datetime.date:
    '''Returns today's date datetime.date format.'''
    return datetime.date.today()

def to_datetime_format(date):
    '''returns the specified date in datetime format'''
    return datetime.datetime.strptime(date, "%Y-%m-%d")

def compare_two_times(first:str, second:str)->bool:
    'Compares two given times (format "YYYY-MM-DD") first < second'
    a = datetime.datetime.strptime(first, "%Y-%m-%d")
    b = datetime.datetime.strptime(second, "%Y-%m-%d")
    return a < b

def compare_time(today:datetime.date, usr_time:datetime, compare = False):
    '''It compares two dates. >= or - Returns bool or difference in days'''
    dt_today = datetime.datetime(today.year, today.month, today.day)
    if not compare:
        compare = usr_time >= dt_today
        return compare
    elif compare:
        return (usr_time - dt_today).days

def chck_date_format(chck_date):
    '''Checks for the correct data format. Returns it in the form Year Month(words) day'''
    try:
        chck_date = datetime.datetime.strptime(chck_date, "%Y-%m-%d")
        return  datetime.date.strftime(chck_date, "%Y %B %d")
    except ValueError:
        print('Zadaná špatný formát datumu')
        return None

def data_generator(data):
    '''Originally for the cur.executemany() handler'''
    # generátor pro vkládání do execute many
    for i in data:
        yield (i)

def warning(func):
    '''Decorator completely irrelevant'''
    def wrapper(*args):
        print()
        print(f'''{10*"!"}POZOR CHCETE SMAZAT ZÁZNAM KLIENTA{10*"!"}\n
              Tato akce vymaže i všechny smlouvy klienta.''')
        func(*args)
    return wrapper

def chck_emial(user_email = None):
    while True:
        print('Apliakce povoluje pouze celojmenné domény. Domény typu "moje_domena" nejsou podporovány.')
        user_email = input('Zadejte email: ')
        if '@' in user_email:
            if '.' in user_email.split('@')[-1]:
                return user_email
            else:
                print('Zadaný email není v požadovaném tvaru.')

def get_hash(salt):
    while True:
        passwd_1 = getpass('Zadejte heslo      (z bezpečnostních důvodů heslo nebude vypisováno): ')
        passwd_2 = getpass('Zadejte heslo znovu(z bezpečnostních důvodů heslo nebude vypisováno): ')
        if passwd_1 == passwd_2:
            return hash(passwd_1, salt)