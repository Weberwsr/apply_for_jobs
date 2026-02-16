from cryptography.fernet import Fernet
import os

DEFAULT_KEY =  b'7P6p_vK0-X1VfR9qG_L2jK5mN8oP3qR6tU9vW2xYzA0='

def encrypt_data(data: str) -> str:
    """Criptografa a senha antes de salvar no banco"""

    key = os.environ.get('CRYPTO_KEY', DEFAULT_KEY)
    f = Fernet(key)

    return f.encrypt(data.encode()).decode()

def decrypt_data(token: str) -> str:
    """Discriptografar a senha para o usuário"""
    key = os.environ.get('CRYPTO_KEY', DEFAULT_KEY)
    f = Fernet(key)
    return f.decrypt(token.encode()).decode()