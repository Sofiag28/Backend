from flask import Blueprint, jsonify, request, current_app
from config import get_db_connection, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT
import pymysql
admin_bp = Blueprint("admin", __name__)

# ===========================
# 🔹 Conexión a la base de datos
# ===========================
def get_db_connection():
    conf = current_app.config["DB_CONNECTION_CONFIG"]
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )


# ===========================
# 🔹 Listar usuarios
# ===========================
@admin_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT id, nombre, apellido, email, rol, id_curso 
        FROM estudiantes
        UNION
        SELECT id, nombre, apellido, email, rol, NULL as id_curso 
        FROM personal
    """
    cursor.execute(query)
    usuarios = cursor.fetchall()

    cursor.close()
    conn.close()
    return jsonify(usuarios), 200

# ===========================
# 🔹 Crear usuario
# ===========================
@admin_bp.route("/crear", methods=["POST"])
def crear_usuario():
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        email = data.get("email")
        password = data.get("password")
        rol = data.get("rol")
        genero = data.get("genero", None)
        id_curso = data.get("id_curso", None)

        if not nombre or not apellido or not email or not password or not rol:
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        # Dependiendo del rol, se inserta en la tabla correspondiente
        if rol.lower() == "estudiante":
            query = """
                INSERT INTO estudiantes (nombre, apellido, email, password, rol, genero, id_curso)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, apellido, email, password, rol, genero, id_curso))
        else:
            query = """
                INSERT INTO personal (nombre, apellido, email, password, rol, genero)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, apellido, email, password, rol, genero))

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Usuario creado correctamente"}), 201

    except Exception as e:
        print("Error al crear usuario:", e)
        return jsonify({"error": str(e)}), 500

# ===========================
# 🔹 Editar usuario
# ===========================
@admin_bp.route("/editar/<int:id>", methods=["PUT"])
def editar_usuario(id):
    try:
        data = request.get_json()
        nombre = data.get("nombre")
        apellido = data.get("apellido")
        email = data.get("email")
        rol = data.get("rol")
        genero = data.get("genero", None)
        id_curso = data.get("id_curso", None)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Verificamos si es estudiante o personal
        cursor.execute("SELECT id FROM estudiantes WHERE id = %s", (id,))
        es_estudiante = cursor.fetchone()

        if es_estudiante:
            query = """
                UPDATE estudiantes 
                SET nombre = %s, apellido = %s, email = %s, rol = %s, genero = %s, id_curso = %s
                WHERE id = %s
            """
            cursor.execute(query, (nombre, apellido, email, rol, genero, id_curso, id))
        else:
            query = """
                UPDATE personal 
                SET nombre = %s, apellido = %s, email = %s, rol = %s, genero = %s
                WHERE id = %s
            """
            cursor.execute(query, (nombre, apellido, email, rol, genero, id))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Usuario actualizado correctamente"}), 200

    except Exception as e:
        print("Error al editar usuario:", e)
        return jsonify({"error": str(e)}), 500

# ===========================
# 🔹 Eliminar usuario
# ===========================
@admin_bp.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar_usuario(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM estudiantes WHERE id=%s", (id,))
        cursor.execute("DELETE FROM personal WHERE id=%s", (id,))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200
    except Exception as e:
        print("Error al eliminar usuario:", e)
        return jsonify({"error": str(e)}), 500

# ===========================
# 🔹 Estadísticas generales
# ===========================
@admin_bp.route("/estadisticas", methods=["GET"])
def estadisticas():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total FROM estudiantes")
    total_estudiantes = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) as total FROM personal")
    total_personal = cursor.fetchone()["total"]

    cursor.close()
    conn.close()

    return jsonify({
        "estudiantes": total_estudiantes,
        "personal": total_personal
    }), 200