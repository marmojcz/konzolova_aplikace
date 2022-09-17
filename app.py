#!/usr/bin/env python3

from utils import cls
import accesses

DATABASE_NAME = 'pojistovna.db'
HEADER = f'{40 * "-"}\nEvidence pojištěných\n{40 * "-"}'
KONEC = "Konec aplikace"

def main_action():
    '''Úvodní obrazovka. Vyžadována akce uživatele.'''
    action = 0
    while action not in range(1,7):
        action = input(
        """Vyberte si akci:
        1 - Přidat nového pojištěného
        2 - Vypsat všechny pojištěné
        3 - Vyhledat pojištěného
        4 - Vymazat záznam(podle id_klienta)
        5 - Editovat záznam
        6 - Konec
        """
        )
        try:
            if action.isnumeric():
                cls()
                action = int(action)
        except ValueError:
            print("Zadána špatná hodnota.")
    return action

def main():
    '''Hlavní tělo hlavního programu'''
    cls()
    usr = accesses.Admin(DATABASE_NAME)
    while True:
        try:
            print(HEADER)
            action = main_action()
            if action == 1:
                usr.add_new_client()
            elif action == 2:
                usr.get_all_clients()
            elif action == 3:
                usr.get_client_by_name()
            elif action == 4:
                usr.remove_client()
            elif action == 5:
                usr.edit_client_record()
            elif action == 6:
                break
        except KeyboardInterrupt:
            break
        input('Pokračujte libovolnou klávesou...')
        cls()
    usr.db_close()
    print(KONEC)
    exit()

main()