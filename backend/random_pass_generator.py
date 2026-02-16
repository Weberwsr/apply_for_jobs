import secrets
import string

def generate(use_letters: bool, use_digits: bool, use_punctuation: bool, length: int) -> str:
    """Gera uma senha aleatória com alta entropia usando o módulo secrets."""
    
    pool = ""
    if use_letters:
        pool += string.ascii_letters
    if use_digits:
        pool += string.digits
    if use_punctuation:
        pool += string.punctuation

    if not pool:
        pool = string.ascii_letters + string.digits 

    return ''.join(secrets.choice(pool) for _ in range(length)) 
