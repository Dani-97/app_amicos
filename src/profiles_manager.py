import os
from passlib.hash import pbkdf2_sha256
import re
import sqlite3

from utils_exceptions import LogInException
from utils_exceptions import InvalidUsernameException
from utils_exceptions import InvalidEmailException
from utils_exceptions import InvalidPasswordException
from utils_exceptions import DuplicatedUserException
from utils_exceptions import UserDeletionException

class User:

    def __init__(self, username, email, role):
        self.username = username
        self.email = email
        self.role = role

    def get_username(self):
        return self.username

    def get_email(self):
        return self.email

    def get_role(self):
        return self.role 

class ProfilesManagerProvider:

    def __init__(self):
        self.current_user = None
        self.USERS_DB_PATH = "users.db"
        self.users_list = []
        self.notified_widgets_list = []

    def add_notified(self, notified_widget):
        self.notified_widgets_list.append(notified_widget)

    def __notify_widgets__(self):
        current_user = self.get_current_user()
        for widget in self.notified_widgets_list:
            widget.update_login(current_user)

    # async function
    def init_db(self):
        conn = sqlite3.connect(self.USERS_DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        email TEXT NOT NULL,
                        role TEXT NOT NULL,
                        password_hash TEXT NOT NULL,
                        is_logged_in BOOLEAN NOT NULL
                    )''')
        conn.commit()
        conn.close()

    def remove_db_file(self):
        os.remove(self.USERS_DB_PATH)

    def username_format_validator(self, username):
        format_validation = (len(username.strip())>=4) and (len(username.strip())<=12)
        format_validation = format_validation and (username.find(" ")==-1)

        return format_validation

    def email_format_validator(self, email):
        reg = r"^\S+@\S+\.\S+$"
        pattern = re.compile(reg)
        patt_match = re.search(pattern, email)

        return patt_match

    def password_format_validator(self, password):
        reg = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$#%])[A-Za-z\d@$#%]{6,12}$"
        pattern = re.compile(reg)
        patt_match = re.search(pattern, password)

        return patt_match

    # async function
    def get_user_by_username(self, username):
        conn = sqlite3.connect(self.USERS_DB_PATH)
        c = conn.cursor()
        c.execute("SELECT username, email, role, is_logged_in FROM users WHERE username=?", (username,))
        result = c.fetchone()

        if (result):
            return result
        
        return None

    # async function
    def create_user(self, username, email, role, password):
        is_username_format_correct = self.username_format_validator(username)
        is_email_format_correct = self.email_format_validator(email)
        is_password_format_correct = self.password_format_validator(password)

        if (not is_username_format_correct):
            raise InvalidUsernameException("nombre_usuario_no_valido")

        if (not is_email_format_correct):
            raise InvalidEmailException("email_no_valido")

        if (not is_password_format_correct):
            # La contraseña debe tener entre 6 y 12 caracteres, tener al menos un número, una mayúscula, una minúscula y un carácter especial de $, @, # ó %
            raise InvalidPasswordException("contrasena_no_valida")

        retrieved_user = self.get_user_by_username(username)
        if (retrieved_user is not None):
            raise DuplicatedUserException("usuario_duplicado")
        else:
            conn = sqlite3.connect(self.USERS_DB_PATH)
            c = conn.cursor()

            hashed = pbkdf2_sha256.hash(password)
            is_logged_in = False
            try:
                c.execute("INSERT INTO users (username, email, role, password_hash, is_logged_in) VALUES (?, ?, ?, ?, ?)", (username, email, role, hashed, is_logged_in))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False
            finally:
                conn.close()

    # async function
    def login_user(self, username, typed_password):
        conn = sqlite3.connect(self.USERS_DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()
        
        if (result):
            username, email, role, stored_password, is_logged_in = result
            if (pbkdf2_sha256.verify(typed_password, stored_password)):
                self.current_user = User(username, email, role)
                c.execute("UPDATE users SET is_logged_in=? WHERE username=?", (True, username,))
                conn.commit()
                conn.close()

                self.__notify_widgets__()

                return self.current_user

        conn.close()

        raise LogInException("The username or the password are incorrect")

    # async function
    def logout_current_user(self):
        conn = sqlite3.connect(self.USERS_DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE users SET is_logged_in=? WHERE username=?", (False, self.current_user.get_username(),))
        conn.commit()

        conn.close()

        self.current_user = None

        self.__notify_widgets__()

    # async function
    def delete_user(self, username, email):
        conn = sqlite3.connect(self.USERS_DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? and email=?", (username, email))
        result = c.fetchone()

        if (result):
            c.execute("DELETE FROM users WHERE username=?", (username,))
        else:
            conn.close()
            raise UserDeletionException("The email is not correct")

        conn.commit()
        conn.close()

        self.__notify_widgets__()

    # async function
    def get_current_user(self):
        conn = sqlite3.connect(self.USERS_DB_PATH)
        c = conn.cursor()
        c.execute("SELECT username, email, role, is_logged_in FROM users")
        result = c.fetchall()

        self.current_user = None
        for current_user in result:
            username, email, role, is_logged_in = current_user
            if (is_logged_in):
                self.current_user = User(username, email, role)                

        conn.close()

        return self.current_user