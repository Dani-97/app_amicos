from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.toolbar import MDTopAppBar
from kivy.core.text import LabelBase
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.image import AsyncImage
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon, MDLabel
from kivy.uix.widget import Widget
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDRaisedButton
from kivymd.uix.spinner import MDSpinner

from kivymd.uix.navigationdrawer import (
    MDNavigationLayout,
    MDNavigationDrawer
)

from kivy.metrics import dp, inch, mm

from kivy.clock import mainthread
import threading
import time

# --- Your custom imports ---
from utils_exceptions import (
    LogInException, InvalidUsernameException, InvalidEmailException,
    InvalidPasswordException, DuplicatedUserException, UserDeletionException
)

class AmicosApp(MDApp):

    def set_current_user(self, current_user):
        self.current_user = current_user

    def set_ui_assets_manager(self, ui_assets_manager):
        self.ui_assets_manager = ui_assets_manager

    def set_message_builder_provider(self, message_builder_provider):
        self.message_builder_provider = message_builder_provider

    def set_profiles_manager_provider(self, profiles_manager_provider):
        self.profiles_manager_provider = profiles_manager_provider

    def set_settings_provider(self, settings_provider):
        self.settings_provider = settings_provider

    def build(self):
        self.title = "App Amicos"
        self.icon = self.ui_assets_manager.get_resource("assets/logo.png")
        self.theme_cls.primary_palette = "BlueGray"
        self.theme_cls.theme_style = "Light"

        self.ui_assets_manager.set_language(self.settings_provider.get_current_language())

        LabelBase.register(name='Titulo', fn_regular=self.ui_assets_manager.get_resource('fonts/Orbitron-Regular.ttf'))
        LabelBase.register(name='Texto', fn_regular=self.ui_assets_manager.get_resource('fonts/FrancoisOne-Regular.ttf'))

        Builder.load_file("mainmenu.kv")
        Builder.load_file("mainwindow.kv")
        Builder.load_file("signupapp.kv")
        Builder.load_file("loginapp.kv")
        Builder.load_file("gridwindow.kv")
        Builder.load_file("tile.kv")

        # Main menu
        self.nav_layout = MDNavigationLayout()
        self.main_menu = MainMenu(self.current_user,
                                  self.ui_assets_manager,
                                  self.settings_provider,
                                  self.profiles_manager_provider, 
                                  orientation="vertical")
        self.main_menu.build()

        # Screens
        main_window = MainWindow(self.current_user,
                                 self.main_menu,
                                 self.ui_assets_manager,
                                 self.message_builder_provider,
                                 self.profiles_manager_provider,
                                 self.settings_provider,
                                 name="main_window")
        signup_screen = SignupScreen(self.ui_assets_manager,
                                     self.profiles_manager_provider,
                                     self.settings_provider,
                                     name="signup_screen")
        signup_screen.build()
        login_screen = LogInScreen(self.ui_assets_manager,
                                   self.profiles_manager_provider, 
                                   self.settings_provider,
                                   name="login_screen")
        login_screen.build()

        self.sm = MDScreenManager()
        self.sm.add_widget(signup_screen)
        self.sm.add_widget(login_screen)
        self.sm.add_widget(main_window)

        self.nav_layout.add_widget(self.sm)
        self.nav_layout.add_widget(self.main_menu)
        
        self.sm.current = "main_window" if self.current_user else "signup_screen"

        return self.nav_layout

class Tile(MDCard):

    def __init__(self, text, link, source, tile_type, tile_mode, bg_color, **kwargs):
        super().__init__(**kwargs)
        self.tile_associated_text = text
        self.tile_type = tile_type
        self.link = link
        self.md_bg_color = bg_color
        self.orientation = 'vertical'
        self.size_hint = (1.0, 1.0)
        self.radius = [15]

        self.ids.tile_image.source = source
        if (tile_mode=='text_and_pictogram'):
            self.ids.tile_label.text = text

class NormalTile(Tile):

    def __init__(self, text, link, source, tile_mode, **kwargs):
        bg_color = (0.16, 0.67, 0.71, 1)
        tile_type = "item"
        super().__init__(text, link, source, tile_type, tile_mode, bg_color, **kwargs)

class CategoryTile(Tile):

    def __init__(self, text, link, source, tile_mode, **kwargs):
        bg_color = (0.45, 0.43, 0.71, 1)
        tile_type = "category"
        super().__init__(text, link, source, tile_type, tile_mode, bg_color, **kwargs)

