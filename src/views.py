from kivy.app import App
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from model import Model
from model import LogInException
from model import InvalidUsernameException
from model import InvalidEmailException
from model import InvalidPasswordException
from model import DuplicatedUserException

class AmicosApp(App):

    def set_model(self, model):
        self.model = model

    """
    Clase principal de la aplicación, se encarga de la inicialización
    Es la encargada de iniciar la aplicación y construirla.    
    """
    def build(self):
        Builder.load_file("loginapp.kv")
        Builder.load_file("signupapp.kv")

        self.sm = ScreenManager()
        self.sm.add_widget(SignupScreen(self.model, name="signup"))
        self.sm.add_widget(LogInScreen(self.model, name="login"))

        return self.sm

class LogInScreen(Screen):

    def __init__(self, model, **kwargs):
        super(LogInScreen, self).__init__(**kwargs)
        self.model = model

    def go_to_signup_page(self):
        self.manager.current = 'signup'  # Switch to the login screen

    def build(self):
        pass

    def validate_login(self):
        username = self.ids.username.text
        password = self.ids.password.text

        try:
            user = self.model.login_user(username, password)
            self.ids.message.text = f"[color=00ff00]Inicio de sesión correcto[/color]"
        except LogInException:
            self.ids.message.text = "[color=ff0000]Nombre de usuario o contraseña incorrectos[/color]"

class SignupScreen(Screen):

    def __init__(self, model, **kwargs):
        super(SignupScreen, self).__init__(**kwargs)
        Window.size = (2048, 1080)
        self.model = model

    def go_to_login_page(self):
        self.manager.current = 'login'  # Switch to the login screen

    def execute_signup(self):        
        username = self.ids.username.text
        email = self.ids.email.text
        role = self.ids.role.text
        password = self.ids.password.text

        try: 
            self.model.create_user(username, email, role, password)
            self.ids.message.text = f"[color=00ff00]Cuenta creada correctamente[/color]"
            self.go_to_login_page()
        except InvalidUsernameException as except_obj:
            self.ids.message.text = f"[color=ff0000]{except_obj}[/color]"
        except InvalidEmailException as except_obj:
            self.ids.message.text = f"[color=ff0000]{except_obj}[/color]"
        except InvalidPasswordException as except_obj:
            self.ids.message.text = f"[color=ff0000]{except_obj}[/color]"
        except DuplicatedUserException as except_obj:
            self.ids.message.text = f"[color=ff0000]{except_obj}[/color]"