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

from kivymd.uix.navigationdrawer import (
    MDNavigationLayout,
    MDNavigationDrawer
)

from kivy.metrics import dp

# --- Your custom imports ---
from utils_exceptions import (
    LogInException, InvalidUsernameException, InvalidEmailException,
    InvalidPasswordException, DuplicatedUserException, UserDeletionException
)

class AmicosApp(MDApp):
    
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

        LabelBase.register(name='Titulo', fn_regular=self.ui_assets_manager.get_resource('fonts/Orbitron-Regular.ttf'))
        LabelBase.register(name='Texto', fn_regular=self.ui_assets_manager.get_resource('fonts/FrancoisOne-Regular.ttf'))

        Builder.load_file("signupapp.kv")
        Builder.load_file("loginapp.kv")
        Builder.load_file("tile.kv")

        self.nav_layout = MDNavigationLayout()
        self.main_menu = MainMenu(self.ui_assets_manager,
                                  self.profiles_manager_provider, 
                                  orientation="vertical")
        self.main_menu.build()

        # Screens
        main_window = MainWindow(
            self.main_menu,
            self.ui_assets_manager,
            self.message_builder_provider,
            self.profiles_manager_provider,
            self.settings_provider,
            name="main_window"
        )
        signup_screen = SignupScreen(self.ui_assets_manager,
                                     self.profiles_manager_provider, 
                                     name="signup_screen")
        login_screen = LogInScreen(self.ui_assets_manager,
                                   self.profiles_manager_provider, 
                                   name="login_screen")

        self.sm = MDScreenManager()
        self.sm.add_widget(signup_screen)
        self.sm.add_widget(login_screen)
        self.sm.add_widget(main_window)

        self.nav_layout.add_widget(self.sm)
        self.nav_layout.add_widget(self.main_menu)

        current_user = self.profiles_manager_provider.get_current_user()
        self.sm.current = "main_window" if current_user else "signup_screen"

        return self.nav_layout

class Tile(MDCard):

    def __init__(self, text, link, source, tile_type, tile_mode, bg_color, **kwargs):
        super().__init__(**kwargs)
        self.tile_associated_text = text
        self.tile_type = tile_type
        self.link = link
        self.md_bg_color=bg_color
        self.orientation = 'vertical'
        self.padding = dp(16)
        self.size_hint = (None, None)
        tile_size = int(Window.width/8)
        self.size = (dp(tile_size), dp(tile_size))
        self.radius = [15]
        self.ripple_behavior = True

        # Label
        self.label = MDLabel(
            text=text,
            halign='center',
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            font_style="H5",
            size_hint_y=None,
            height=dp(40)
        )

        self.image_anchor = AnchorLayout(anchor_x='center', anchor_y='center')
        # Image
        image_size = int(Window.width/12)
        self.image = AsyncImage(source=source, 
                                size=(dp(image_size), dp(image_size)),
                                size_hint=(None, None))
        self.image_anchor.add_widget(self.image)

        # Add widgets according to tile_mode
        if tile_mode == "text_and_pictogram":
            self.__show_text_and_pictogram__()
        elif tile_mode == "only_text":
            self.__show_only_text__()
        elif tile_mode == "only_pictogram":
            self.__show_only_pictogram__()

    def __show_only_text__(self):
        self.add_widget(Widget(size_hint_y=1.0))
        self.add_widget(self.label)
        self.add_widget(Widget(size_hint_y=0.03))

    def __show_only_pictogram__(self):
        self.add_widget(self.image_anchor)
        self.add_widget(Widget(size_hint_y=1.0))
        self.label.text = ""
        self.add_widget(self.label)
        self.add_widget(Widget(size_hint_y=0.03))

    def __show_text_and_pictogram__(self):
        self.add_widget(self.image_anchor)
        self.add_widget(Widget(size_hint_y=1.0))
        self.add_widget(self.label)
        self.add_widget(Widget(size_hint_y=0.03))

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
        Window.size = (2340, 1080)
        self.tab_id = tab_id
        self.parent_window = parent_window

    def set_ui_assets_manager(self, ui_assets_manager):
        self.ui_assets_manager = ui_assets_manager

    def set_content(self, words_with_images, tile_mode):
        self.words_with_images = words_with_images
        self.tile_mode = tile_mode

    def set_message_builder_provider(self, message_builder_provider):
        self.message_builder_provider = message_builder_provider

    def build(self):
        grid = GridLayout(rows=len(self.words_with_images),
                          cols=len(self.words_with_images[0]) if self.words_with_images else 0,
                          spacing=(25, 16),
                          size_hint=(1.6, 1.6))
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
                grid.add_widget(tile)

        self.add_widget(grid)

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
    
    def __init__(self, ui_assets_manager, profiles_manager_provider, **kwargs):
        super().__init__(**kwargs)
        Window.size = (2340, 1080)
        self.ui_assets_manager = ui_assets_manager
        self.profiles_manager_provider = profiles_manager_provider

    def go_to_signup_page(self):
        self.manager.current = 'signup_screen'

    def go_to_main_window(self):
        self.manager.current = 'main_window'

    def validate_login(self):
        username = self.ids.username.text
        password = self.ids.password.text
        try:
            _ = self.profiles_manager_provider.login_user(username, password)
            MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("inicio_sesion_correcto"))).open()
            self.ids.username.text = ""
            self.ids.password.text = ""
            self.go_to_main_window()
        except LogInException:
            MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("inicio_sesion_incorrecto"))).open()

