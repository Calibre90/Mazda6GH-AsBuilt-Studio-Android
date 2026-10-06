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
RSA_N=22673276078073802685707298463770369337852563532100005637400495351697895608685910147007410584905524630361582164471103710313278161575910661477143980407300271697058747997713121485549478130043317473995845296759926640208581625694895434324386994464061376620806408769102227198916808028744365704006296118437489107688560116176141243367480627546547612328922590470541953439967357256258908982035230903602066411544748698932026301974381681950007938726023442096890840110857546168563275338477431825765239096991575528772779495261293140414900448989324579546180304459496471432082201782737600736188959668499123128490664132407953900331343

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
