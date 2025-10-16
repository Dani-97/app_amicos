from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
import json
import os
import requests

class AIApp(App):

    def build(self):
        self.layout = BoxLayout(orientation='vertical')

        self.user_input = TextInput(hint_text='Introduce tu pregunta', font_size="48px", size_hint_y=0.3)
        self.layout.add_widget(self.user_input)

        self.submit_btn = Button(text='Enviar', font_size="48px", size_hint_x=0.7, size_hint_y=0.1)
        self.submit_btn.bind(on_press=self.send_to_ai)
        self.layout.add_widget(self.submit_btn)

        self.response_label = Label(text='La respuesta aparecerá aquí', font_size="48px", size_hint_y=0.3)
        self.layout.add_widget(self.response_label)

        lang_box = BoxLayout(size_hint_y=None, height=50, spacing=10)
        lang_label = Label(text="🌐 Idioma:", font_size=18, size_hint_x=None, width=120, color=(0, 0, 0, 1))
        self.lang_spinner = Spinner(
            text="es_ES",
            values=("es_ES", "gal_ES", "en_GB"),
            size_hint=(1, None),
            height=44,
            font_size=16,
            background_color=(0.8, 0.8, 0.8, 1)
        )
        lang_box.add_widget(lang_label)
        lang_box.add_widget(self.lang_spinner)
        self.layout.add_widget(lang_box)

        return self.layout

    def send_to_ai(self, instance):
        prompt = self.user_input.text
        response_text = self.query_cerebras(prompt)
        self.response_label.text = response_text

    def __process_result_text__(self, raw_response):
        # Split by lines that start with "data:"
        chunks = []
        for line in raw_response.splitlines():
            line = line.strip()
            if line.startswith("data: "):
                json_str = line[len("data: "):].strip()
                if json_str and json_str != "[DONE]":  # avoid empty or final signals
                    try:
                        chunk = json.loads(json_str)
                        chunks.append(chunk)
                    except json.JSONDecodeError:
                        pass  # skip malformed lines

        # Combine text from deltas
        final_text = ""
        for chunk in chunks:
            delta = chunk.get("choices", [{}])[0].get("delta", {})
            if "content" in delta:
                final_text += delta["content"]

        return final_text

    def query_cerebras(self, message_to_conjugate):
        prompt_file = open(f"./strings/prompt_{self.lang_spinner.text}.txt")
        prompt_text = prompt_file.read()
        prompt_text += f'\n\n Frase: {message_to_conjugate}'

        api_key = 'csk-6rwhpfhyyd6j3wm8cvf9255wr56d9ph8wexxn5xrhyrx6h9x'

        url = "https://api.cerebras.ai/v1/chat/completions"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        data = {
            "model": "llama-3.3-70b",
            "stream": True,
            "max_tokens": 20000,
            "temperature": 0.7,
            "top_p": 0.8,
            "messages": [
                {
                    "role": "user",
                    "content": f"{prompt_text}"
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)

        if (response.status_code==200):
            processed_result_text = self.__process_result_text__(response.text)
        else:
            processed_result_text = f'Se ha producido un problema: código de estado -> {response.status_code}'

        return processed_result_text

if __name__ == "__main__":
    AIApp().run()
