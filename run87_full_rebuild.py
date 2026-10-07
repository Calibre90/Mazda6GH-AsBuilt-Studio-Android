from pathlib import Path
# FIX7: do not replace the proven Run84 Main UI at all.
# The workflow already assembles and SHA-verifies the exact golden Run84 source.
p=Path("main_base.py")
s=p.read_text(encoding="utf-8")
required=["class Main(BoxLayout):","def refresh(self):","def toggle(self,f,active):","def open_document(self,*_):","def save_document(self,*_):"]
missing=[x for x in required if x not in s]
if missing:
    raise SystemExit("Golden Run84 UI verification failed: "+", ".join(missing))
print("FIX7: exact golden Run84 Main renderer preserved; no Carbon UI patch applied")
