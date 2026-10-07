from pathlib import Path
p=Path("main_base.py")
s=p.read_text(encoding="utf-8")
required=["class Main(BoxLayout):","def refresh(self):","def toggle(self,f,active):","def open_document(self,*_):","def save_document(self,*_):"]
missing=[x for x in required if x not in s]
if missing: raise SystemExit("Golden Run88 core verification failed: "+", ".join(missing))

# Run89 Premium UI: visual shell only; working ABT/toggle/save logic stays intact.
s=s.replace('Window.softinput_mode="below_target"','Window.softinput_mode="below_target"; Window.clearcolor=(0.015,0.035,0.055,1)')
s=s.replace('"open_text":"Open As-Built file","save_text":"Save As-Built file"','"open_text":"📂  Открыть ABT","save_text":"💾  Сохранить ABT"')
s=s.replace('"admin_text":"⚙","author_text":"КТО СДЕЛАЛ ПРОГРАММУ"','"admin_text":"⚙","author_text":"MAZDA 6 GH  •  AS BUILT STUDIO"')
# Add visible placeholders only: no guessed HEX mapping, so they cannot alter vehicle data.
needle='{"id":"new_feature","module":"IC","label":"Новая функция","row":"720-01-01","mode":"HEX","hex_indices":"2,3","on":"40","off":"00","status":"НЕ ПРОВЕРЕНО"},'
extra=needle+'{"id":"tpms_pending","module":"IC","label":"TPMS / давление в шинах  •  ожидает адрес","row":"__UNMAPPED__","mode":"HEX","hex_indices":"0","on":"0","off":"0","status":"НЕ ПОДКЛЮЧЕНО"},{"id":"afs_pending","module":"IC","label":"AFS / адаптивный свет  •  ожидает адрес","row":"__UNMAPPED__","mode":"HEX","hex_indices":"0","on":"0","off":"0","status":"НЕ ПОДКЛЮЧЕНО"},{"id":"dsc_pending","module":"IC","label":"DSC / стабилизация  •  ожидает адрес","row":"__UNMAPPED__","mode":"HEX","hex_indices":"0","on":"0","off":"0","status":"НЕ ПОДКЛЮЧЕНО"},'
s=s.replace(needle,extra)
# Premium dark/navy buttons and panels, preserving callbacks.
s=s.replace('ab=Button(text=self.app.data.get("ui",{}).get("admin_text","⚙"),size_hint_x=None,width=dp(52))','ab=Button(text=self.app.data.get("ui",{}).get("admin_text","⚙"),size_hint_x=None,width=dp(52),background_normal="",background_color=(0.03,0.32,0.68,1),color=(1,1,1,1))')
s=s.replace('ob=Button(text=ui.get("open_text","Open As-Built file")); sb=Button(text=ui.get("save_text","Save As-Built file"))','ob=Button(text=ui.get("open_text","Open As-Built file"),background_normal="",background_color=(0.02,0.28,0.62,1),color=(1,1,1,1)); sb=Button(text=ui.get("save_text","Save As-Built file"),background_normal="",background_color=(0.02,0.28,0.62,1),color=(1,1,1,1))')
s=s.replace('b=Button(text="Dim304",font_size="11sp",padding=(dp(2),dp(2)))','b=Button(text="ⓘ",font_size="18sp",padding=(dp(2),dp(2)),background_normal="",background_color=(0.02,0.28,0.62,1),color=(1,1,1,1))')
p.write_text(s,encoding="utf-8")
print("Run89 Premium UI applied; golden handlers preserved; TPMS/AFS/DSC placeholders are unmapped and safe.")

# build-trigger: run89-1

# registered-workflow-trigger
