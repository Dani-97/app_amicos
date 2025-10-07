from kivy.app import App
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from KivyCustom.Custom import ButtonRnd, CustomTextInput
from KivyCustom.Custom import Tile
from KivyCustom.Custom import TileWithPictogram
from kivy.uix.scrollview import ScrollView
from openpyxl import load_workbook
import os

class AmicosApp(App):

    def set_ui_assets_manager(self, ui_assets_manager):
        self.ui_assets_manager = ui_assets_manager

    def set_message_builder_provider(self, message_builder_provider):
        self.message_builder_provider = message_builder_provider

    """
    Clase principal de la aplicación, se encarga de la inicialización
    Es la encargada de iniciar la aplicación y construirla.    
    """
    def build(self):
        self.title = 'App Amicos'  
        
        self.ui_assets_manager.set_language("es_ES")
        
        self.icon = self.ui_assets_manager.get_resource("assets/logo.png")
        
        LabelBase.register(name='Titulo', fn_regular=self.ui_assets_manager.get_resource('src/fonts/Orbitron-Regular.ttf'))
        LabelBase.register(name='Texto', fn_regular=self.ui_assets_manager.get_resource('src/fonts/FrancoisOne-Regular.ttf'))

        main_window = MainWindow(self.ui_assets_manager,
                                 self.message_builder_provider)
        main_window.build()

        self.sm = ScreenManager()
        self.sm.add_widget(main_window)

        return self.sm

class GridWindow(GridLayout):

    """
    Esta clase crea un tablero con las palabras y las imágenes correspondientes
    Patron de diseño: Composite
    """
    def __init__(self, parent_window, tab_id, **kwargs):
        super(GridWindow, self).__init__(**kwargs)
        self.tab_id = tab_id
        self.parent_window = parent_window

    def set_ui_assets_manager(self, ui_assets_manager):
        self.ui_assets_manager = ui_assets_manager

    def set_content(self, words_with_images, pictograms):
        self.words_with_images = words_with_images
        self.pictograms = pictograms

    def set_message_builder_provider(self, message_builder_provider):
        self.message_builder_provider = message_builder_provider

    def build(self):
        self.rows = len(self.words_with_images)
        self.cols = len(self.words_with_images[0]) if self.words_with_images else 0
        self.spacing = [10, 10]
        self.tiles = []
        for row in self.words_with_images:
            for picture, word in row:
                if self.pictograms:
                    tile = TileWithPictogram(text=str(word), source=self.ui_assets_manager.get_resource(f'src/assets/{picture}'), on_press=self.on_tile_clicked)
                else:
                    tile = Tile(text=str(word), on_press=self.on_tile_clicked, font_name='Texto')
                self.tiles.append(tile)
                self.add_widget(tile)

    # Función que se ejecuta al pulsar una casilla
    def on_tile_clicked(self, instance):
        tile_text = ""

        if (self.pictograms):
            tile_text = instance.label.text
        else: 
            tile_text = instance.text
        
        try:        
            self.parent_window.swap_grid_window(tile_text)
        except KeyError:
            self.message_builder_provider.add_word_to_message(tile_text)
            self.parent_window.swap_grid_window(self.tab_id)

