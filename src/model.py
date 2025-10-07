from json import load as json_load
from os.path import join as os_path_join, abspath as os_path_abspath, dirname as os_path_dirname, exists as os_path_exists
import sys

class UIAssetsManager():

    def __init__(self):
        pass

    def set_language(self, selected_language_code):
        self.selected_language_code = selected_language_code
        with open(self.get_resource(f"src/strings/{self.selected_language_code}.json"), "r", encoding='utf-8') as f:
            self.strings = json_load(f)

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