class GridWindow(MDBoxLayout):
    
    def __init__(self, parent_window, tab_id, **kwargs):
        super().__init__(**kwargs)
        self.tab_id = tab_id
        self.parent_window = parent_window

        self.grid = self.ids.grid_window_main_layout

    def set_ui_assets_manager(self, ui_assets_manager):
        self.ui_assets_manager = ui_assets_manager

    def set_content(self, words_with_images, tile_mode):
        self.words_with_images = words_with_images
        self.tile_mode = tile_mode

    def set_message_builder_provider(self, message_builder_provider):
        self.message_builder_provider = message_builder_provider

    def build(self):
        self.grid.rows = len(self.words_with_images)
        self.grid.cols = len(self.words_with_images[0])
        for row in self.words_with_images:
            for tile_type, word, picture, link in row:
                if (tile_type=="category"):
                    tile = CategoryTile(str(word),
                                        link,
                                        self.ui_assets_manager.get_resource(f'assets/{picture}'),
                                        self.tile_mode,
                                        on_release=self.on_tile_clicked)
                if (tile_type=="item"):
                    tile = NormalTile(str(word),
                                      link,
                                      self.ui_assets_manager.get_resource(f'assets/{picture}'),
                                      self.tile_mode,
                                      on_release=self.on_tile_clicked)
                self.grid.add_widget(tile)

        # self.add_widget(self.grid)

    def on_tile_clicked(self, instance):
        tile_type = instance.tile_type
        if (tile_type=="category"):
            tile_link = instance.link
            self.parent_window.swap_grid_window(tile_link)
        if (tile_type=="item"):
            tile_text = instance.tile_associated_text
            self.message_builder_provider.add_word_to_message(tile_text)
            self.parent_window.swap_grid_window(self.tab_id)

class LogInScreen(MDScreen):
    
    def __init__(self, ui_assets_manager, profiles_manager_provider, settings_provider, **kwargs):
        super().__init__(**kwargs)
        self.ui_assets_manager = ui_assets_manager
        self.profiles_manager_provider = profiles_manager_provider
        self.settings_provider = settings_provider
        self.settings_provider.add_notified(self)

        available_languages = self.settings_provider.get_available_languages_names()
        menu_items = [
            {
                "text": lang,
                "viewclass": "OneLineListItem",
                "on_release": lambda input_value=lang: self.on_click_language_option(input_value)
            } for lang in available_languages
        ]

        self.language_menu = MDDropdownMenu(
            caller=None,  # We'll assign the button later
            items=menu_items,
            width_mult=4
        )

    @mainthread
    def build(self):
        login_screen_title_text = self.ui_assets_manager.get_string("iniciar_sesion")
        self.ids.toolbar.title = login_screen_title_text
        self.ids.toolbar.right_action_items = [["translate", lambda x: self.on_click_but_language(x)]]

        username_header = self.ui_assets_manager.get_string("nombre_usuario")
        self.ids.username.hint_text = username_header

        password_header = self.ui_assets_manager.get_string("contrasena")
        self.ids.password.hint_text = password_header

        but_login_hint_text = self.ui_assets_manager.get_string("iniciar_sesion")
        self.ids.but_login.text = but_login_hint_text

        link_create_account_text = self.ui_assets_manager.get_string("link_a_crear_perfil")
        self.ids.link_create_account.text = link_create_account_text

    def update_language(self):
        self.build()

    def on_click_language_option(self, widget):
        # The KivyMD library, in this case, sends the widget as
        # a text.
        new_language_code = self.settings_provider.get_language_code_by_name(widget)
        self.settings_provider.change_current_language(new_language_code)

    def on_click_but_language(self, widget):
        self.language_menu.caller = widget
        self.language_menu.open()

    def go_to_signup_page(self):
        self.manager.current = 'signup_screen'

    @mainthread
    def go_to_main_window(self):
        self.manager.current = 'main_window'

    def validate_login(self):
        
        def __validate_login_aux__(login_screen, username, password):
            try:
                _ = login_screen.profiles_manager_provider.login_user(username, password)
                login_screen.__successful_login__()
            except LogInException:
                login_screen.__wrong_login__()

        self.login_spinner = MDSpinner(size_hint=(None, None),
                                       size=(dp(46), dp(46)),
                                       pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                       active=True)
        self.ids.but_login.disabled = True
        self.ids.link_create_account.disabled = True
        self.add_widget(self.login_spinner)

        username = self.ids.username.text
        password = self.ids.password.text
        runner_thread = threading.Thread(target=__validate_login_aux__, args=(self, username, password,))
        runner_thread.start()

    @mainthread
    def __successful_login__(self):
        self.login_spinner.active = False
        self.ids.but_login.disabled = False
        self.ids.link_create_account.disabled = False
        MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("inicio_sesion_correcto"))).open()
        self.ids.username.text = ""
        self.ids.password.text = ""
        self.go_to_main_window()

    @mainthread
    def __wrong_login__(self):
        self.login_spinner.active = False
        self.ids.but_login.disabled = False
        self.ids.link_create_account.disabled = False
        MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("inicio_sesion_incorrecto"))).open()

