#!/admin/bin/env python3

from utils import cls
import accesses

DATABASE_NAME = 'pojistovna.db'
HEADER = f'{40 * "-"}\nEvidence pojištěných\n{40 * "-"}'
KONEC = "Konec aplikace"


def main_action():
    '''Úvodní obrazovka. Vyžadována akce uživatele.'''
    action = None
    while None == action not in range(0, 10):
        action = input(
        """
        Vyberte si akci:
        0 - Konec
        1 - Přidat nového pojištěného
        2 - Vypsat všechny klienty
        3 - Vyhledat pojištěného
        4 - Vymazat klienta(podle id_klienta)
        5 - Editovat záznam
        6 - Přiřadit pojištění ke klientovi
        7 - Výpis všech klientů se s pojištěním
        8 - Odebrání pojištění klienta
        9 - Úprava pojištění klienta
        10 - Vypiš typy pojištění
        """
        )
        try:
            if action.isnumeric():
                cls()
                action = int(action)
        except ValueError:
            print("Zadána špatná hodnota.")
    return action


def main_app():
    '''Tělo akcí administrátora'''
    cls()
    admin = accesses.Admin(DATABASE_NAME)
    while True:
        try:
            print(HEADER)
            action = main_action()
            if action == 1:
                #vytvořit nového klienta------------------------------OK
                admin.add_new_client()
            elif action == 2:
                #výpis všech klientů----------------------------------OK
                admin.get_all_clients()
            elif action == 3:
                #vyhledání klient apodle jména a příjmení-------------OK
                admin.get_client_by_name()
            elif action == 4:
                #odstranění klienta i s pojištěním--------------------OK
                admin.remove_client()
            elif action == 5:
                #úprava záznamu klienta-------------------------------OK
                admin.edit_client_record()
            elif action == 6:
                #přiřadit pojištění ke klientovi----------------------OK
                admin.assign_new_insurance()
            elif action == 7:
                #výpis všech klientů kteří mají nějaké pojištění------OK
                admin.get_all_clients_with_insurance()
            elif action == 8:
                #odebrání klientova pojištění-------------------------OK
                admin.remmove_client_insurance()
            elif action == 9:
                #úprava pojištění klienta-----------------------------OK
                admin.edit_client_insurance()
            elif action == 10:
                #výpis typů pojištění---------------------------------OK
                admin.get_types_of_insurance()
            elif action == 0:
                break
        except KeyboardInterrupt:
            break
        input('Pokračujte libovolnou klávesou...')
        cls()
    admin.db_close()
    print(KONEC)
    exit()