import os
from passlib.hash import pbkdf2_sha256
import sqlite3

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

class LogInException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Model:

    def __init__(self):
        self.DB_PATH = "users.db"
        self.users_list = []
        self.current_user = None

    def init_db(self):
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY,
                        email TEXT NOT NULL,
                        role TEXT NOT NULL,
                        password_hash TEXT NOT NULL
                    )''')
        conn.commit()
        conn.close()

    def remove_db_file(self):
        os.remove(self.DB_PATH)

    def create_user(self, username, email, role, password):
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        hashed = pbkdf2_sha256.hash(password)
        try:
            c.execute("INSERT INTO users (username, email, role, password_hash) VALUES (?, ?, ?, ?)", (username, email, role, hashed))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()

    def login_user(self, username, typed_password):
        conn = sqlite3.connect(self.DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        result = c.fetchone()
        conn.close()
        if (result):
            username, email, role, stored_password = result
            if (pbkdf2_sha256.verify(typed_password, stored_password)):
                self.current_user = User(username, email, role)
                
                return self.current_user

        raise LogInException("The username or the password are incorrect")

    def get_current_user(self):
        return self.current_user
