import json, os
from datetime import datetime
from pathlib import Path
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from license_core_v3 import activation_key

class AdminApp(App):
    def build(self):
        self.title="M6GH Run84 License Admin"
        self.db=Path(self.user_data_dir)/"licenses.json"
        self.rows=self.load()
        root=BoxLayout(orientation="vertical",padding=dp(12),spacing=dp(8))
        root.add_widget(Label(text="M6GH Run84 — генератор лицензий",size_hint_y=None,height=dp(44),font_size="20sp"))
        self.email=TextInput(hint_text="E-mail покупателя",multiline=False,size_hint_y=None,height=dp(48))
        self.device=TextInput(hint_text="Device Code",multiline=False,size_hint_y=None,height=dp(48))
        root.add_widget(self.email); root.add_widget(self.device)
        b=Button(text="Создать / сменить устройство",size_hint_y=None,height=dp(52)); b.bind(on_release=self.generate); root.add_widget(b)
        self.key=TextInput(hint_text="Lifetime Key",readonly=True,multiline=False,size_hint_y=None,height=dp(48)); root.add_widget(self.key)
        cp=Button(text="Копировать Lifetime Key",size_hint_y=None,height=dp(48)); cp.bind(on_release=self.copy_key); root.add_widget(cp)
        self.search=TextInput(hint_text="Поиск: e-mail / № / Device Code / Key",multiline=False,size_hint_y=None,height=dp(48)); root.add_widget(self.search)
        sb=Button(text="Найти",size_hint_y=None,height=dp(46)); sb.bind(on_release=self.do_search); root.add_widget(sb)
        self.out=Label(text="",halign="left",valign="top",size_hint_y=None)
        self.out.bind(texture_size=lambda w,s:setattr(w,"height",max(dp(180),s[1]+dp(20))))
        sc=ScrollView(); sc.add_widget(self.out); root.add_widget(sc)
        self.refresh(self.rows)
        return root
    def load(self):
        try:return json.loads(self.db.read_text(encoding="utf-8")) if self.db.exists() else []
        except:return []
    def save(self): self.db.write_text(json.dumps(self.rows,ensure_ascii=False,indent=2),encoding="utf-8")
    def generate(self,*_):
        email=self.email.text.strip().lower(); dc=self.device.text.strip().upper()
        if not email or not dc: return self.msg("Введите e-mail и Device Code")
        found=next((x for x in self.rows if x["email"].lower()==email),None)
        key=activation_key(dc)
        if found:
            if found["device_code"]!=dc:
                found.setdefault("history",[]).append({"device_code":found["device_code"],"key":found["key"],"status":"REPLACED","date":datetime.now().isoformat(timespec="seconds")})
                found["transfers"]=found.get("transfers",0)+1
            found.update(device_code=dc,key=key,status="ACTIVE",date=datetime.now().isoformat(timespec="seconds"))
        else:
            found={"license_no":len(self.rows)+1,"email":email,"date":datetime.now().isoformat(timespec="seconds"),"device_code":dc,"key":key,"status":"ACTIVE","transfers":0,"history":[]}
            self.rows.append(found)
        self.key.text=key; self.save(); self.refresh([found])
    def copy_key(self,*_):
        from kivy.core.clipboard import Clipboard; Clipboard.copy(self.key.text)
    def do_search(self,*_):
        q=self.search.text.strip().lower()
        if not q:return self.refresh(self.rows)
        self.refresh([x for x in self.rows if q in x["email"].lower() or q==str(x["license_no"]) or q in x["device_code"].lower() or q in x["key"].lower()])
    def refresh(self,rows):
        self.out.text="\n\n".join(f'№{x["license_no"]}  {x["email"]}\n{x["status"]} | переносов: {x.get("transfers",0)}\nDevice: {x["device_code"]}\nKey: {x["key"]}\nДата: {x["date"]}' for x in rows) or "База пока пустая"
    def msg(self,t): Popup(title="Админ",content=Label(text=t),size_hint=(.85,.3)).open()
if __name__=="__main__": AdminApp().run()
