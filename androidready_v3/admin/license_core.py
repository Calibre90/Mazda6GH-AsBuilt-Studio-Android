import hashlib,hmac,re
_LICENSE_SECRET=b"M6GH-R22-2026-OFFLINE-9F4C2A7D"
def activation_key(dc):
 dc=str(dc).strip().upper(); sig=hmac.new(_LICENSE_SECRET,dc.encode('ascii'),hashlib.sha256).hexdigest().upper(); return '-'.join(sig[i:i+5] for i in range(0,25,5))
