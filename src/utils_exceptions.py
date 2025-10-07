class LogInException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidUsernameException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidEmailException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class InvalidPasswordException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class DuplicatedUserException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class UserDeletionException(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)