class SignupScreen(MDScreen):
    
    def __init__(self, ui_assets_manager, profiles_manager_provider, settings_provider, **kwargs):
        super().__init__(**kwargs)
        self.ui_assets_manager = ui_assets_manager
        self.profiles_manager_provider = profiles_manager_provider
        self.settings_provider = settings_provider
        self.settings_provider.add_notified(self)
        
        available_languages = self.settings_provider.get_available_languages_names()
        menu_items = [
            {
                "text": lang,
                "viewclass": "OneLineListItem",
                "on_release": lambda input_value=lang: self.on_click_language_option(input_value)
            } for lang in available_languages
        ]

        self.language_menu = MDDropdownMenu(
            caller=None,  # We'll assign the button later
            items=menu_items,
            width_mult=4
        )

    def build(self):
        signup_screen_title_text = self.ui_assets_manager.get_string("crear_cuenta")
        self.ids.toolbar.title = signup_screen_title_text
        self.ids.toolbar.right_action_items = [["translate", lambda x: self.on_click_but_language(x)]]

        username_header = self.ui_assets_manager.get_string("nombre_usuario")
        self.ids.username.hint_text = username_header

        role_header = self.ui_assets_manager.get_string("rol")
        self.ids.role.hint_text = role_header

        email_header = self.ui_assets_manager.get_string("email")
        self.ids.email.hint_text = email_header

        password_header = self.ui_assets_manager.get_string("contrasena")
        self.ids.password.hint_text = password_header

        but_create_account_text = self.ui_assets_manager.get_string("crear_cuenta")
        self.ids.but_create_account.text = but_create_account_text

        link_to_login = self.ui_assets_manager.get_string("link_a_inicio_sesion")
        self.ids.link_to_login.text = link_to_login

    def update_language(self):
        self.build()

    def on_click_language_option(self, widget):
        # The KivyMD library, in this case, sends the widget as
        # a text.
        new_language_code = self.settings_provider.get_language_code_by_name(widget)
        self.settings_provider.change_current_language(new_language_code)

    def on_click_but_language(self, widget):
        self.language_menu.caller = widget
        self.language_menu.open()

    def go_to_login_page(self):
        self.manager.current = 'login_screen'

    def go_to_main_window(self):
        self.manager.current = 'main_window'

    def execute_signup(self):

        def __execute_signup_aux__(signup_screen, username, email, role, password):
            try:
                self.profiles_manager_provider.create_user(username, email, role, password)
                _ = self.profiles_manager_provider.login_user(username, password)
                signup_screen.__successful_create_account__()
            except (InvalidUsernameException, InvalidEmailException,
                    InvalidPasswordException, DuplicatedUserException) as exception_id:
                signup_screen.__wrong_create_account__(exception_id.message)

        username = self.ids.username.text
        email = self.ids.email.text
        role = self.ids.role.text
        password = self.ids.password.text

        self.signup_spinner = MDSpinner(size_hint=(None, None),
                                       size=(dp(46), dp(46)),
                                       pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                       active=True)
        self.ids.but_create_account.disabled = True
        self.ids.link_to_login.disabled = True
        self.add_widget(self.signup_spinner)

        runner_thread = threading.Thread(target=__execute_signup_aux__, args=(self, username, email, role, password,))
        runner_thread.start()

    @mainthread
    def __successful_create_account__(self):
        MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("crear_cuenta_correcto"))).open()
        self.ids.username.text = ""
        self.ids.email.text = ""
        self.ids.role.text = ""
        self.ids.password.text = ""

        self.ids.but_create_account.disabled = False
        self.ids.link_to_login.disabled = False
        self.signup_spinner.active = False

        self.go_to_main_window()

    @mainthread
    def __wrong_create_account__(self, error_message):
        MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string(error_message))).open()

        self.ids.but_create_account.disabled = False
        self.ids.link_to_login.disabled = False
        self.signup_spinner.active = False