class SignupScreen(MDScreen):
    
    def __init__(self, ui_assets_manager, profiles_manager_provider, **kwargs):
        super().__init__(**kwargs)
        Window.size = (2340, 1080)
        self.ui_assets_manager = ui_assets_manager
        self.profiles_manager_provider = profiles_manager_provider

    def go_to_login_page(self):
        self.manager.current = 'login_screen'

    def go_to_main_window(self):
        self.manager.current = 'main_window'

    def execute_signup(self):
        username = self.ids.username.text
        email = self.ids.email.text
        role = self.ids.role.text
        password = self.ids.password.text
        try:
            self.profiles_manager_provider.create_user(username, email, role, password)
            MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("crear_cuenta_correcto"))).open()
            _ = self.profiles_manager_provider.login_user(username, password)

            self.ids.username.text = ""
            self.ids.email.text = ""
            self.ids.role.text = ""
            self.ids.password.text = ""

            self.go_to_main_window()
        except (InvalidUsernameException, InvalidEmailException,
                InvalidPasswordException, DuplicatedUserException) as exception_id:
            MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string(exception_id.message))).open()

class MainMenu(MDNavigationDrawer):

    def __init__(self, ui_assets_manager, profiles_manager_provider, **kwargs):
        super().__init__(kwargs)
        self.ui_assets_manager = ui_assets_manager
        self.profiles_manager_provider = profiles_manager_provider
        self.profiles_manager_provider.add_notified(self)

    def update_login(self):
        self.current_user = self.profiles_manager_provider.get_current_user()
        self.username_row_label.text = ""
        self.email_row_label.text = ""
        if (self.current_user is not None):
            self.username_row_label.text = self.current_user.get_username()
            self.email_row_label.text = self.current_user.get_email()

    def build(self):
        main_layout = MDBoxLayout(orientation="vertical")

        username_row_box = MDBoxLayout()
        username_row_icon = MDIcon(icon="account", 
                                pos_hint={"center_y": 0.75},
                                padding=(16, 16))
        self.current_user = self.profiles_manager_provider.get_current_user()
        current_username = ""
        current_user_email = ""
        if (self.current_user!=None):
            current_username = self.current_user.get_username()
            current_user_email = self.current_user.get_email()

        self.username_row_label = MDLabel(text=current_username, 
                                  size_hint_y=None,
                                  font_style="Body1",
                                  pos_hint={"center_y": 0.75})
        username_row_box.add_widget(username_row_icon)
        username_row_box.add_widget(self.username_row_label)
        
        email_row_box = MDBoxLayout()
        email_row_icon = MDIcon(icon="email", 
                        pos_hint={"center_y": 1.50},
                        padding=(16, 16))
        self.email_row_label = MDLabel(text=current_user_email, 
                                  size_hint_y=None,
                                  font_style="Body1",
                                  pos_hint={"center_y": 1.50})
        
        email_row_box.add_widget(email_row_icon)
        email_row_box.add_widget(self.email_row_label)

        third_row_box = MDBoxLayout()
        third_row_space = MDLabel(text="")
        third_row_button = MDIconButton(
            icon="logout",
            pos_hint={"center_y": 2.90},
            md_bg_color="#f9f871",
            on_release=lambda x: self.on_click_but_close_session(x)
        )
        third_row_box.add_widget(third_row_space)
        third_row_box.add_widget(third_row_button)

        fourth_row_box = MDBoxLayout()
        fourth_row_label = MDLabel(text="", pos_hint={"center_y": 3.30})
        
        fourth_row_button = MDIconButton(
            icon="delete-forever",
            pos_hint={"center_y": 3.30},
            size_hint=(None, None),
            padding=(40, 0),
            md_bg_color="#a23663",
            on_release=lambda x: self.on_click_but_delete_account(x)
        )
        fourth_row_box.add_widget(fourth_row_label)
        fourth_row_box.add_widget(fourth_row_button)

        main_layout.add_widget(username_row_box)
        main_layout.add_widget(email_row_box)
        main_layout.add_widget(third_row_box)
        main_layout.add_widget(fourth_row_box)

        self.add_widget(main_layout)

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
        self.profiles_manager_provider.logout_current_user()
        self.close_menu()

