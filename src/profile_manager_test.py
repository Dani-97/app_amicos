import unittest
from model import Model, User, LogInException

class SignupTestCase(unittest.TestCase):

    def test_correct_signup_and_login(self):
        model = Model()
        model.init_db()

        created_user = User("user1", "user1@app.com", "Usuario común")
        password = "1234"

        model.create_user(created_user.get_username(), 
                          created_user.get_email(),
                          created_user.get_role(),
                          password)
        retrieved_user = model.login_user(created_user.get_username(), password)
        self.assertEqual(created_user.get_username(), retrieved_user.get_username())
        self.assertEqual(created_user.get_email(), retrieved_user.get_email())
        self.assertEqual(created_user.get_role(), retrieved_user.get_role())

        model.remove_db_file()

    def test_incorrect_login(self):
        model = Model()
        model.init_db()

        created_user = User("user1", "user1@app.com", "Usuario común")
        correct_password = "1234"
        wrong_password = "123"
        model.create_user(created_user.get_username(), 
                          created_user.get_email(),
                          created_user.get_role(),
                          correct_password)
        with self.assertRaises(LogInException):
            model.login_user(created_user.get_username(), wrong_password)

        model.remove_db_file()

if __name__ == '__main__':
    unittest.main()