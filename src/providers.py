from json import load as json_load
import os
from os.path import join as os_path_join, abspath as os_path_abspath, dirname as os_path_dirname, exists as os_path_exists
import sys
import xml.etree.ElementTree as ET

class UIAssetsManager():

    def __init__(self):
        pass

    def set_language(self, selected_language_code):
        self.selected_language_code = selected_language_code

        with open(self.get_resource(f"strings/{self.selected_language_code}.json"), "r", encoding='utf-8') as f:
            self.strings = json_load(f)

    def __parse_xml__(self, filename):
        
        def parse_xml_aux(root, grid, current_row):
            for child in root:
                if (len(child)>0):
                    grid = parse_xml_aux(child, 
                        grid, 
                        current_row)
                    if (child.tag=="row"):
                        if (len(current_row)>0):
                            grid.append(current_row)
                            current_row = []
                else:
                    if (child.tag=="category"):
                        current_row.append(("category",
                                            child.text, 
                                            child.attrib['picture_url'], 
                                            child.attrib['link']))
                    if (child.tag=="item"):
                        current_row.append(("item",
                                            child.text, 
                                            child.attrib['picture_url'], 
                                            None))

            return grid

        tree = ET.parse(filename)
        root = tree.getroot()

        grid = parse_xml_aux(root, [], [])
        
        return grid

    def load_grids(self, language):
        grids_content = {}

        root_dir = f'grids/{language}'
        grids_list = os.listdir(root_dir)

        for current_grid_filename in grids_list:
            current_grid_id = current_grid_filename.replace('.xml', '')
            current_grid_path = f'{root_dir}/{current_grid_filename}'
            current_grid_path = self.get_resource(current_grid_path)
            current_grid_content = self.__parse_xml__(current_grid_path)
            grids_content[current_grid_id] = current_grid_content

        return grids_content

    def get_resource(self, relative_path):
        """
        Obtiene la ruta absoluta al recurso, funciona tanto en desarrollo como en PyInstaller
        """
        try:
            # Cuando está empaquetado con PyInstaller
            base_path = sys._MEIPASS
        except AttributeError:
            # Cuando se ejecuta como script
            base_path = os_path_abspath(".")

        # Si lo hay en la carpeta (los tableros) 
        exe_path = os_path_abspath(os_path_join(os_path_dirname(sys.executable), relative_path))
        if os_path_exists(exe_path):
            return exe_path
        else:
            return os_path_join(base_path, relative_path)

    def get_string(self, string_id):
        return self.strings[string_id]

class MessageBuilderProvider():

    def __init__(self):
        self.message = []
        self.notified_widgets_list = []

    def add_notified(self, notified_widget):
        self.notified_widgets_list.append(notified_widget)

    def __notify_widgets__(self):
        for widget in self.notified_widgets_list:
            widget.update_message()

    def get_current_message(self):
        return self.message

    def update_message(self, new_message):
        self.message = new_message
        self.__notify_widgets__()

    def add_word_to_message(self, new_word):
        self.message.append(new_word)
        self.__notify_widgets__()

    def remove_last_word_from_message(self):
        self.message = self.message[:-1]
        self.__notify_widgets__()

    def clear_message(self):
        self.message = []
        self.__notify_widgets__()

class Settings_Provider():

    def __init__(self):
        self.available_languages = ["es_ES", "gal_ES"]
        self.languages_names_dict = {"Castellano": "es_ES", "Galego": "gal_ES"}
        self.available_tile_modes = ['text_and_pictogram', 'only_pictogram']
        self.language_selected = "es_ES"
        self.notified_widgets_list = []
        self.tile_mode = "text_and_pictogram"

    def add_notified(self, notified_widget):
        self.notified_widgets_list.append(notified_widget)

    def __notify_widgets__(self):
        for widget in self.notified_widgets_list:
            widget.update_language()

    def get_language_code_by_name(self, language_name):
        return self.languages_names_dict[language_name]

    def get_current_language(self):
        return self.language_selected
    
    def get_available_languages_codes(self):
        return self.available_languages
    
    def get_available_languages_names(self):
        return self.languages_names_dict.keys()

    def change_current_language(self, new_language):
        self.language_selected = new_language
        self.__notify_widgets__()

    def get_current_tile_mode(self):
        return self.tile_mode

    def get_available_tile_modes(self):
        return self.available_tile_modes
    
    def change_current_tile_mode(self, new_tile_mode):
        self.tile_mode = new_tile_mode
        self.__notify_widgets__()