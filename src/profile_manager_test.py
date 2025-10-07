import unittest
from model import Model, User
from model import InvalidUsernameException, InvalidEmailException, InvalidPasswordException
from model import LogInException, UserDeletionException, DuplicatedUserException

class SignupTestCase(unittest.TestCase):

    # Creación de cuenta correcta.
    def test_cp1(self):
        model = Model()
        model.init_db()

        user1 = User("user1", "user1@app.com", "Usuario común")
        user2 = User("user2", "user2@app.com", "Logopeda")
        user3 = User("user3", "user3@app.com", "Cuidador")

        users_list = [user1, user2, user3]

        password = "aA12345678@"

        for user_aux in users_list:
            model.create_user(user_aux.get_username(), 
                            user_aux.get_email(),
                            user_aux.get_role(),
                            password)

        for user_aux in users_list:
            retrieved_user = model.login_user(user_aux.get_username(), password)
            self.assertEqual(user_aux.get_username(), retrieved_user.get_username())
            self.assertEqual(user_aux.get_email(), retrieved_user.get_email())
            self.assertEqual(user_aux.get_role(), retrieved_user.get_role())

        model.remove_db_file()

    # Inicio de sesión correcto.
    def test_cp2(self):
        model = Model()
        model.init_db()

        user1 = User("user1", "user1@app.com", "Usuario común")
        user2 = User("user2", "user2@app.com", "Logopeda")
        users_list = [user1, user2]

        password = "aA12345678@"

        for user_aux in users_list:
            model.create_user(user_aux.get_username(), 
                            user_aux.get_email(),
                            user_aux.get_role(),
                            password)

        for user_aux in users_list:
            _ = model.login_user(user_aux.get_username(), password)
            current_user = model.get_current_user()

            self.assertEqual(current_user.get_username(), user_aux.get_username())
            self.assertEqual(current_user.get_email(), user_aux.get_email())
            self.assertEqual(current_user.get_role(), user_aux.get_role())

        model.remove_db_file()

    # Eliminación de cuenta correcto.
    def test_cp3(self):
        model = Model()
        model.init_db()

        user1 = User("user1", "user1@app.com", "Usuario común")
        password = "aA12345678@"

        model.create_user(user1.get_username(), 
                        user1.get_email(),
                        user1.get_role(),
                        password)
        _ = model.login_user(user1.get_username(), password)
        current_user = model.get_current_user()

        self.assertEqual(current_user.get_username(), user1.get_username())
        self.assertEqual(current_user.get_email(), user1.get_email())
        self.assertEqual(current_user.get_role(), user1.get_role())

        model.delete_user(current_user.get_username(), current_user.get_email())

        with self.assertRaises(LogInException):
            _ = model.login_user(user1.get_username(), password)

        model.remove_db_file()

    # Cierre de sesión correcto.
    def test_cp4(self):
        model = Model()
        model.init_db()

        user1 = User("user1", "user1@app.com", "Usuario común")
        password = "aA12345678@"
        model.create_user(user1.get_username(), 
                        user1.get_email(),
                        user1.get_role(),
                        password)
        _ = model.login_user(user1.get_username(), password)

        current_user = model.get_current_user()

        self.assertEqual(current_user.get_username(), user1.get_username())
        self.assertEqual(current_user.get_email(), user1.get_email())
        self.assertEqual(current_user.get_role(), user1.get_role())

        model.logout_current_user()
        current_user = model.get_current_user()

        self.assertEqual(current_user, None)

        model.remove_db_file()

    # Creación de usuario: nombre con formato incorrecto.
    def test_cp1_1(self):
        model = Model()
        model.init_db()

        password = "aA12345678@"
        user1 = User("", "user1@app.com", "Usuario común")

        with self.assertRaises(InvalidUsernameException):
            model.create_user(user1.get_username(), 
                            user1.get_email(),
                            user1.get_role(),
                            password)

        user1 = User("Use", "user1@app.com", "Usuario común")

        with self.assertRaises(InvalidUsernameException):
            model.create_user(user1.get_username(), 
                            user1.get_email(),
                            user1.get_role(),
                            password)

        user1 = User("UserUserUserUser", "user1@app.com", "Usuario común")

        with self.assertRaises(InvalidUsernameException):
            model.create_user(user1.get_username(), 
                            user1.get_email(),
                            user1.get_role(),
                            password)

        user1 = User("U s e r s", "user1@app.com", "Usuario común")

        with self.assertRaises(InvalidUsernameException):
            model.create_user(user1.get_username(), 
                            user1.get_email(),
                            user1.get_role(),
                            password)

        model.remove_db_file()

    # Creación de usuario: usuario duplicado.
    def test_cp1_2(self):
        model = Model()
        model.init_db()

        user1 = User("testing_user", "user1@app.com", "Usuario común")
        user2 = User("testing_user", "user2@app.com", "Logopeda")
        correct_password = "aA12345678@"
        
        model.create_user(user1.get_username(), 
                    user1.get_email(),
                    user1.get_role(),
                    correct_password)

        with self.assertRaises(DuplicatedUserException):
            model.create_user(user2.get_username(), 
                        user2.get_email(),
                        user2.get_role(),
                        correct_password)

        model.remove_db_file()

    # Creación de usuario: email con formato incorrecto.
    def test_cp1_3(self):
        model = Model()
        model.init_db()

        user1 = User("testing_user", "user1app.com", "Usuario común")
        correct_password = "aA12345678@"

        with self.assertRaises(InvalidEmailException):
            model.create_user(user1.get_username(), 
                    user1.get_email(),
                    user1.get_role(),
                    correct_password)

        user1 = User("testing_user", "user1@app", "Usuario común")
        correct_password = "aA12345678@"

        with self.assertRaises(InvalidEmailException):
            model.create_user(user1.get_username(), 
                    user1.get_email(),
                    user1.get_role(),
                    correct_password)

        model.remove_db_file()

    # Creación de usuario: contraseña con formato incorrecto.
    def test_cp_1_4(self):
        model = Model()
        model.init_db()

        # Menos de 6 caracteres.
        user1 = User("testing_user", "user1@app.com", "Usuario común")
        correct_password = "aA1@"

        with self.assertRaises(InvalidPasswordException):
            model.create_user(user1.get_username(), 
                            user1.get_email(),
                            user1.get_role(),
                            correct_password)

        # Más de 12 caracteres.
        user1 = User("testing_user", "user1@app.com", "Usuario común")
        correct_password = "aA1234567890@"

        with self.assertRaises(InvalidPasswordException):
            model.create_user(user1.get_username(), 
                            user1.get_email(),
                            user1.get_role(),
                            correct_password)

        # No tiene, al menos, un número.
        user1 = User("testing_user", "user1@app.com", "Usuario común")
        correct_password = "aABCDEFG@"

        with self.assertRaises(InvalidPasswordException):
            model.create_user(user1.get_username(), 
                            user1.get_email(),
                            user1.get_role(),
                            correct_password)

        # No tiene, al menos, una mayúscula.
        user1 = User("testing_user", "user1@app.com", "Usuario común")
        correct_password = "aabcdefg@"

        with self.assertRaises(InvalidPasswordException):
            model.create_user(user1.get_username(), 
                            user1.get_email(),
                            user1.get_role(),
                            correct_password)

        # No tiene, al menos, una minúscula.
        user1 = User("testing_user", "user1@app.com", "Usuario común")
        correct_password = "AABCDEFG@"

        with self.assertRaises(InvalidPasswordException):
            model.create_user(user1.get_username(), 
                            user1.get_email(),
                            user1.get_role(),
                            correct_password)

        # No tiene, al menos, un carácter especial.
        user1 = User("testing_user", "user1@app.com", "Usuario común")
        correct_password = "aA12345678"

        with self.assertRaises(InvalidPasswordException):
            model.create_user(user1.get_username(), 
                            user1.get_email(),
                            user1.get_role(),
                            correct_password)

        model.remove_db_file()

    # Inicio de sesión: nombre de usuario incorrecto.
    def test_cp_2_1(self):
        model = Model()
        model.init_db()

        correct_username = "user1"
        wrong_username = "user2"
        created_user = User(correct_username, "user1@app.com", "Usuario común")
        correct_password = "aA12345678@"
        model.create_user(created_user.get_username(), 
                    created_user.get_email(),
                    created_user.get_role(),
                    correct_password)

        with self.assertRaises(LogInException):
            model.login_user(wrong_username, correct_password)

        model.remove_db_file()

    # Inicio de sesión: contraseña incorrecta.
    def test_cp_2_2(self):
        model = Model()
        model.init_db()

        created_user = User("user1", "user1@app.com", "Usuario común")
        correct_password = "aA12345678@"
        wrong_password = "123"
        model.create_user(created_user.get_username(), 
                          created_user.get_email(),
                          created_user.get_role(),
                          correct_password)

        with self.assertRaises(LogInException):
            model.login_user(created_user.get_username(), wrong_password)

        model.remove_db_file()

    # Inicio de sesión: usuario no logueado.
    def test_cp_2_3(self):
        model = Model()
        model.init_db()

        current_user = model.get_current_user()
        self.assertEqual(current_user, None)

        created_user = User("user1", "user1@app.com", "Usuario común")
        correct_password = "aA12345678@"
        model.create_user(created_user.get_username(), 
                    created_user.get_email(),
                    created_user.get_role(),
                    correct_password)

        current_user = model.get_current_user()
        self.assertEqual(current_user, None)

        model.remove_db_file()

    # Inicio de sesión: email incorrecto.
    def test_cp_3_1(self):
        model = Model()
        model.init_db()

        current_user = model.get_current_user()
        self.assertEqual(current_user, None)

        correct_email = "user1@app.com"
        incorrect_email = "user2@app.com"
        created_user = User("user1", "user1@app.com", "Usuario común")
        correct_password = "aA12345678@"
        model.create_user(created_user.get_username(), 
                    created_user.get_email(),
                    created_user.get_role(),
                    correct_password)

        model.login_user(created_user.get_username(), correct_password)

        with self.assertRaises(UserDeletionException):
            model.delete_user(created_user.get_username(), incorrect_email)

        model.remove_db_file()

if __name__ == '__main__':
    unittest.main()