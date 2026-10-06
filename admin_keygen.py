from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.clipboard import Clipboard
from license_core import activation_key, normalize_device_id

class KeyAdminApp(App):
    def build(self):
        self.title = "M6GH License Admin"
        root = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))
        root.add_widget(Label(text="Mazda 6 GH — выдача ключа", size_hint_y=None, height=dp(48)))
        self.device = TextInput(hint_text="Код устройства клиента", multiline=False, size_hint_y=None, height=dp(48))
        self.key = TextInput(hint_text="Ключ активации", readonly=True, multiline=False, size_hint_y=None, height=dp(48))
        make = Button(text="Сгенерировать ключ", size_hint_y=None, height=dp(50))
        copy = Button(text="Копировать ключ", size_hint_y=None, height=dp(50))
        make.bind(on_release=self.generate)
        copy.bind(on_release=lambda *_: Clipboard.copy(self.key.text))
        root.add_widget(self.device); root.add_widget(make); root.add_widget(self.key); root.add_widget(copy)
        root.add_widget(Label(text="Ключ действует только для указанного кода устройства.\nИнтернет для генерации и активации не требуется."))
        return root

    def generate(self, *_):
        dc = normalize_device_id(self.device.text)
        self.key.text = activation_key(dc) if dc else ""

if __name__ == "__main__":
    KeyAdminApp().run()
