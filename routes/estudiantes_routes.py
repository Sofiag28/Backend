from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from datetime import datetime
import jwt
import pymysql
from config import get_db_connection

SECRET_KEY = "123456"

estudiantes_bp = Blueprint("estudiantes", __name__, url_prefix="/estudiantes")


# ==========================
# 🔹 LISTAR ESTUDIANTES
# ==========================
@estudiantes_bp.route("/listar", methods=["GET"])
def listar_estudiantes():
    try:
        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        curso = request.args.get("curso")
        if curso:
            cursor.execute("SELECT * FROM estudiantes WHERE curso = %s", (curso,))
        else:
            cursor.execute("SELECT * FROM estudiantes")

        estudiantes = cursor.fetchall()
        return jsonify(estudiantes), 200

    except Exception as e:
        print(f"❌ Error al listar estudiantes: {e}")
        return jsonify({"error": "Error al obtener los estudiantes"}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()


# ==========================
# 🔹 CREAR ESTUDIANTE
# ==========================
@estudiantes_bp.route("/crear", methods=["POST"])
def crear_estudiante():
    try:
        data = request.get_json()

        nombre = data.get("nombre")
        apellido = data.get("apellido")
        email = data.get("email")
        password = data.get("password")
        genero = data.get("genero")
        curso = data.get("curso")

        if not all([nombre, apellido, email, password, genero, curso]):
            return jsonify({"error": "Todos los campos son obligatorios"}), 400

        password_hash = generate_password_hash(password)
        token = jwt.encode({"email": email}, SECRET_KEY, algorithm="HS256")
        fecha_inscripcion = datetime.now().strftime("%Y-%m-%d")

        db = get_db_connection()
        cursor = db.cursor(pymysql.cursors.DictCursor)

        # Verificar si ya existe
        cursor.execute("SELECT * FROM estudiantes WHERE email = %s", (email,))
        if cursor.fetchone():
            return jsonify({"error": "El correo ya está registrado"}), 400

        # Insertar
        cursor.execute("""
            INSERT INTO estudiantes (nombre, apellido, email, genero, fecha_inscripcion, password, curso)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, apellido, email, genero, fecha_inscripcion, password_hash, curso))
        db.commit()

        return jsonify({
            "mensaje": "Estudiante registrado exitosamente",
            "token": token
        }), 201

    except Exception as e:
        print(f"❌ Error al crear estudiante: {e}")
        return jsonify({"error": "Error al registrar estudiante"}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()


# ==========================
# 🔹 ACTUALIZAR ESTUDIANTE
# ==========================
@estudiantes_bp.route("/actualizar/<int:id>", methods=["PUT"])
def actualizar_estudiante(id):
    try:
        data = request.get_json()

        db = get_db_connection()
        cursor = db.cursor()

        cursor.execute("""
            UPDATE estudiantes
            SET nombre=%s, apellido=%s, email=%s, genero=%s, fecha_inscripcion=%s, curso=%s
            WHERE id=%s
        """, (
            data.get("nombre"),
            data.get("apellido"),
            data.get("email"),
            data.get("genero"),
            data.get("fecha_inscripcion"),
            data.get("curso"),
            id
        ))

        db.commit()
        return jsonify({"mensaje": "Estudiante actualizado correctamente"}), 200

    except Exception as e:
        print(f"❌ Error al actualizar estudiante: {e}")
        return jsonify({"error": "Error al actualizar estudiante"}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()


# ==========================
# 🔹 ELIMINAR ESTUDIANTE
# ==========================
@estudiantes_bp.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar_estudiante(id):
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("DELETE FROM estudiantes WHERE id=%s", (id,))
        db.commit()
        return jsonify({"mensaje": "Estudiante eliminado correctamente"}), 200

    except Exception as e:
        print(f"❌ Error al eliminar estudiante: {e}")
        return jsonify({"error": "Error al eliminar estudiante"}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'db' in locals():
            db.close()
