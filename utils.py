#!/usr/bin/env python3
import hashlib
from datetime import date, datetime
from os import listdir as __listdir
from os import system as __system
from os import name as __name

def cls()->None:
    '''Clear console.'''
    __system('cls' if __name =='nt' else 'clear')

def get_age(birthdate:str) -> int:
    '''It brings back the age. according to the specified date and the current date.
The format for inserting the date is datetime.date. (%Y-%m%-%d)'''
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    today = date.today()
    one_or_zero = ((today.month, today.day) < (birthdate.month, birthdate.day))
    year_difference = today.year - birthdate.year
    age = year_difference - one_or_zero
    return age

def hash(passwd, salt)->str:
    '''Return hash with salt'''
    return hashlib.sha256((passwd + salt).encode()).hexdigest()

def timestamp() -> str:
    '''Returns today's date'''
    return date.strftime(date.today(), "%Y-%m-%d")

def check_date(chck_date):
    chck_date = datetime.strptime(chck_date, "%Y-%m-%d")
    return f'Váš datum narození {date.strftime(chck_date, "%Y %B %d")}'

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

#cls()
#print(get_age('1987-7-9'))
#print(timestamp())
#print(hash("mojeheslo","uzivatel"))