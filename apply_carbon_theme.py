from pathlib import Path

p = Path('main_base.py')
s = p.read_text(encoding='utf-8')

# Changed HEX symbols: red -> electric blue.
s = s.replace('[color=ff3333][b]{ch}[/b][/color]', '[color=2196F3][b]{ch}[/b][/color]')

# Carbon theme is applied at runtime without touching ABT/admin/business logic.
needle = 'from kivy.graphics import Color, Rectangle\n'
insert = '''from kivy.graphics import Color, Rectangle\nfrom kivy.lang import Builder\n\n# Run85 Carbon skin. Keep behavior identical to the verified Run84 core.\nBuilder.load_string(r\'\'\'\n<Button>:\n    background_normal: \'\'\n    background_down: \'\'\n    background_color: (0.075, 0.082, 0.09, 1) if self.state == \'normal\' else (0.03, 0.32, 0.58, 1)\n    color: (0.90, 0.94, 0.98, 1)\n<Label>:\n    color: (0.90, 0.94, 0.98, 1)\n<TextInput>:\n    background_normal: \'\'\n    background_active: \'\'\n    background_color: (0.055, 0.06, 0.07, 1)\n    foreground_color: (0.90, 0.94, 0.98, 1)\n    cursor_color: (0.13, 0.59, 0.95, 1)\n    hint_text_color: (0.48, 0.58, 0.68, 1)\n<TabbedPanelItem>:\n    background_normal: \'\'\n    background_down: \'\'\n    background_color: (0.07, 0.075, 0.085, 1) if self.state == \'normal\' else (0.03, 0.34, 0.62, 1)\n    color: (0.92, 0.96, 1, 1)\n\'\'\')\nWindow.clearcolor = (0.025, 0.028, 0.032, 1)\n'''
if needle not in s:
    raise SystemExit('graphics import anchor not found')
s = s.replace(needle, insert, 1)

# Carbon weave backdrop: subtle checker weave behind controls.
anchor = '        super().__init__(orientation="vertical",spacing=dp(3),padding=(dp(7),dp(28),dp(7),dp(7)),**kw); self.app=App.get_running_app();'
replacement = '''        super().__init__(orientation="vertical",spacing=dp(3),padding=(dp(7),dp(28),dp(7),dp(7)),**kw); self.app=App.get_running_app();\n        with self.canvas.before:\n            Color(0.025,0.028,0.032,1); self._carbon_bg=Rectangle(pos=self.pos,size=self.size)\n            Color(0.055,0.06,0.068,1); self._carbon_a=Rectangle(pos=self.pos,size=(self.width,dp(2)))\n            Color(0.035,0.04,0.047,1); self._carbon_b=Rectangle(pos=(self.x,self.y+dp(4)),size=(self.width,dp(2)))\n        def _carbon_sync(*_):\n            self._carbon_bg.pos=self.pos; self._carbon_bg.size=self.size\n            self._carbon_a.pos=(self.x,self.y); self._carbon_a.size=(self.width,dp(2))\n            self._carbon_b.pos=(self.x,self.y+dp(4)); self._carbon_b.size=(self.width,dp(2))\n        self.bind(pos=_carbon_sync,size=_carbon_sync);'''
if anchor not in s:
    raise SystemExit('Main init anchor not found')
s = s.replace(anchor, replacement, 1)

p.write_text(s, encoding='utf-8')
print('Run85 Carbon theme applied')
print('blue HEX:', '[color=2196F3]' in s)
print('admin login preserved:', 'admin_login' in s)
print('ABT parser preserved:', 'def parse_abt' in s)
