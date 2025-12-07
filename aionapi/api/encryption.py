# encryption.py
from cryptography.fernet import Fernet
from django.conf import settings

fernet = Fernet(settings.FERNET_KEY.encode())

def encrypt_token(str_token: str) -> str:
    return fernet.encrypt(str_token.encode()).decode()

def decrypt_token(str_encrypted_token: str) -> str:
    return fernet.decrypt(str_encrypted_token.encode()).decode()