class MainMenu(MDNavigationDrawer):

    def __init__(self, current_user, ui_assets_manager, settings_provider, profiles_manager_provider, **kwargs):
        super().__init__(kwargs)
        self.ui_assets_manager = ui_assets_manager
        self.settings_provider = settings_provider
        self.settings_provider.add_notified(self)
        self.profiles_manager_provider = profiles_manager_provider
        self.profiles_manager_provider.add_notified(self)
        self.current_user = current_user

    def update_language(self):
        self.ui_assets_manager.set_language(self.settings_provider.get_current_language())
        but_label = self.ui_assets_manager.get_string('eliminar_cuenta')
        self.ids.but_delete_account.text = but_label

    def update_login(self, current_user):
        self.current_user = current_user
        self.ids.username_row_label.text = ""
        self.ids.email_row_label.text = ""
        if (self.current_user is not None):
            self.ids.username_row_label.text = self.current_user.get_username()
            self.ids.email_row_label.text = self.current_user.get_email()

    def build(self):
        self.ids.but_delete_account.text = self.ui_assets_manager.get_string('eliminar_cuenta')
        current_username = ""
        current_user_email = ""
        if (self.current_user!=None):
            current_username = self.current_user.get_username()
            current_user_email = self.current_user.get_email()

        self.ids.username_row_label.text = current_username
        self.ids.email_row_label.text = current_user_email

    def on_click_but_delete_account(self, widget):
        delete_account_dialog = DeleteAccountDialog(self,
                                                    self.ui_assets_manager,
                                                    self.profiles_manager_provider)
        delete_account_dialog.show_delete_dialog(widget)

    def open_menu(self):
        self.set_state('open')

    def close_menu(self):
        self.set_state('close')

    def on_click_but_close_session(self, widget):

        def __logout_current_user_aux__(main_menu):
            self.profiles_manager_provider.logout_current_user()     
            main_menu.__successful_logout__()    

        runner_thread = threading.Thread(target=__logout_current_user_aux__, args=(self,))
        runner_thread.start()

        self.logout_spinner = MDSpinner(size_hint=(None, None),
                            size=(dp(46), dp(46)),
                            pos_hint={'center_x': 0.5, 'center_y': 0.5},
                            active=True)
        self.add_widget(self.logout_spinner)

    @mainthread
    def __successful_logout__(self):
        self.logout_spinner.active = False
        self.close_menu()

class DeleteAccountDialog(MDBoxLayout):

    def __init__(self, main_menu, ui_assets_manager, profiles_manager_provider, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_y = None
        self.height = dp(120)

        self.main_menu = main_menu
        self.ui_assets_manager = ui_assets_manager
        self.profiles_manager_provider = profiles_manager_provider
        deletion_warning = self.ui_assets_manager.get_string("aviso_eliminacion")
        self.dialog_label = MDLabel(text=deletion_warning) 

        self.email_field = MDTextField()
        self.add_widget(self.dialog_label)
        self.add_widget(self.email_field)

    def show_delete_dialog(self, widget):
        self.delete_dialog = MDDialog(
            title=self.ui_assets_manager.get_string("confirmar_eliminacion"),
            type="custom",
            content_cls=self,
            buttons=[
                MDFlatButton(
                    text=self.ui_assets_manager.get_string("cancelar"),
                    on_release=lambda x: self.delete_dialog.dismiss()
                ),
                MDRaisedButton(
                    text=self.ui_assets_manager.get_string("eliminar"),
                    md_bg_color=(1, 0, 0, 1),
                    on_release=lambda x: self.confirm_account_deletion(x)
                ),
            ],
        )
        self.delete_dialog.open()

    def confirm_account_deletion(self, widget):

        def __delete_account_aux__(delete_account_dialog, typed_email):
            try:
                current_username = self.profiles_manager_provider.get_current_user().get_username()
                self.profiles_manager_provider.delete_user(current_username, typed_email)
                delete_account_dialog.__successful_delete_user__()
            except UserDeletionException:
                delete_account_dialog.__wrong_delete_user__()

        typed_email = self.email_field.text
        runner_thread = threading.Thread(target=__delete_account_aux__, args=(self, typed_email,))
        runner_thread.start()

        self.delete_user_spinner = MDSpinner(size_hint=(None, None),
                                             size=(dp(46), dp(46)),
                                             pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                             active=True)
        self.add_widget(self.delete_user_spinner)

    @mainthread
    def __successful_delete_user__(self):
        self.delete_user_spinner.active = False
        self.delete_dialog.dismiss()
        self.main_menu.close_menu()
        MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("confirmacion_eliminacion_cuenta"))).open()

    @mainthread
    def __wrong_delete_user__(self):
        self.delete_user_spinner.active = False
        self.delete_dialog.dismiss()
        self.main_menu.close_menu()
        MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("eliminar_cuenta_email_incorrecto"))).open()

