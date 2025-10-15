from flask import Blueprint, request, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash

usuarios_bp = Blueprint("usuarios", __name__, url_prefix="/usuarios")

# LISTAR todos los usuarios
@usuarios_bp.route("/listar", methods=["GET"])
def listar_usuarios():
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    return jsonify(usuarios), 200

# CREAR un nuevo usuario
@usuarios_bp.route("/crear", methods=["POST"])
def crear_usuario():
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor()
    data = request.json

    # Validación básica
    if not data.get("username") or not data.get("contraseña") or not data.get("rol"):
        return jsonify({"error": "Username, contraseña y rol son obligatorios"}), 400

    contrasena_hash = generate_password_hash(data.get("contraseña"))
    
    cursor.execute(
        """
        INSERT INTO usuarios(username, contraseña, rol) 
        VALUES (%s, %s, %s)
        """,
        (
            data.get("username"),
            contrasena_hash,
            data.get("rol")
        )
    )
    db.commit()
    return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

# ACTUALIZAR un usuario@usuarios_bp.route("/actualizar/<int:id>", methods=["PUT"])
@usuarios_bp.route("/actualizar/<int:id>", methods=["PUT"])
def actualizar_usuario(id):
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor()
    data = request.json

    # Validación de campos obligatorios
    if not data.get("username") or not data.get("rol"):
        return jsonify({"error": "Username y rol son obligatorios"}), 400

    try:
        cursor.execute(
            """
            UPDATE usuarios 
            SET username=%s, rol=%s
            WHERE id=%s
            """,
            (
                data.get("username"),
                data.get("rol"),
                id
            )
        )
        db.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Usuario no encontrado"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"mensaje": "Usuario actualizado correctamente"}), 200


# ELIMINAR un usuario
@usuarios_bp.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id=%s", (id,))
    db.commit()
    return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200
