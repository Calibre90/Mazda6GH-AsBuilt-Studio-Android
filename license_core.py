import base64
import hashlib
import re

LICENSE_SCHEME = "M6GH-RUN84-LIFETIME-PKCS1-SHA256"
RSA_E = 65537
RSA_N = int("22248895552979762047984411655976931923360516625196253486827222381729885632478344007813360072737376213002061761429196620496014294722594228439204808448910135613442035083939988141118862386363451404758224242934862468293458518238745138679079659922088153395190591451272181114160065967647868758325671135921124831883010180253315693007383813247345747665807098596614250770268781544282479988857578182396334294624311120826585234272506476548709597878410927544681122202541397715116485655488314820172016947303057953195405180135084620112882143198889436447481998314097133723111760266476887380249558453950989062461099873324991148619861")

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
