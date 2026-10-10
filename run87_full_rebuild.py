from pathlib import Path
p=Path("main_base.py")
s=p.read_text(encoding="utf-8")
required=["class Main(BoxLayout):","def refresh(self):","def toggle(self,f,active):","def open_document(self,*_):","def save_document(self,*_):"]
missing=[x for x in required if x not in s]
if missing: raise SystemExit("Run88 #12 core verification failed: "+", ".join(missing))

# Run89 Red Premium: visual-only shell over the proven Run88 #12 core.
s=s.replace('from kivy.graphics import Color, Rectangle','from kivy.graphics import Color, Rectangle, RoundedRectangle')
s=s.replace('Window.softinput_mode="below_target"','Window.softinput_mode="below_target"; Window.clearcolor=(0.015,0.012,0.018,1)')
s=s.replace('"background":"#f2f2f2","panel":"#fff7f2"','"background":"#08070a","panel":"#121116"')
s=s.replace('"open_text":"Open As-Built file","save_text":"Save As-Built file"','"open_text":"📂  Open As-Built file","save_text":"💾  Save As-Built file"')
s=s.replace('"author_text":"КТО СДЕЛАЛ ПРОГРАММУ"','"author_text":"MAZDA 6 GH   AS-BUILT STUDIO"')

s=s.replace('ab=Button(text=self.app.data.get("ui",{}).get("admin_text","⚙"),size_hint_x=None,width=dp(52))',
'''ab=Button(text=self.app.data.get("ui",{}).get("admin_text","⚙"),size_hint_x=None,width=dp(52),background_normal="",background_color=(0.42,0.015,0.025,1),color=(1,1,1,1))''')

s=s.replace('ob=Button(text=ui.get("open_text","Open As-Built file")); sb=Button(text=ui.get("save_text","Save As-Built file"))',
'''ob=Button(text=ui.get("open_text","Open As-Built file"),background_normal="",background_color=(0.42,0.015,0.025,1),color=(1,1,1,1)); sb=Button(text=ui.get("save_text","Save As-Built file"),background_normal="",background_color=(0.42,0.015,0.025,1),color=(1,1,1,1))''')

old='''b=Button(text="Dim304",font_size="11sp",padding=(dp(2),dp(2)))
        b.bind(on_release=lambda _b:self.open_url("https://www.drive2.ru/users/dim304"))
        self.header_links.add_widget(b)'''
new='''b=Button(text="ⓘ",font_size="18sp",padding=(dp(2),dp(2)),background_normal="",background_color=(0.42,0.015,0.025,1),color=(1,1,1,1))
        b.bind(on_release=self.about_popup)
        self.header_links.add_widget(b)'''
if old not in s: raise SystemExit("Run89 author hook not found")
s=s.replace(old,new)

anchor='''    def open_url(self,url):
'''
about='''    def about_popup(self,*_):
        box=BoxLayout(orientation="vertical",spacing=dp(10),padding=dp(14))
        title=Label(text="[b]Mazda 6 GH[/b]\\n[b]AS BUILT STUDIO[/b]\\n[color=999999]Android версия[/color]",markup=True,font_size="20sp",size_hint_y=.30,halign="center")
        title.bind(size=lambda inst,val:setattr(inst,"text_size",(val[0],None))); box.add_widget(title)
        dev=Button(text="[b]Разработчик[/b]\\nDim304\\n[color=4da3ff]drive2.ru/users/dim304[/color]",markup=True,background_normal="",background_color=(0.08,0.07,0.09,1),color=(1,1,1,1))
        dev.bind(on_release=lambda _b:self.open_url("https://www.drive2.ru/users/dim304/")); box.add_widget(dev)
        sup=Button(text="[b]Дополнительная поддержка[/b]\\nWolis11\\n[color=4da3ff]drive2.ru/users/wolis11[/color]",markup=True,background_normal="",background_color=(0.08,0.07,0.09,1),color=(1,1,1,1))
        sup.bind(on_release=lambda _b:self.open_url("https://www.drive2.ru/users/wolis11/")); box.add_widget(sup)
        ver=Label(text="Версия: 1.0.0 (STUDIO)\\nСборка: Run #89",font_size="13sp",size_hint_y=.18,color=(.75,.75,.75,1)); box.add_widget(ver)
        ok=Button(text="OK",size_hint_y=None,height=dp(48),background_normal="",background_color=(0.55,0.015,0.025,1),color=(1,1,1,1)); box.add_widget(ok)
        pop=Popup(title="ⓘ  О программе",content=box,size_hint=(.90,.78),background_color=(0.04,0.03,0.05,.98),separator_color=(0.8,0.02,0.03,1))
        ok.bind(on_release=pop.dismiss); pop.open()
    def open_url(self,url):
'''
if anchor not in s: raise SystemExit("Run89 about insertion point not found")
s=s.replace(anchor,about,1)

# Dark/red content cards while retaining exact handlers/data.
s=s.replace('info=Button(text=f\'[b]{m.get("name")}[/b]  | ID: {m.get("address")} | Ver.: {m.get("version","1")}\',markup=True,size_hint_y=None,height=dp(44)',
'''info=Button(text=f'[b]{m.get("name")}[/b]  | ID: {m.get("address")} | Ver.: {m.get("version","1")}',markup=True,size_hint_y=None,height=dp(44),background_normal="",background_color=(0.07,0.065,0.08,1),color=(1,1,1,1)''')
s=s.replace('lbl=Button(text=f.get("label",""),halign="left",valign="middle",font_size="11sp",padding=(dp(2),0),disabled=True)',
'''lbl=Button(text=f.get("label",""),halign="left",valign="middle",font_size="11sp",padding=(dp(2),0),disabled=True,background_normal="",background_color=(0.055,0.05,0.065,1))''')
s=s.replace('a=Button(text=addr,size_hint_x=.30,font_name="Roboto",font_size="13sp",disabled=True);',
'''a=Button(text=addr,size_hint_x=.30,font_name="Roboto",font_size="13sp",disabled=True,background_normal="",background_color=(0.09,0.075,0.085,1));''')
s=s.replace('v=Button(text=rendered.strip(),markup=True,size_hint_x=.70,font_name="Roboto",font_size="14sp",disabled=True);',
'''v=Button(text=rendered.strip(),markup=True,size_hint_x=.70,font_name="Roboto",font_size="14sp",disabled=True,background_normal="",background_color=(0.045,0.04,0.052,1));''')

checks=["def about_popup(self,*_):","def toggle(self,f,active):","def open_document(self,*_):","def save_document(self,*_):","Run #89","Wolis11","drive2.ru/users/dim304","drive2.ru/users/wolis11"]
missing=[x for x in checks if x not in s]
if missing: raise SystemExit("Run89 post-patch verification failed: "+", ".join(missing))
p.write_text(s,encoding="utf-8")
print("Run89 Red Premium verified: Run88 #12 handlers preserved, red/dark shell + About popup installed.")