class MainWindow(MDScreen):

    def __init__(self,
                 current_user,
                 main_menu,
                 ui_assets_manager,
                 message_builder_provider,
                 profiles_manager_provider,
                 settings_provider,
                 **kwargs):
        super().__init__(**kwargs)
        self.main_menu = main_menu
        self.ui_assets_manager = ui_assets_manager
        self.message_builder_provider = message_builder_provider
        self.message_builder_provider.add_notified(self)
        self.profiles_manager_provider = profiles_manager_provider
        self.profiles_manager_provider.add_notified(self)
        self.settings_provider = settings_provider
        self.settings_provider.add_notified(self)
        self.dialog = None
        self.current_user = current_user

        self.ids.top_bar.left_action_items = [["menu", lambda x: self.on_click_main_menu_dots(x)],
                                              ["eye", lambda x: self.on_click_but_tile_mode(x)]]
        self.ids.top_bar.right_action_items = [["translate", lambda x: self.on_click_but_language(x)]]
        self.ids.top_bar.title = self.ui_assets_manager.get_string('titulo_app')

        # --- Language selection dropdown ---
        available_languages = self.settings_provider.get_available_languages_names()
        menu_items = [
            {
                "text": lang,
                "viewclass": "OneLineListItem",
                "on_release": lambda input_value=lang: self.on_click_language_option(input_value)
            } for lang in available_languages
        ]
        self.language_menu = MDDropdownMenu(
            caller=None,  # We'll assign the button later
            items=menu_items,
            width_mult=4
        )

        self.build()

    @mainthread
    def go_to_login_page(self):
        self.manager.current = "login_screen"

    def build(self):
        self.ids.grid_window_layout.clear_widgets()
        self.current_username = self.current_user.get_username() if self.current_user else ""

        # # --- GRID SETUP ---
        self.grids_content = {}
        self.build_grid_content()

        self.grid_window = None
        self.swap_grid_window('main_window')

    # --- GRID & LANGUAGE LOGIC ---
    def build_grid_content(self):
        language = self.settings_provider.get_current_language()
        self.grids_content = self.ui_assets_manager.load_grids(language)

    def update_message(self):
        message = self.message_builder_provider.get_current_message()
        message_str = " ".join(message)

        self.ids.tf_user_aac_message.text = message_str

    def update_language(self):
        self.message_builder_provider.clear_message()
        self.build()

    def update_login(self, current_user):
        if (current_user is None):
            self.go_to_login_page()

    def swap_grid_window(self, tab_id):
        if self.grid_window:
            self.ids.grid_window_layout.remove_widget(self.grid_window)

        self.grid_window = GridWindow(self, 
                                      tab_id)
        self.grid_window.set_ui_assets_manager(self.ui_assets_manager)
        self.grid_window.set_content(
            self.grids_content[tab_id],
            self.settings_provider.get_current_tile_mode()
        )
        self.grid_window.set_message_builder_provider(self.message_builder_provider)
        self.grid_window.build()

        self.ids.grid_window_layout.add_widget(self.grid_window)

    # --- BUTTON CALLBACKS ---
    def on_click_main_menu_dots(self, widget):
        self.main_menu.open_menu()

    def on_click_but_tile_mode(self, widget):
        self.message_builder_provider.clear_message()
        available_tile_modes = self.settings_provider.get_available_tile_modes()
        current_tile_mode = self.settings_provider.get_current_tile_mode()

        for idx, tile_mode_aux in enumerate(available_tile_modes):
            if (tile_mode_aux==current_tile_mode):
                new_idx = (idx+1)%(len(available_tile_modes))

        self.settings_provider.change_current_tile_mode(available_tile_modes[new_idx])

    def on_click_but_language(self, widget):
        self.language_menu.caller = widget
        self.language_menu.open()

    def on_click_but_profile(self, widget):
        MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("no_disponible"))).open()

    def on_click_but_play_speech(self, widget):
        MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("no_disponible"))).open()

    def on_click_language_option(self, widget):
        # The KivyMD library, in this case, sends the widget as
        # a text.
        new_language_code = self.settings_provider.get_language_code_by_name(widget)
        self.settings_provider.change_current_language(new_language_code)

    def on_click_but_delete_last_word(self, widget):
        self.message_builder_provider.remove_last_word_from_message()

    def on_click_but_clear_message(self, widget):
        self.message_builder_provider.clear_message()
