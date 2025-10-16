from flask import Blueprint, request, jsonify, current_app

personal_bp = Blueprint("personal", __name__, url_prefix="/personal")

# LISTAR todo el personal
@personal_bp.route("/listar", methods=["GET"])
def listar_personal():
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM personal")
    personal = cursor.fetchall()
    return jsonify(personal), 200

# CREAR un nuevo miembro del personal
@personal_bp.route("/crear", methods=["POST"])
def crear_personal():
    data = request.json
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO personal(nombre, apellido, email, genero, rol) VALUES (%s,%s,%s,%s,%s)",
        (
            data.get("nombre"),
            data.get("apellido"),
            data.get("email"),
            data.get("genero"),
            data.get("rol")
        )
    )
    db.commit()
    return jsonify({"mensaje": "Personal registrado correctamente"}), 201

# 🚨 Aquí faltaban las barras antes del parámetro <id>
@personal_bp.route("/actualizar/<int:id>", methods=["PUT"])
def actualizar_personal(id):
    data = request.json
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor()
    cursor.execute(
        "UPDATE personal SET nombre=%s, apellido=%s, email=%s, genero=%s, rol=%s WHERE id=%s",
        (
            data.get("nombre"),
            data.get("apellido"),
            data.get("email"),
            data.get("genero"),
            data.get("rol"),
            id
        )
    )
    db.commit()
    return jsonify({"mensaje": "Personal actualizado correctamente"}), 200

# 🚨 Aquí igual: faltaba la barra antes de <id>
@personal_bp.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar_personal(id):
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor()
    cursor.execute("DELETE FROM personal WHERE id=%s", (id,))
    db.commit()
    return jsonify({"mensaje": "Personal eliminado correctamente"}), 200
