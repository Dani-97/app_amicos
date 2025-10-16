from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from jnius import autoclass

# Java classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')
TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
Locale = autoclass('java.util.Locale')
Bundle = autoclass('android.os.Bundle')
JavaString = autoclass('java.lang.String')


class MultiLangTTSApp(App):
    def build(self):
        self.activity = PythonActivity.mActivity
        self.tts = TextToSpeech(self.activity, None)

        # Layout
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Text input
        self.text_input = TextInput(
            text='Type something to speak...',
            size_hint_y=0.3
        )
        layout.add_widget(self.text_input)

        # Language selector
        self.language_spinner = Spinner(
            text='English (US)',
            values=('English (US)', 'Spanish (ES)', 'French (FR)', 'German (DE)'),
            size_hint_y=None,
            height=44
        )
        layout.add_widget(self.language_spinner)

        # Speak button
        speak_btn = Button(text='Speak')
        speak_btn.bind(on_press=self.speak_text)
        layout.add_widget(speak_btn)

        return layout

    def speak_text(self, instance):
        # Map selected spinner value to Locale
        lang_map = {
            'English (US)': Locale("en", "US"),
            'Spanish (ES)': Locale("es", "ES"),
            'French (FR)': Locale("fr", "FR"),
            'German (DE)': Locale("de", "DE")
        }

        selected_lang = self.language_spinner.text
        locale = lang_map.get(selected_lang, Locale("en", "US"))

        # Set language and check if supported
        status = self.tts.setLanguage(locale)
        if status in (TextToSpeech.LANG_MISSING_DATA, TextToSpeech.LANG_NOT_SUPPORTED):
            print(f"{selected_lang} not supported on this device")
            return

        # Speak the text
        text = JavaString(self.text_input.text)
        params = Bundle()
        utterance_id = JavaString("utterance1")
        self.tts.speak(text, TextToSpeech.QUEUE_FLUSH, params, utterance_id)


if __name__ == '__main__':
    MultiLangTTSApp().run()
