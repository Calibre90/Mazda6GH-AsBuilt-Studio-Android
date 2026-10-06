import hashlib, hmac, re

# Run #22 offline licensing. Keep this value identical in the admin generator.
# This is intentionally separate from the UI so it can later be replaced by public-key signatures.
_LICENSE_SECRET = b"M6GH-R22-2026-OFFLINE-9F4C2A7D"

def normalize_device_id(value):
    return re.sub(r"[^A-Z0-9]", "", str(value).upper())

def device_code(android_id):
    raw = normalize_device_id(android_id)
    digest = hashlib.sha256(("M6GH|" + raw).encode("utf-8")).hexdigest().upper()
    return "-".join(digest[i:i+4] for i in range(0, 20, 4))

def activation_key(device_code_value):
    dc = normalize_device_id(device_code_value)
    sig = hmac.new(_LICENSE_SECRET, dc.encode("ascii"), hashlib.sha256).hexdigest().upper()[:24]
    return "M6GH-" + "-".join(sig[i:i+4] for i in range(0, 24, 4))

def verify_activation(device_code_value, key):
    expected = activation_key(device_code_value)
    supplied = str(key).strip().upper()
    return hmac.compare_digest(expected, supplied)
