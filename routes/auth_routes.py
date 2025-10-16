from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from Controllers.auth import crear_token, login_usuario
from datetime import datetime
import pymysql
from config import get_db_connection

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# ==========================
# 🔹 REGISTRO ESTUDIANTE
# ==========================
@auth_bp.route("/registro", methods=["POST"])
def registro():
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        email = data.get("email")
        password = data.get("password")
        id_curso = data.get("id_curso")
        genero = data.get("genero")

        # Validación de campos requeridos
        if not all([nombre, apellido, email, password, id_curso, genero]):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        # 🔹 Conexión a BD
        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # Verificar si el correo ya existe
        cursor.execute("SELECT * FROM estudiantes WHERE email = %s", (email,))
        if cursor.fetchone():
            cursor.close()
            db.close()
            return jsonify({"error": "El correo ya está registrado"}), 400

        # Insertar nuevo estudiante
        hashed_password = generate_password_hash(password)
        fecha_inscripcion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        insert_query = """
            INSERT INTO estudiantes 
            (nombre, apellido, email, password, id_curso, genero, fecha_inscripcion, rol)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            nombre, apellido, email, hashed_password, id_curso, genero, fecha_inscripcion, "estudiante"
        ))

        db.commit()
        return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

    except Exception as e:
        print(f"❌ Error en registro: {e}")
        return jsonify({"error": "Error al registrar usuario"}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()


# ==========================
# 🔹 LOGIN GENERAL
# ==========================
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"error": "Email y contraseña son obligatorios"}), 400

        db = get_db_connection()
        resultado = login_usuario(email, password, db)

        if not resultado or resultado[0] is None:
            return jsonify({"error": resultado[1] if resultado else "Credenciales inválidas"}), 401

        token, rol, id_curso, user_id, nombre = resultado

        return jsonify({
            "mensaje": "Login exitoso ✅",
            "token": token,
            "rol": rol,
            "id": user_id,
            "nombre": nombre,
            "id_curso": id_curso,
        }), 200

    except Exception as e:
        print(f"❌ Error en login: {e}")
        return jsonify({"error": "Error interno en el login"}), 500

    finally:
        if 'db' in locals():
            db.close()
