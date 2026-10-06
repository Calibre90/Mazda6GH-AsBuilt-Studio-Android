import json, re, hashlib, os
from pathlib import Path
from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.spinner import Spinner
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import platform
from kivy.core.clipboard import Clipboard
from license_core import device_code, verify_activation

DEFAULT={
 "ui":{"title":"Mazda 6 GH As-Built Studio","author_text":"Кто сделал приложение","link1_text":"Ссылка 1","link1_url":"","link2_text":"Ссылка 2","link2_url":""},
 "username":"admin","password_hash":hashlib.sha256("MazdaAdmin-ChangeMe-2026".encode()).hexdigest(),
 "modules":[{"id":"IC","name":"IC: Instrument Cluster","address":"720","version":"1"},{"id":"R_BCM","name":"R_BCM: Rear Body Control Module","address":"7B7","version":"1"},{"id":"SSU","name":"SSU: Start Stop Unit","address":"731","version":"1"}],
 "rows":[{"module":"IC","address":"720-01-01","value":"1F40 7126 809F","status":"Пример"},{"module":"IC","address":"720-01-02","value":"000E F255 E766","status":"Пример"},{"module":"IC","address":"720-01-03","value":"0F0E C236 CC0C","status":"Пример"},{"module":"R_BCM","address":"7B7-01-01","value":"85D0 0004 A1BA","status":"Пример"},{"module":"R_BCM","address":"7B7-01-02","value":"A501 C300 204A","status":"Пример"},{"module":"R_BCM","address":"7B7-01-03","value":"0018 5400 2E","status":"Пример"},{"module":"SSU","address":"731-01-01","value":"","status":"Заполнить из ABT"}],
 "features":[{"id":"rvm","module":"IC","label":"RVM / контроль слепых зон","row":"720-01-01","hex_indices":"1","on":"8","off":"0","status":"НЕ ПРОВЕРЕНО"},{"id":"autolock","module":"R_BCM","label":"Auto Door Lock","row":"7B7-01-01","hex_indices":"0","on":"8","off":"0","status":"НЕ ПРОВЕРЕНО"},{"id":"advanced_key","module":"SSU","label":"Advanced Keyless Entry","row":"731-01-01","hex_indices":"0","on":"8","off":"0","status":"НЕ ПРОВЕРЕНО"}]
}

def norm(s): return re.sub(r"[^0-9A-F]","",str(s).upper())
def decode_abt_index(tok):
    tok=tok.upper()
    if len(tok)==2 and tok[0]>="G": return (ord(tok[0])-ord("G"))*16+int(tok[1],16)
    return int(tok,10)
def encode_abt_index(n): n=int(n); return chr(ord("G")+(n>>4))+format(n&15,"X")
def address_parts(addr):
    a,b,c=addr.upper().split("-")
    def cv(x):
        try:return decode_abt_index(x)
        except:return int(x,10)
    return a,cv(b),cv(c)
def checksum_for(addr,raw):
    mod,b,l=address_parts(addr); total=int(mod[:1],16)+int(mod[1:],16)+b+l
    total+=sum(int(raw[i:i+2],16) for i in range(0,len(raw),2)); return f"{total&255:02X}"
def recalc(row):
    raw=norm(row.get("value",""))
    if len(raw)>=4 and len(raw)%2==0:
        raw=raw[:-2]+checksum_for(row["address"],raw[:-2]); row["value"]=" ".join(raw[i:i+4] for i in range(0,len(raw),4))
def parse_indices(spec):
    out=[]
    for p in re.split(r"[,; ]+",str(spec).strip()):
        if not p: continue
        if "-" in p:
            a,b=map(int,p.split("-",1)); out.extend(range(min(a,b),max(a,b)+1))
        else: out.append(int(p))
    return out
