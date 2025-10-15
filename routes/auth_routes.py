from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from Controllers.auth import crear_token,login_usuario
from datetime import datetime
import pymysql
from config import get_db_connection

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ==========================
# 🔹 REGISTRO ESTUDIANTE
# ==========================
@auth_bp.route("/registro", methods=["POST"])
def registro():
    data = request.json
    nombre = data.get("nombre")
    apellido = data.get("apellido")
    email = data.get("email")
    password = data.get("password")
    id_curso = data.get("id_curso")
    genero = data.get("genero")

    if not all([nombre, apellido, email, password, id_curso, genero]):
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    # 🔹 Crear conexión nueva
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)

    # Verificar si ya existe
    cursor.execute("SELECT * FROM estudiantes WHERE email=%s", (email,))
    if cursor.fetchone():
        cursor.close()
        db.close()
        return jsonify({"error": "El correo ya está registrado"}), 400

    fecha_inscripcion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Insertar nuevo estudiante
    hashed = generate_password_hash(password)
    cursor.execute(
        """
        INSERT INTO estudiantes (nombre, apellido, email, password, id_curso, genero, fecha_inscripcion, rol)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """,
        (nombre, apellido, email, hashed, id_curso, genero, fecha_inscripcion, "estudiante")
    )
    db.commit()
    cursor.close()
    db.close()  # 🔹 Cierra la conexión siempre

    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201


# ==========================
# 🔹 LOGIN GENERAL
# ==========================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    db = get_db_connection()  # 🔹 nueva conexión
    resultado = login_usuario(email, password, db)
    db.close()  # 🔹 cerrar al final

    if not resultado or resultado[0] is None:
        return jsonify({"error": resultado[1] if resultado else "Error en login"}), 401

    token, rol, id_curso, user_id, nombre = resultado

    return jsonify({
        "mensaje": "Login exitoso ✅",
        "token": token,
        "rol": rol,
        "id": user_id,
        "nombre": nombre,
        "id_curso": id_curso,
    }), 200
