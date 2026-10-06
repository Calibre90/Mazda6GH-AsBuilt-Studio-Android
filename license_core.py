# Run #70 Licensed client verifier.
# Public-key verification is intentionally kept separate from the admin signer.
# The admin private key must never be shipped in the client APK.
import base64, hashlib, re

def normalize_device_id(value):
    return re.sub(r"[^A-Z0-9]", "", str(value).upper())

def device_code(android_id):
    raw=normalize_device_id(android_id)
    digest=hashlib.sha256(("M6GH|"+raw).encode("utf-8")).hexdigest().upper()
    return "-".join(digest[i:i+4] for i in range(0,20,4))

# Public RSA key parameters are injected here before release.
RSA_E=65537
RSA_N=0

def license_message(device_code_value):
    return ("M6GH-LIFETIME|"+normalize_device_id(device_code_value)).encode("ascii")

def verify_activation(device_code_value,key):
    try:
        if RSA_N <= 0: return False
        raw=re.sub(r"[^A-Za-z0-9_-]","",str(key))
        sig=int.from_bytes(base64.urlsafe_b64decode(raw+"="*((4-len(raw)%4)%4)),"big")
        recovered=pow(sig,RSA_E,RSA_N)
        expected=int.from_bytes(hashlib.sha256(license_message(device_code_value)).digest(),"big")
        return recovered==expected
    except Exception:
        return False
