#!/usr/bin/env python3
import hashlib
import datetime
from os import listdir as __listdir
from os import system as __system
from os import name as __name


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
    '''Returns today's date'''
    return datetime.date.strftime(datetime.date.today(), "%Y-%m-%d")

def get_today() -> datetime.date:
    return datetime.date.today()

def to_datetime_format(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d")

def compare_time(today:datetime.date, usr_time:datetime, compare = False):
    dt_today = datetime.datetime(today.year, today.month, today.day)
    if not compare:
        compare = usr_time >= dt_today
        return compare
    elif compare:
        return (usr_time - dt_today).days

def chck_date_format(chck_date):
    try:
        chck_date = datetime.datetime.strptime(chck_date, "%Y-%m-%d")
        return  datetime.date.strftime(chck_date, "%Y %B %d")
    except ValueError:
        print('Zadaná špatný formát datumu')
        return None


def data_generator(self, data):
    # generátor pro vkládání do execute many
    for i in data:
        yield (i)


def warning(func):
    def wrapper(*args):
        print()
        print(f'{10*"!"}POZOR CHCETE SMAZAT ZÁZNAM KLIENTA{10*"!"}')
        func(*args)
    return wrapper

# cls()
# print(get_age('1987-7-9'))
# print(timestamp())
# print(hash("mojeheslo","uzivatel"))
