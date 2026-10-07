from pathlib import Path
p=Path('main_base.py')
s=p.read_text(encoding='utf-8')
# Carbon palette and blue HEX highlight
s=s.replace('"background":"#f2f2f2","panel":"#fff7f2"','"background":"#080a0c","panel":"#171a1d"')
s=s.replace('[color=ff3333]','[color=00A8FF]')
# replace old header author/link area with compact info button + admin
old='self.header=BoxLayout(size_hint_y=None,height=dp(42),spacing=dp(2)); self.header.add_widget(Widget()); self.title_label=Label(text=self.app.data.get("ui",{}).get("author_text","КТО СДЕЛАЛ ПРОГРАММУ"),font_size="13sp",halign="right",valign="middle",size_hint_x=None,width=dp(150)); self.title_label.bind(size=lambda inst,val:setattr(inst,"text_size",(val[0],val[1]))); self.header.add_widget(self.title_label); self.header_links=BoxLayout(size_hint_x=None,width=dp(92),spacing=dp(2)); self.header.add_widget(self.header_links)\n        ab=Button(text=self.app.data.get("ui",{}).get("admin_text","⚙"),size_hint_x=None,width=dp(52)); ab.bind(on_release=self.admin_login); self.header.add_widget(ab); self.add_widget(self.header)'
new='self.header=BoxLayout(size_hint_y=None,height=dp(50),spacing=dp(6)); self.brand_label=Label(text="[b]MAZDA 6 GH[/b]   AS BUILT STUDIO",markup=True,font_size="14sp",halign="left",valign="middle"); self.brand_label.bind(size=lambda inst,val:setattr(inst,"text_size",val)); self.header.add_widget(self.brand_label); ib=Button(text="ⓘ",font_size="24sp",size_hint_x=None,width=dp(52),background_normal="",background_color=(.32,.02,.02,1),color=(1,.25,.20,1)); ib.bind(on_release=self.show_about); self.header.add_widget(ib); ab=Button(text=self.app.data.get("ui",{}).get("admin_text","⚙"),font_size="20sp",size_hint_x=None,width=dp(52),background_normal="",background_color=(.18,.02,.02,1),color=(1,.3,.25,1)); ab.bind(on_release=self.admin_login); self.header.add_widget(ab); self.add_widget(self.header)'
s=s.replace(old,new)
# refresh no longer references removed title/header_links
s=s.replace('self.title_label.text=self.app.data.get("ui",{}).get("author_text","КТО СДЕЛАЛ ПРОГРАММУ"); self.refresh_author(); self.tabholder.clear_widgets();','self.tabholder.clear_widgets();')
# make legacy refresh_author harmless
start=s.find('    def refresh_author(self):')
end=s.find('    def open_url(self,url):', start)
if start!=-1 and end!=-1:
    s=s[:start]+'    def refresh_author(self):\n        pass\n'+s[end:]
# carbonize common buttons globally inside Main after init setup
needle='        self.stat=Label(text=self.status,size_hint_y=None,height=dp(28),font_size="12sp"); self.add_widget(self.stat); self.refresh()'
replacement='        self.stat=Label(text=self.status,size_hint_y=None,height=dp(28),font_size="12sp",color=(.82,.84,.86,1)); self.add_widget(self.stat)\n        with self.canvas.before:\n            Color(.025,.03,.035,1); self._carbon_bg=Rectangle(pos=self.pos,size=self.size)\n        self.bind(pos=lambda *_:setattr(self._carbon_bg,"pos",self.pos),size=lambda *_:setattr(self._carbon_bg,"size",self.size))\n        self.refresh()'
s=s.replace(needle,replacement)
# Insert about dialog before admin_login
marker='    def admin_login(self,*_):'
about='''    def show_about(self,*_):\n        ui=self.app.data.setdefault("ui",{})\n        box=BoxLayout(orientation="vertical",spacing=dp(8),padding=dp(14))\n        title=Label(text=f'[b]{ui.get("about_product","Mazda 6 GH")}[/b]\\n[b]{ui.get("about_studio","AS BUILT STUDIO")}[/b]\\n[color=aaaaaa]{ui.get("about_android","Android версия")}[/color]',markup=True,font_size="20sp",size_hint_y=None,height=dp(105),halign="center")\n        box.add_widget(title)\n        box.add_widget(Label(text='[b]'+ui.get("about_dev_title","Разработчик")+'[/b]',markup=True,size_hint_y=None,height=dp(30),halign="left"))\n        d=Button(text=ui.get("about_dev_name","Dim304")+'\\n[color=00A8FF]'+ui.get("about_dev_url","https://www.drive2.ru/users/dim304/")+'[/color]',markup=True,size_hint_y=None,height=dp(62),background_normal="",background_color=(.08,.09,.10,1)); d.bind(on_release=lambda *_:self.open_url(ui.get("about_dev_url",""))); box.add_widget(d)\n        box.add_widget(Label(text='[b]'+ui.get("about_support_title","Дополнительная поддержка")+'[/b]',markup=True,size_hint_y=None,height=dp(30),halign="left"))\n        w=Button(text=ui.get("about_support_name","Wolis11")+'\\n[color=00A8FF]'+ui.get("about_support_url","https://www.drive2.ru/users/wolis11/")+'[/color]',markup=True,size_hint_y=None,height=dp(62),background_normal="",background_color=(.08,.09,.10,1)); w.bind(on_release=lambda *_:self.open_url(ui.get("about_support_url",""))); box.add_widget(w)\n        box.add_widget(Label(text=ui.get("about_version","Версия: 1.0.0 (STUDIO)")+'\\n'+ui.get("about_build","Сборка: Run #86"),color=(.7,.72,.74,1),size_hint_y=None,height=dp(54)))\n        ok=Button(text="OK",size_hint_y=None,height=dp(50),background_normal="",background_color=(.35,.02,.02,1),color=(1,.3,.25,1)); box.add_widget(ok)\n        pop=Popup(title="ⓘ  О программе",content=box,size_hint=(.92,.82),separator_color=(.75,.05,.04,1)); ok.bind(on_release=pop.dismiss); pop.open()\n\n'''
s=s.replace(marker,about+marker)
# Admin: add editable about fields into existing appearance form
oldloop='("ready_text","Текст статуса")'
newloop='("ready_text","Текст статуса"),("about_product","О программе: Mazda 6 GH"),("about_studio","О программе: AS BUILT STUDIO"),("about_android","О программе: Android версия"),("about_dev_title","Заголовок разработчика"),("about_dev_name","Имя разработчика"),("about_dev_url","Ссылка разработчика"),("about_support_title","Заголовок поддержки"),("about_support_name","Имя поддержки"),("about_support_url","Ссылка поддержки"),("about_version","Строка версии"),("about_build","Строка сборки")'
s=s.replace(oldloop,newloop)
# Defaults are supplied lazily by dialog, but persist standard values on fresh settings
p.write_text(s,encoding='utf-8')
