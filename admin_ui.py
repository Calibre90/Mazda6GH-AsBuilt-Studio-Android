from kivy.app import App
from kivy.core.clipboard import Clipboard
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
import re

class LicenseAdminApp(App):
    title = "M6GH License Admin"

    def build(self):
        root = BoxLayout(orientation="vertical", padding=dp(18), spacing=dp(10))
        root.add_widget(Label(text="M6GH Run84 License Admin", font_size="20sp",
                              size_hint_y=None, height=dp(54)))
        root.add_widget(Label(text="Введите Device Code из клиентского приложения",
                              size_hint_y=None, height=dp(42)))
        self.device = TextInput(hint_text="XXXXX-XXXXX-XXXXX-XXXXX",
                                multiline=False, size_hint_y=None, height=dp(48))
        self.key = TextInput(hint_text="Lifetime Key", readonly=True,
                             multiline=True, size_hint_y=1)
        self.status = Label(text="Ключ подписи не хранится в GitHub",
                            size_hint_y=None, height=dp(42))
        generate = Button(text="Создать Lifetime Key", size_hint_y=None, height=dp(52))
        copy = Button(text="Копировать ключ", size_hint_y=None, height=dp(48))
        generate.bind(on_release=self.generate_key)
        copy.bind(on_release=lambda *_: Clipboard.copy(self.key.text.strip()))
        for w in (self.device, generate, self.key, copy, self.status):
            root.add_widget(w)
        return root

    def generate_key(self, *_):
        code = self.device.text.strip().upper()
        if not re.fullmatch(r"[A-F0-9]{5}(?:-[A-F0-9]{5}){3}", code):
            self.key.text = ""
            self.status.text = "Ошибка: Device Code должен быть XXXXX-XXXXX-XXXXX-XXXXX"
            return
        try:
            from admin_signer import sign_device_code
            self.key.text = sign_device_code(code)
            if not self.key.text:
                raise ValueError("empty key")
            self.status.text = "Lifetime Key создан для " + code
        except Exception:
            self.key.text = ""
            self.status.text = "Нет приватного ключа/модуля подписи"

if __name__ == "__main__":
    LicenseAdminApp().run()
