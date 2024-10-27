from flask_jwt_extended import get_jwt_identity
import re
import os

def get_current_user_id():
    # Obtener el ID del usuario a partir token de acceso
    if os.getenv('FLASK_ENV') == 'testing':
        current_user_id = 1
    else:
        current_user_id = get_jwt_identity()
    return current_user_id

def replace_parameters(text, parameters):
    for i, param in enumerate(parameters, 1):
        placeholder = f"##param{i}##"
        text = re.sub(placeholder, param, text)
    return text
