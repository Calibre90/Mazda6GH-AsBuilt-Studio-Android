# Run84 exact-source + Run22 offline activation gate
# Import the exact Run84 as a module. This avoids executing its original App.run()
# while the license wrapper is starting.
from main_base import *
from license_core import device_code, verify_activation
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.clipboard import Clipboard
from kivy.utils import platform

class LicensedMazdaAndroidApp(MazdaAndroidApp):
    def _android_id(self):
        try:
            if platform == "android":
                from jnius import autoclass
                Secure = autoclass("android.provider.Settings$Secure")
                Activity = autoclass("org.kivy.android.PythonActivity").mActivity
                value = Secure.getString(Activity.getContentResolver(), Secure.ANDROID_ID)
                if value:
                    return str(value)
        except Exception:
            pass
        # Keep startup alive even if Android ID access fails unexpectedly.
        return "ANDROID-UNKNOWN"

    def build(self):
        self.title = "Mazda 6 GH As-Built Studio"
        Window.softinput_mode = "below_target"
        self.db = Path(self.user_data_dir) / "settings.json"
        self.data = self.load_settings()
        self.license_db = Path(self.user_data_dir) / "license.json"
        self.dc = device_code(self._android_id())

        if self.license_db.exists():
            try:
                d = json.loads(self.license_db.read_text(encoding="utf-8"))
                if d.get("device_code") == self.dc and verify_activation(self.dc, d.get("key", "")):
                    return Main()
            except Exception:
                pass

        root = BoxLayout(orientation="vertical", padding=dp(18), spacing=dp(10))
        root.add_widget(Label(text="Активация Mazda6GH As-Built Studio", font_size="20sp"))
        root.add_widget(Label(text="Device Code"))
        code = TextInput(text=self.dc, readonly=True, multiline=False, size_hint_y=None, height=dp(48))
        root.add_widget(code)
        cp = Button(text="Копировать Device Code", size_hint_y=None, height=dp(48))
        cp.bind(on_release=lambda *_: Clipboard.copy(self.dc))
        root.add_widget(cp)
        key = TextInput(hint_text="Lifetime Key", multiline=False, size_hint_y=None, height=dp(48))
        root.add_widget(key)
        status = Label(text="Введите ключ, полученный у администратора")
        root.add_widget(status)
        btn = Button(text="Активировать", size_hint_y=None, height=dp(52))
        root.add_widget(btn)

        def activate(*_):
            if verify_activation(self.dc, key.text):
                self.license_db.write_text(
                    json.dumps({"device_code": self.dc, "key": key.text.strip().upper()}),
                    encoding="utf-8",
                )
                root.clear_widgets()
                root.add_widget(Main())
            else:
                status.text = "Неверный ключ активации"

        btn.bind(on_release=activate)
        return root

if __name__ == "__main__":
    LicensedMazdaAndroidApp().run()
