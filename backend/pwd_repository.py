import uuid
import time
from typing import Dict, Any, Optional

# Mock de banco de dados em memória
db_mock: Dict[str, Dict[str, Any]] = {}

def save_new_pwd(encrypted_pwd: str, view_limit: int, expiration_seconds: int) -> str:
    """
    Gera um UUID v4, calcula a expiração e persiste no mock.
    """
    pwd_id = str(uuid.uuid4())
    expiration_time = int(time.time()) + expiration_seconds
    
    db_mock[pwd_id] = {
        'pwd': encrypted_pwd,
        'viewCount': view_limit,
        'expirationDate': expiration_time
    }
    return pwd_id 

def get_by_pwd_id(pwd_id: str) -> Dict[str, Optional[Dict[str, Any]]]:
    """
    Busca a senha no dicionário global. 
    CORREÇÃO: Alterado de id_mock para db_mock para evitar NameError.
    """
    item = db_mock.get(pwd_id)
    return {'Item': item} if item else {}

def delete_by_pwd_id(pwd_id: str) -> None:
    """
    Remove o registro do mock de forma segura.
    """
    db_mock.pop(pwd_id, None)

def decrease_count_view(pwd_id: str, remaining_views: int) -> None:
    """
    Atualiza o contador de visualizações restantes.
    """
    if pwd_id in db_mock:
        db_mock[pwd_id]['viewCount'] = remaining_views