class DeleteAccountDialog(MDBoxLayout):

    def __init__(self, main_menu, ui_assets_manager, profiles_manager_provider, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.spacing = dp(12)
        self.padding = dp(12)
        self.size_hint_y = None
        self.height = dp(130)

        self.main_menu = main_menu
        self.ui_assets_manager = ui_assets_manager
        self.profiles_manager_provider = profiles_manager_provider
        deletion_warning = self.ui_assets_manager.get_string("aviso_eliminacion")
        self.dialog_label = MDLabel(text=deletion_warning) 
        
        self.email_field = MDTextField(
            mode="rectangle",
            size_hint_y=None,
            height=dp(60),
        )
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
        current_username = self.profiles_manager_provider.get_current_user().get_username()
        typed_email = self.email_field.text
        self.delete_dialog.dismiss()
        try:
            self.main_menu.close_menu()
            self.profiles_manager_provider.delete_user(current_username, typed_email)
            MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("confirmacion_eliminacion_cuenta"))).open()
        except UserDeletionException:
            MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("eliminar_cuenta_email_incorrecto"))).open()

class MainWindow(MDScreen):

    def __init__(self,
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

        Window.size = (2340, 1080)

        self.build()

    def go_to_login_page(self):
        self.manager.current = "login_screen"

    def build(self):
        self.clear_widgets()
        self.ui_assets_manager.set_language(self.settings_provider.get_current_language())

        # --- MAIN LAYOUT ---
        self.main_layout = MDBoxLayout(orientation="vertical")

        self.current_user = self.profiles_manager_provider.get_current_user()
        self.current_username = self.current_user.get_username() if self.current_user else ""

        # --- TOP LAYOUT ---
        self.top_layout = MDBoxLayout(orientation="vertical")

        self.build_top_app_bar()
        self.build_message_field()

        self.main_layout.add_widget(self.top_layout)

        # --- GRID SETUP ---
        self.grids_content = {}
        self.build_grid_content()

        self.grid_window = None
        self.swap_grid_window('main_window')

        self.add_widget(self.main_layout)

    def build_top_app_bar(self):
        self.toolbar = MDTopAppBar(
            title=self.ui_assets_manager.get_string("titulo_app"),
            md_bg_color="#29acb6",
            type="top",
            type_height="small",
            left_action_items=[["menu", lambda x: self.on_click_main_menu_dots(x)],
                               ["eye", lambda x: self.on_click_but_tile_mode(x)]],
            right_action_items=[["translate", lambda x: self.on_click_but_language(x)]],
            padding=(18, 18)
        )

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

        self.top_layout.add_widget(self.toolbar)

    def build_message_field(self):
        # --- MESSAGE FIELD WITH ICONS OVERLAY ---
        self.message_field_container = MDBoxLayout(padding=(18, 18))

        # Speaker icon button
        self.but_play_speech = MDIconButton(
            icon="account-voice",
            font_size="28sp",
            pos_hint={"top": 0.95},
            md_bg_color="#f9f871",
            on_release=self.on_click_but_play_speech
        )
        self.message_field_container.add_widget(self.but_play_speech)

        # Scrollable text field
        self.tf_user_aac_message = MDTextField(
            text="",
            readonly=True,
            mode="rectangle",
            multiline=True,
            height=Window.height * 0.2,
            pos_hint={"right": 0.9, "top": 0.99},
            line_color_focus=(0.3, 0.3, 0.3, 1)
        )
        self.message_field_container_adjuster = MDBoxLayout(padding=(18, 0))
        self.message_field_container_adjuster.add_widget(self.tf_user_aac_message)
        self.message_field_container.add_widget(self.message_field_container_adjuster)

        # --- ICON BUTTONS OVERLAY ---

        # Delete last word button
        self.but_delete_last_word = MDIconButton(
            icon="backspace",
            font_size="28sp",
            pos_hint={"top": 0.99},  # Top-right corner
            md_bg_color="#f9f871",
            on_release=self.on_click_but_delete_last_word,
        )
        self.message_field_container.add_widget(self.but_delete_last_word)

        # Clear message button
        self.but_clear_message = MDIconButton(
            icon="delete",
            font_size="28sp",
            pos_hint={"top": 0.99},
            md_bg_color="#f9f871",
            on_release=self.on_click_but_clear_message
        )
        self.message_field_container.add_widget(self.but_clear_message)

        self.top_layout.add_widget(self.message_field_container)

    # --- GRID & LANGUAGE LOGIC ---
    def build_grid_content(self):
        language = self.settings_provider.get_current_language()
        self.grids_content = self.ui_assets_manager.load_grids(language)

    def update_message(self):
        message = self.message_builder_provider.get_current_message()
        message_str = " ".join(message)

        self.tf_user_aac_message.text = message_str

    def update_language(self):
        self.message_builder_provider.clear_message()
        self.build()

    def update_login(self):
        current_user = self.profiles_manager_provider.get_current_user()
        if current_user:
            self.build()
        else:
            self.go_to_login_page()

    def swap_grid_window(self, tab_id):
        if self.grid_window:
            self.main_layout.remove_widget(self.grid_window)

        self.grid_window = GridWindow(self, tab_id, padding=(16, 16))
        self.grid_window.set_ui_assets_manager(self.ui_assets_manager)
        self.grid_window.set_content(
            self.grids_content[tab_id],
            self.settings_provider.get_current_tile_mode()
        )
        self.grid_window.set_message_builder_provider(self.message_builder_provider)
        self.grid_window.build()

        self.main_layout.add_widget(self.grid_window)
        self.main_layout.do_layout()

    # --- BUTTON CALLBACKS ---
    def on_click_main_menu_dots(self, widget):
        self.main_menu.open_menu()

    def on_click_but_profile(self, widget):
        MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("no_disponible"))).open()

    def on_click_but_play_speech(self, widget):
        MDSnackbar(MDLabel(text=self.ui_assets_manager.get_string("no_disponible"))).open()

    def on_click_but_language(self, widget):
        self.language_menu.caller = widget
        self.language_menu.open()

    def on_click_language_option(self, widget):
        # The KivyMD library, in this case, sends the widget as
        # a text.
        new_language_code = self.settings_provider.get_language_code_by_name(widget)
        self.settings_provider.change_current_language(new_language_code)

    def on_click_but_tile_mode(self, widget):
        self.message_builder_provider.clear_message()
        available_tile_modes = self.settings_provider.get_available_tile_modes()
        current_tile_mode = self.settings_provider.get_current_tile_mode()

        for idx, tile_mode_aux in enumerate(available_tile_modes):
            if (tile_mode_aux==current_tile_mode):
                new_idx = (idx+1)%(len(available_tile_modes))

        self.settings_provider.change_current_tile_mode(available_tile_modes[new_idx])

    def on_click_but_delete_last_word(self, widget):
        self.message_builder_provider.remove_last_word_from_message()

    def on_click_but_clear_message(self, widget):
        self.message_builder_provider.clear_message()
