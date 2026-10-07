from pathlib import Path
p=Path('main_base.py')
s=p.read_text(encoding='utf-8')
s=s.replace('from kivy.graphics import Color, Rectangle','from kivy.graphics import Color, Rectangle, RoundedRectangle, Line')
insert='''\nclass CarbonPanel(BoxLayout):\n    def __init__(self, **kw):\n        super().__init__(**kw)\n        with self.canvas.before:\n            Color(.025,.028,.032,1); self.bg=RoundedRectangle(pos=self.pos,size=self.size,radius=[dp(10)])\n            Color(.20,.21,.22,1); self.edge=Line(rounded_rectangle=(self.x,self.y,self.width,self.height,dp(10)),width=1.2)\n            Color(.34,.02,.02,.45); self.rededge=Line(rounded_rectangle=(self.x+dp(2),self.y+dp(2),max(0,self.width-dp(4)),max(0,self.height-dp(4)),dp(8)),width=.8)\n        self.bind(pos=self._sync,size=self._sync)\n    def _sync(self,*_):\n        self.bg.pos=self.pos; self.bg.size=self.size; self.edge.rounded_rectangle=(self.x,self.y,self.width,self.height,dp(10)); self.rededge.rounded_rectangle=(self.x+dp(2),self.y+dp(2),max(0,self.width-dp(4)),max(0,self.height-dp(4)),dp(8))\n\nclass CarbonButton(Button):\n    def __init__(self, active=False, **kw):\n        super().__init__(background_normal='',background_down='',background_color=(0,0,0,0),color=(.94,.94,.94,1),**kw); self.active=active\n        with self.canvas.before:\n            Color(.055,.06,.065,1); self.bg=RoundedRectangle(pos=self.pos,size=self.size,radius=[dp(7)]); self.rc=Color(1,.08,.04,.9 if active else .5); self.line=Line(rounded_rectangle=(self.x,self.y,self.width,self.height,dp(7)),width=1.5 if active else 1.0)\n        self.bind(pos=self._sync,size=self._sync,state=self._state)\n    def _sync(self,*_): self.bg.pos=self.pos; self.bg.size=self.size; self.line.rounded_rectangle=(self.x,self.y,self.width,self.height,dp(7))\n    def _state(self,*_): self.rc.a=1 if self.state=='down' or self.active else .5\n\nclass CarbonHexRow(BoxLayout):\n    def __init__(self, **kw):\n        super().__init__(orientation='horizontal',spacing=dp(2),padding=dp(3),**kw)\n        with self.canvas.before:\n            Color(.045,.05,.055,1); self.bg=RoundedRectangle(pos=self.pos,size=self.size,radius=[dp(5)]); Color(.23,.24,.25,1); self.l=Line(rounded_rectangle=(self.x,self.y,self.width,self.height,dp(5)),width=1)\n        self.bind(pos=self._sync,size=self._sync)\n    def _sync(self,*_): self.bg.pos=self.pos;self.bg.size=self.size;self.l.rounded_rectangle=(self.x,self.y,self.width,self.height,dp(5))\n'''
s=s.replace('class Main(BoxLayout):',insert+'\nclass Main(BoxLayout):')
s=s.replace('[color=ff3333]','[color=00A8FF]')
start=s.index('    def __init__(self,**kw):',s.index('class Main(BoxLayout):'))
end=s.index('    def set_status(',start)
new='''    def __init__(self,**kw):\n        super().__init__(orientation="vertical",spacing=dp(7),padding=dp(10),**kw)\n        self.app=App.get_running_app(); self.changed={}; self.changed_positions={}; self.original_values={r.get("address"):norm(r.get("value","")) for r in self.app.data.get("rows",[])}; self.tabs=None; self.pending_save_module=None; self.active_module_id=self.app.data.get("modules",[{"id":"IC"}])[0].get("id","IC"); self.feature_active={}; self.feature_baselines={}; self.row_feature_baselines={}; self.status=self.app.data.get("ui",{}).get("ready_text","Готово"); self.checks={}\n        with self.canvas.before:\n            Color(.012,.014,.016,1); self.carbon=Rectangle(pos=self.pos,size=self.size)\n        self.bind(pos=lambda *_:setattr(self.carbon,"pos",self.pos),size=lambda *_:setattr(self.carbon,"size",self.size))\n        top=CarbonPanel(size_hint_y=None,height=dp(62),padding=dp(8),spacing=dp(8)); brand=Label(text="[b]MAZDA 6 GH[/b]\\n[color=aaaaaa]AS BUILT STUDIO[/color]",markup=True,font_size="16sp",halign="left",valign="middle"); brand.bind(size=lambda w,v:setattr(w,"text_size",v)); top.add_widget(brand); info=CarbonButton(text="ⓘ",font_size="24sp",size_hint_x=None,width=dp(58)); info.bind(on_release=self.show_about); top.add_widget(info); admin=CarbonButton(text="⚙",font_size="22sp",size_hint_x=None,width=dp(58)); admin.bind(on_release=self.admin_login); top.add_widget(admin); self.add_widget(top)\n        self.tabholder=BoxLayout(size_hint_y=None,height=dp(52),spacing=dp(5)); self.add_widget(self.tabholder); self.body=CarbonPanel(orientation="vertical",padding=dp(9),spacing=dp(7)); self.add_widget(self.body)\n        actions=BoxLayout(size_hint_y=None,height=dp(58),spacing=dp(8)); ob=CarbonButton(text=self.app.data.get("ui",{}).get("open_text","OPEN AS-BUILT"),font_size="15sp"); sb=CarbonButton(text=self.app.data.get("ui",{}).get("save_text","SAVE AS-BUILT"),font_size="15sp"); ob.bind(on_release=self.open_document); sb.bind(on_release=self.save_document); actions.add_widget(ob);actions.add_widget(sb);self.add_widget(actions)\n        self.author_bar=BoxLayout(size_hint_y=None,height=dp(1)); self.header_links=BoxLayout(size_hint_y=None,height=dp(1)); self.title_label=Label(text='',size_hint_y=None,height=dp(1)); self.stat=Label(text=self.status,size_hint_y=None,height=dp(27),font_size="11sp",color=(.72,.72,.72,1));self.add_widget(self.stat);self.refresh()\n\n    def refresh_author(self): pass
    def refresh(self):
        keep_tab=self.active_module_id
        self.tabholder.clear_widgets()
        mods=self.app.data.get("modules",[])
        tab_w=min(dp(68),(Window.width-dp(14))/max(1,len(mods)))
        tabs=TabbedPanel(do_default_tab=False,tab_height=dp(36),tab_width=tab_w)
        self.tabs=tabs
        for m in mods:
            ti=TabbedPanelItem(text=m["id"],font_size="11sp")
            ti.bind(on_release=lambda tab:self._remember_tab(tab.text))
            scroll=ScrollView()
            content=BoxLayout(orientation="vertical",size_hint_y=None,spacing=dp(5),padding=dp(5))
            content.bind(minimum_height=content.setter("height"))
            info=CarbonButton(text=f'[b]{m.get("name")}[/b]  | ID: {m.get("address")} | Ver.: {m.get("version","1")}',markup=True,size_hint_y=None,height=dp(44),font_size="11sp")
            content.add_widget(info)
            feats=[x for x in self.app.data.get("features",[]) if x.get("module")==m["id"]]
            if feats:
                cols=max(1,int(self.app.data.get("ui",{}).get("feature_columns",2)))
                grid=GridLayout(cols=cols,size_hint_y=None,spacing=dp(1),row_default_height=dp(34),row_force_default=True)
                grid.bind(minimum_height=grid.setter("height"))
                for f in feats:
                    line=BoxLayout(size_hint_y=None,height=dp(34),spacing=0)
                    cb=CheckBox(size_hint_x=None,width=dp(30))
                    fk=f.get("id") or (str(f.get("module"))+"|"+str(f.get("row"))+"|"+str(f.get("label")))
                    actual=self.feature_state(f)
                    self.feature_active[fk]=actual if fk not in self.feature_active else self.feature_active[fk]
                    cb.active=bool(self.feature_active[fk])
                    cb.bind(active=lambda _c,val,ff=f:self.toggle(ff,val))
                    line.add_widget(cb)
                    lbl=CarbonButton(text=f.get("label",""),halign="left",valign="middle",font_size="11sp")
                    lbl.bind(size=lambda inst,val:setattr(inst,"text_size",(max(dp(10),val[0]-dp(4)),val[1])))
                    line.add_widget(lbl); grid.add_widget(line)
                content.add_widget(grid)
            for r in [x for x in self.app.data.get("rows",[]) if x.get("module")==m["id"]]:
                raw=norm(r.get("value","")); pos=set(self.changed_positions.get(r["address"],set()))
                for ff in feats:
                    if ff.get("row")==r["address"] and self.feature_active.get(ff.get("id") or (str(ff.get("module"))+"|"+str(ff.get("row"))+"|"+str(ff.get("label"))),False):
                        try:
                            if str(ff.get("mode","HEX")).upper()=="BITS":
                                bi=int(ff.get("byte_index",0)); pos.update((bi*2,bi*2+1))
                            else: pos.update(parse_indices(ff.get("hex_indices",0)))
                        except Exception: pass
                rendered=""
                for i,ch in enumerate(raw):
                    rendered += (f'[color=00A8FF][b]{ch}[/b][/color]' if i in pos else ch)
                    rendered += (" " if i%4==3 else "")
                row=CarbonHexRow(size_hint_y=None,height=dp(40))
                addr=Label(text='[b]'+r["address"]+'[/b]',markup=True,size_hint_x=.30,font_size="13sp")
                val=Label(text=rendered.strip(),markup=True,size_hint_x=.70,font_size="14sp")
                row.add_widget(addr); row.add_widget(val); content.add_widget(row)
            scroll.add_widget(content); ti.add_widget(scroll); tabs.add_widget(ti)
        self.body.clear_widgets()
        self.body.add_widget(tabs)
        if keep_tab:
            Clock.schedule_once(lambda _dt,k=keep_tab:self._restore_tab(k),0)
    def _remember_tab(self,tab_id): self.active_module_id=tab_id
    def _restore_tab(self,tab_id):
        if not self.tabs:return
        target=next((t for t in self.tabs.tab_list if t.text==tab_id),None)
        if target:self.tabs.switch_to(target);self.active_module_id=tab_id