def parse_abt(text,modules):
    parsed=[]; by_addr={str(m.get("address","")).upper():m.get("id","IC") for m in modules}; current=None
    for source in text.splitlines():
        line=source.strip().lstrip("\ufeff")
        bm=re.match(r"^;\s*Block\s+(\d+)",line,re.I)
        if bm: current=int(bm.group(1)); continue
        if not line or line.startswith((";","#","//")): continue
        m=re.match(r"^([0-9A-Fa-f]{3})([0-9A-Za-z]{2})([0-9A-Za-z]{2})([0-9A-Fa-f]+)$",line) or re.match(r"^([0-9A-Fa-f]{3})[- ]([0-9A-Za-z]{2})[- ]([0-9A-Za-z]{2})\s+([0-9A-Fa-f ]+)$",line)
        if not m: continue
        try: bn=decode_abt_index(m.group(2)); ln=decode_abt_index(m.group(3))
        except: continue
        value=norm(m.group(4))
        if not value or len(value)%2: continue
        parsed.append({"module":by_addr.get(m.group(1).upper(),"OTHER"),"address":f"{m.group(1).upper()}-{bn:02d}-{ln:02d}","value":" ".join(value[i:i+4] for i in range(0,len(value),4)),"status":"Импортировано из ABT","abt_block":current if current is not None else bn})
    return parsed

# Full V2.4 UI source follows in the uploaded project. This repository copy
# keeps the core parser/build entrypoint available while the remaining UI
# source is transferred without binary-artifact coupling.
class MazdaAndroidApp(App):
    def _android_id(self):
        try:
            if platform=="android":
                from jnius import autoclass
                S=autoclass("android.provider.Settings$Secure")
                a=autoclass("org.kivy.android.PythonActivity").mActivity
                return str(S.getString(a.getContentResolver(),S.ANDROID_ID))
        except Exception: pass
        return "DESKTOP-TEST"
    def _valid(self):
        try:
            saved=json.loads(self.license_db.read_text(encoding="utf-8"))
            return saved.get("device_code")==self.device_code and verify_activation(self.device_code,saved.get("key",""))
        except Exception: return False
    def _activation(self):
        box=BoxLayout(orientation="vertical",padding=dp(18),spacing=dp(9))
        box.add_widget(Label(text="Mazda 6 GH As-Built Studio",font_size="20sp",size_hint_y=None,height=dp(54)))
        box.add_widget(Label(text="Для запуска требуется активация.\nПередайте продавцу код устройства:",halign="center",size_hint_y=None,height=dp(58)))
        code=TextInput(text=self.device_code,readonly=True,multiline=False,size_hint_y=None,height=dp(46))
        key=TextInput(hint_text="Введите Lifetime-ключ",multiline=False,size_hint_y=None,height=dp(46))
        status=Label(text="",size_hint_y=None,height=dp(42))
        copy=Button(text="Копировать код устройства",size_hint_y=None,height=dp(48))
        activate=Button(text="Активировать навсегда",size_hint_y=None,height=dp(50))
        copy.bind(on_release=lambda *_: Clipboard.copy(self.device_code))
        def go(*_):
            entered=key.text.strip()
            if verify_activation(self.device_code,entered):
                self.license_db.write_text(json.dumps({"device_code":self.device_code,"key":entered}),encoding="utf-8")
                status.text="Активация успешна"; self.manager.current="main"
            else: status.text="Ошибка: ключ не подходит к этому телефону"
        activate.bind(on_release=go)
        for w in (code,copy,key,activate,status): box.add_widget(w)
        return box
    def build(self):
        self.title="Mazda 6 GH As-Built Studio Run #70 Licensed"
        self.license_db=Path(self.user_data_dir)/"license.json"
        self.device_code=device_code(self._android_id())
        self.manager=ScreenManager()
        activation=Screen(name="activation"); activation.add_widget(self._activation())
        main=Screen(name="main")
        root=BoxLayout(orientation="vertical",padding=dp(12),spacing=dp(8))
        root.add_widget(Label(text="Mazda 6 GH As-Built Studio"))
        root.add_widget(Label(text="Run #70 Licensed\nABT parser and checksum core are active."))
        main.add_widget(root)
        self.manager.add_widget(activation); self.manager.add_widget(main)
        self.manager.current="main" if self._valid() else "activation"
        return self.manager

if __name__=="__main__": MazdaAndroidApp().run()
