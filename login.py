'''The module is designed to verify login credentials.
Returns the user ID and its credentials. 0 = user, 1 = administrator.
'''

from getpass import getpass as _getpass
from utils import hash as _hash

class Login:
    from accesses import Admin as __admin

    def __init__(self, db_name) -> None:
        self.db_name = db_name
        self.email = self.__set_user
        self._passwd = self.__set_passwd()
        self.__get_id = self.__get_auth() #salt
        self.permissions = self.__get_permissions
        if self.permissions == 1:
            pass #admin_actions(user_id)
        elif self.permissions == 0:
            pass #user_actions(user_id)

    def __str__(self) -> str:
        return f'Uživatel ID {self.email}'

    def __repr__(self) -> str:
        return f'{self.email}'

    def __get_auth(self):
        '''Try to check user_email info'''
        while True:
            db = self.__admin(self.db_name)
            chckemail = db._chck_email_exists(self.email)
            if not chckemail:
                print('Zadáno špatné ID.')
                self.email = self.__set_user
                self._passwd = self.__set_passwd()
                continue
            chck_passwd = db._chck_auth(self.email, self._passwd)
            db.db_close()
            return chck_passwd

    @property
    def __get_permissions(self):
        return self.__get_id[0][2]

    def __set_passwd(self):
        #Returns a password hash for verification.
        return _hash(_getpass("Heslo: "), ''.join(self.email))

    @property
    def __set_user(self):
        jmeno = input('Zadej přihlašovací jméno(ID): ')
        return jmeno