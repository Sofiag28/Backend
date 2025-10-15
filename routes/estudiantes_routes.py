from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash
from datetime import datetime 
import jwt

SECRET_KEY = "123456"

estudiantes_bp = Blueprint("estudiantes", __name__, url_prefix="/estudiantes")


# LISTAR todos los estudiantes o filtrar por curso
@estudiantes_bp.route("/listar", methods=["GET"])
def listar_estudiantes():
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor(dictionary=True)

    curso = request.args.get("curso")  

    if curso:
        cursor.execute("SELECT * FROM estudiantes WHERE curso = %s", (curso,))
    else:
        cursor.execute("SELECT * FROM estudiantes")

    estudiantes = cursor.fetchall()
    return jsonify(estudiantes), 200

# CREAR un estudiante nuevo

@estudiantes_bp.route("/crear", methods=["POST"])
def crear_estudiante():
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor(dictionary=True)
    data = request.json

    if not data.get("nombre") or not data.get("apellido") or not data.get("email"):
        return jsonify({"error": "Nombre, apellido y email son obligatorios"}), 400

    password_hash = generate_password_hash(data.get("password"))

    # Token de verificación
    token = jwt.encode(
        {"email": data.get("email")},
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    fecha_inscripcion = datetime.now().strftime("%Y-%m-%d")

    try:
        cursor.execute(
            """
            INSERT INTO estudiantes(nombre, apellido, email, genero, fecha_inscripcion, password,curso)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                data.get("nombre"),
                data.get("apellido"),
                data.get("email"),
                data.get("genero"),
                fecha_inscripcion,
                password_hash,
                data.get("curso")
            )
        )
        db.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Retornar mensaje rápido sin enviar correo aún
    return jsonify({
        "mensaje": "Estudiante registrado exitosamente",
        "token": token
    }), 201
# ACTUALIZAR un estudiante existente
@estudiantes_bp.route("/actualizar<int:id>", methods=["PUT"])
def actualizar_estudiante(id):
    data = request.json
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor()
    cursor.execute(
        "UPDATE estudiantes SET nombre=%s, apellido=%s, email=%s, genero=%s, fecha_inscripcion=%s, curso=%s WHERE id=%s",
        (
            data.get("nombre"),
            data.get("apellido"),
            data.get("email"),
            data.get("genero"),
            data.get("fecha_inscripcion"),
            data.get("curso"),
            id
        )
    )
    db.commit()
    return jsonify({"mensaje": "Estudiante actualizado correctamente"}), 200

# ELIMINAR un estudiante
@estudiantes_bp.route("/eliminar<int:id>", methods=["DELETE"])
def eliminar_estudiante(id):
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor()
    cursor.execute("DELETE FROM estudiantes WHERE id=%s", (id,))
    db.commit()
    return jsonify({"mensaje": "Estudiante eliminado correctamente"}), 200
