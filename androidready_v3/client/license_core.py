import hashlib, hmac, re
_LICENSE_SECRET=b"M6GH-R22-2026-OFFLINE-9F4C2A7D"
def normalize_device_id(v): return re.sub(r'[^A-Z0-9]','',str(v).upper())
def device_code(android_id):
 raw=("M6GH|"+normalize_device_id(android_id)).encode('utf-8')
 h=hashlib.sha256(raw).hexdigest().upper()
 return '-'.join(h[i:i+5] for i in range(0,20,5))
def activation_key(dc):
 dc=str(dc).strip().upper()
 sig=hmac.new(_LICENSE_SECRET,dc.encode('ascii'),hashlib.sha256).hexdigest().upper()
 return '-'.join(sig[i:i+5] for i in range(0,25,5))
def verify_activation(dc,key):
 return hmac.compare_digest(activation_key(dc),str(key).strip().upper())