class MainWindow(Screen):

    def __init__(self, ui_assets_manager, message_builder_provider, **kwargs):
        super(MainWindow, self).__init__(**kwargs)
        self.ui_assets_manager = ui_assets_manager
        self.message_builder_provider = message_builder_provider
        self.message_builder_provider.add_notified(self)
        Window.size = (2048, 1080)

    def build(self):
        self.but_delete_last_word = None
        self.but_clear_message = None

        Builder.load_file(self.ui_assets_manager.get_resource('src/KivyCustom/custom.kv'))

        # Layout principal
        self.main_layout = BoxLayout(orientation='vertical')  # Cambia la orientación a vertical
        self.add_widget(self.main_layout)
                
        # Añade un espacio en blanco 
        blank_space = BoxLayout(size_hint=(1, .03))

        # Layout de los botones
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, .17), spacing=10)
        self.vertical_layout = BoxLayout(orientation='vertical', size_hint=(1, 0.2))
        self.vertical_layout.add_widget(buttons_layout)
        self.main_layout.add_widget(self.vertical_layout)

        # El boton de inicio
        self.but_config = ButtonRnd(text=self.ui_assets_manager.get_string("config"), 
                                    size_hint=(.15, 1), 
                                    on_press=self.on_click_but_settings, 
                                    font_name='Texto', 
                                    disabled = True)
        buttons_layout.add_widget(self.but_config)

        # Espacio para texto
        scroll = ScrollView(size_hint=(.4, 1), scroll_type=['bars', 'content'], bar_width=10)
        self.tf_user_aac_message = CustomTextInput(
            text="",
            # Limita el ancho del texto al ancho del widget
            #size_hint_y=None,  # Esto permitirá que el TextInput se expanda a su tamaño natural
            height=Window.height * 0.2,  # Altura inicial del TextInput
            halign='left',  
            font_name='Texto', 
            font_size=40,
            background_color=(0.7, 0.7, 0.7, 1),
            foreground_color=(0, 0, 0, 1),
            readonly=True,
            cursor_blink=False,  # Deshabilita el parpadeo del cursor
            cursor_width=0,  # Establece el ancho del cursor a 0
            focus=False
        )

        self.tf_user_aac_message.bind(on_text=self.on_tf_user_aac_message_text_changed)  # Añade un evento para cuando el texto cambie
        self.tf_user_aac_message.bind(on_touch_down = self.on_tf_user_aac_message_touch_down)
        scroll.add_widget(self.tf_user_aac_message)
        buttons_layout.add_widget(scroll)

        # El boton para borrar una palabra
        self.but_delete_last_word = ButtonRnd(text=self.ui_assets_manager.get_string("borrar"), 
                                              size_hint=(.15, 1), 
                                              on_press=self.on_click_but_delete_last_word, 
                                              font_name='Texto')
        buttons_layout.add_widget(self.but_delete_last_word)

        # El boton para borrar todo el texto
        self.but_clear_message = ButtonRnd(text=self.ui_assets_manager.get_string("borrar_todo"), 
                                           size_hint=(.15, 1), 
                                           on_press=self.on_click_but_clear_message, 
                                           font_name='Texto')
        buttons_layout.add_widget(self.but_clear_message)

        self.grids_content = {}
        self.build_grid_content()

        self.grid_window = None
        self.swap_grid_window('TAB. INICIAL')

        self.vertical_layout.add_widget(blank_space)

    def build_grid_content(self):
        language = "es_ES"
        filename = self.ui_assets_manager.get_resource(f'src/grids/grids_{language}.xlsx')
        wb = load_workbook(filename)
        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]
            words_with_images = []
            for ws_row_aux in ws.iter_rows():
                current_row_content = []
                for i in range(0, len(ws_row_aux), 2):
                    tile_image = ws_row_aux[i]
                    tile_word = ws_row_aux[i + 1]
                    current_row_content.append((tile_image.value, tile_word.value))
                
                words_with_images.append(current_row_content)

            self.grids_content[sheet_name] = words_with_images

    def update_message(self, message):
        message_str = ""
        for current_word in message:
            message_str+=" " + current_word

        self.tf_user_aac_message.text = message_str

    def swap_grid_window(self, tab_id):
        if (self.grid_window is not None):
            self.main_layout.remove_widget(self.grid_window)
        
        self.grid_window = GridWindow(self, tab_id, size_hint=(1, 0.8))
        self.grid_window.set_ui_assets_manager(self.ui_assets_manager)
        self.grid_window.set_content(self.grids_content[tab_id], True)
        self.grid_window.set_message_builder_provider(self.message_builder_provider)
        self.grid_window.build()

        self.main_layout.add_widget(self.grid_window, index=0)
        self.main_layout.do_layout()

    def on_tf_user_aac_message_text_changed(self, widget):
        pass

    def on_tf_user_aac_message_touch_down(self, widget, touch):
        pass

    def on_click_but_settings(self, widget):
        pass

    def on_click_but_delete_last_word(self, widget):
        self.message_builder_provider.remove_last_word_from_message()

    def on_click_but_clear_message(self, widget):
        self.message_builder_provider.clear_message()
