import re

def validate_password(use_letters: bool, use_digits: bool, use_punctuation: bool, length: int, password: str) -> bool:
    """Valida se a senha inserida atende aos critérios de segurança exigidos."""
    
    # Verifica tamanho mínimo
    if len(password) < length:
        return False
    
    # Validações com Regex (Expressões Regulares)
    if use_letters and not re.search(r'[a-zA-Z]', password):
        return False
    if use_digits and not re.search(r'\d', password):
        return False
    if use_punctuation and not re.search(r'[^\w\s]', password):
        return False
        
    return True