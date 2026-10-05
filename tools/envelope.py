"""제출 파일 암호화 (RSA-OAEP + AES-GCM).

공개키로 잠근 파일은 채점 서버의 개인키로만 열 수 있다.
fork 저장소는 누구나 볼 수 있지만, 암호화된 submission.enc 의 내용은 다른 학생이 볼 수 없다.
"""
import base64
import json
import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

_OAEP = padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)


def encrypt(data: bytes, public_key_pem: bytes) -> bytes:
    pub = serialization.load_pem_public_key(public_key_pem)
    key = AESGCM.generate_key(bit_length=256)
    nonce = os.urandom(12)
    ct = AESGCM(key).encrypt(nonce, data, None)
    env = {"v": 1, "ek": base64.b64encode(pub.encrypt(key, _OAEP)).decode(),
           "nonce": base64.b64encode(nonce).decode(), "ct": base64.b64encode(ct).decode()}
    return json.dumps(env).encode()


def decrypt(blob: bytes, private_key_pem: bytes) -> bytes:
    env = json.loads(blob)
    priv = serialization.load_pem_private_key(private_key_pem, password=None)
    key = priv.decrypt(base64.b64decode(env["ek"]), _OAEP)
    return AESGCM(key).decrypt(base64.b64decode(env["nonce"]), base64.b64decode(env["ct"]), None)
