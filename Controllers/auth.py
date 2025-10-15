from flask import current_app
from werkzeug.security import check_password_hash
import bcrypt
import jwt
from datetime import datetime, timedelta
from config import get_db_connection


def crear_token(usuario, secret_key, horas=24):
    payload = {
        "usuario": usuario,
        "exp": datetime.utcnow() + timedelta(hours=horas)
    }
    return jwt.encode(payload, secret_key, algorithm="HS256")

def login_usuario(email, password, db):
    cursor = db.cursor(dictionary=True)

    # 1️⃣ Buscar en estudiantes
    cursor.execute("SELECT * FROM estudiantes WHERE email=%s", (email,))
    usuario = cursor.fetchone()
    tipo = "estudiante"

    # 2️⃣ Si no está, buscar en personal
    if not usuario:
        cursor.execute("SELECT * FROM personal WHERE email=%s", (email,))
        usuario = cursor.fetchone()
        tipo = "personal"

    if not usuario:
        return None, "Usuario no encontrado"

    # 3️⃣ Verificar contraseña
    if tipo == "estudiante":
        # Usuarios estudiantes usan werkzeug
        if not check_password_hash(usuario["password"], password):
            return None, "Contraseña incorrecta"
    else:
        # Usuarios personal usan bcrypt
        if not bcrypt.checkpw(password.encode('utf-8'), usuario["password"].encode('utf-8')):
            return None, "Contraseña incorrecta"

    # 4️⃣ Crear token JWT
    token = crear_token(
        {
            "id": usuario["id"],
            "email": usuario["email"],
            "rol": usuario.get("rol", "estudiante")
        },
        current_app.config["SECRET_KEY"]
    )

    cursor.close()
    return token, usuario.get("rol"), usuario.get("id_curso", None), usuario["id"], usuario["nombre"]
