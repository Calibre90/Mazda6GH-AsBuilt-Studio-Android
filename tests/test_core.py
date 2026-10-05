import ast
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / 'main.py'
TREE = ast.parse(SRC.read_text(encoding='utf-8'))
WANTED = {'norm','decode_abt_index','encode_abt_index','address_parts','checksum_for','recalc','parse_indices','parse_abt'}
BODY = [n for n in TREE.body if isinstance(n, (ast.Import, ast.ImportFrom)) and any(a.name in {'json','re','hashlib','os'} for a in n.names)]
BODY += [n for n in TREE.body if isinstance(n, ast.FunctionDef) and n.name in WANTED]
MOD = ast.Module(body=BODY, type_ignores=[])
ns = {}
exec(compile(MOD, str(SRC), 'exec'), ns)

def test_abt_compact_and_spaced():
    modules=[{'id':'IC','address':'720'}]
    text='720G1G11F407126809F\n720-G1-G2 000E F255 E766\n'
    rows=ns['parse_abt'](text, modules)
    assert len(rows)==2
    assert rows[0]['address']=='720-01-01'
    assert rows[1]['address']=='720-01-02'
    assert rows[0]['value']=='1F40 7126 809F'

def test_index_roundtrip():
    for n in (0,1,15,16,31,255):
        assert ns['decode_abt_index'](ns['encode_abt_index'](n)) == n

def test_indices():
    assert ns['parse_indices']('0,2-4;7') == [0,2,3,4,7]

def test_checksum_recalc_changes_last_byte_only():
    row={'address':'720-01-01','value':'1F40 7126 8000'}
    before=ns['norm'](row['value'])
    ns['recalc'](row)
    after=ns['norm'](row['value'])
    assert after[:-2] == before[:-2]
    assert after[-2:] == ns['checksum_for']('720-01-01', before[:-2])
