import base64
import hashlib
import re

RSA_E = 65537
RSA_N = 22673276078073802685707298463770369337852563532100005637400495351697895608685910147007410584905524630361582164471103710313278161575910661477143980407300271697058747997713121485549478130043317473995845296759926640208581625694895434324386994464061376620806408769102227198916808028744365704006296118437489107688560116176141243367480627546547612328922590470541953439967357256258908982035230903602066411544748698932026301974381681950007938726023442096890840110857546168563275338477431825765239096991575528772779495261293140414900448989324579546180304459496471432082201782737600736188959668499123128490664132407953900331343

_SHA256_DER = bytes.fromhex("3031300d060960864801650304020105000420")

def device_code(android_id):
    raw=("M6GH84|"+str(android_id)).encode("utf-8")
    h=hashlib.sha256(raw).hexdigest().upper()
    return "-".join((h[:5],h[5:10],h[10:15],h[15:20]))

def license_message(code):
    clean=re.sub(r"[^A-Z0-9-]","",str(code).upper())
    return ("M6GH-RUN84-LIFETIME|"+clean).encode("utf-8")

def _emsa(message,k):
    digest=hashlib.sha256(message).digest()
    t=_SHA256_DER+digest
    if k < len(t)+11:
        raise ValueError("RSA key too short")
    return b"\x00\x01"+b"\xff"*(k-len(t)-3)+b"\x00"+t

def verify_activation(code,key):
    try:
        token=re.sub(r"\s+","",str(key))
        token += "="*((4-len(token)%4)%4)
        sig=base64.urlsafe_b64decode(token.encode("ascii"))
        k=(RSA_N.bit_length()+7)//8
        if len(sig)!=k:return False
        recovered=pow(int.from_bytes(sig,"big"),RSA_E,RSA_N).to_bytes(k,"big")
        return recovered==_emsa(license_message(code),k)
    except Exception:
        return False
