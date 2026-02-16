from flask import Flask, request, jsonify
from flask_cors import CORS
import random_pass_generator as generator 
import sended_password_validation as validator 
import pwd_repository as repository 
import crypto
import time

app = Flask(__name__)

CORS(app)


DEFAULT_EXPIRATION = 3600
MIN_PASSWORD_LENGTH = 12

@app.route('/pwd', methods=['POST'])
def create_password():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Corpo da requisição inválido (JSON esperado)."}), 400

    user_password = data.get('password', '').strip()
    
    # 1. GERAÇÃO OU VALIDAÇÃO
    if not user_password:
        final_password = generator.generate(True, True, True, MIN_PASSWORD_LENGTH)
    else:
        is_valid = validator.validate_password(True, True, True, MIN_PASSWORD_LENGTH, user_password)
        if not is_valid:
            return jsonify({
                "error": f"Política de Segurança: A senha deve ter no mínimo {MIN_PASSWORD_LENGTH} caracteres e incluir letras, números e símbolos."
            }), 400
        final_password = user_password

    # 2. PROCESSAMENTO E PERSISTÊNCIA
    try:
        encrypted_pwd = crypto.encrypt_data(final_password)
        view_limit = data.get('viewLimit', 1)
        expiration = data.get('expirationSeconds', DEFAULT_EXPIRATION)
        
        pwd_id = repository.save_new_pwd(encrypted_pwd, view_limit, expiration)
        
        return jsonify({"id": pwd_id, "message": "Senha validada e salva."}), 201
    except Exception as e:
        return jsonify({"error": "Erro interno ao processar segurança."}), 500

@app.route('/pwd/<pwd_id>', methods=['GET'])
def get_password(pwd_id):
    result = repository.get_by_pwd_id(pwd_id)
    item = result.get('Item')

    # 1. VERIFICAÇÃO DE EXISTÊNCIA E EXPIRAÇÃO
    if not item:
        return jsonify({"error": "Senha não encontrada."}), 404
        
    if int(time.time()) > item['expirationDate']:
        repository.delete_by_pwd_id(pwd_id)
        return jsonify({"error": "Esta senha expirou."}), 404

    # 2. DESCRIPTOGRAFIA E LOGICA DE VISUALIZAÇÃO
    try:
        decrypted_password = crypto.decrypt_data(item['pwd'])
        new_count = item['viewCount'] - 1
        
        if new_count <= 0:
            repository.delete_by_pwd_id(pwd_id)
        else:
            repository.decrease_count_view(pwd_id, new_count)

        return jsonify({
            "password": decrypted_password, 
            "views_remaining": max(0, new_count)
        }), 200
    except Exception:
        return jsonify({"error": "Erro ao recuperar dados seguros."}), 500

if __name__ == '__main__':
    app.run(debug=True)