from flask import Blueprint, jsonify, current_app, request
import pymysql
from datetime import datetime
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT

tareas_bp = Blueprint("tareas_bp", __name__)

# ===========================
# 🔹 Función de conexión global (versión estable para producción)
# ===========================
def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        cursorclass=pymysql.cursors.DictCursor
    )

# ===========================
# 🔹 Obtener todas las tareas asignadas a un estudiante
# ===========================
@tareas_bp.route("/curso-estudiante/<int:id_estudiante>", methods=["GET"])
def obtener_tareas_curso_estudiante(id_estudiante):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id_curso FROM estudiantes WHERE id = %s", (id_estudiante,))
        estudiante = cursor.fetchone()
        if not estudiante:
            return jsonify({"error": "Estudiante no encontrado"}), 404

        id_curso = estudiante["id_curso"]

        cursor.execute("""
            SELECT id, titulo, descripcion, estado, fecha_entrega, id_curso
            FROM tareas
            WHERE id_curso = %s
            ORDER BY fecha_entrega ASC
        """, (id_curso,))
        tareas = cursor.fetchall()

        cursor.close()
        conn.close()
        return jsonify(tareas), 200

    except Exception as e:
        print("Error al obtener tareas del curso del estudiante:", e)
        return jsonify({"error": str(e)}), 500


# ===========================
# 🔹 Actualizar estado de tarea general
# ===========================
@tareas_bp.route("/<int:id_tarea>/estado", methods=["PUT"])
def actualizar_estado_tarea(id_tarea):
    try:
        data = request.json
        nuevo_estado = data.get("estado")
        if nuevo_estado not in ["pendiente", "completada"]:
            return jsonify({"error": "Estado inválido"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tareas SET estado = %s WHERE id = %s", (nuevo_estado, id_tarea))
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Estado actualizado correctamente"}), 200

    except Exception as e:
        print("Error al actualizar estado de tarea:", e)
        return jsonify({"error": str(e)}), 500


# ===========================
# 🔹 Métricas personales del estudiante
# ===========================
@tareas_bp.route("/metricas/<int:id_estudiante>", methods=["GET"])
def metricas_estudiante(id_estudiante):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT id_curso FROM estudiantes WHERE id = %s", (id_estudiante,))
        estudiante = cursor.fetchone()
        if not estudiante:
            return jsonify({"error": "Estudiante no encontrado"}), 404

        id_curso = estudiante["id_curso"]

        cursor.execute("""
            SELECT 
                COUNT(*) AS total_tareas,
                SUM(CASE WHEN estado = 'completada' THEN 1 ELSE 0 END) AS tareas_completadas,
                SUM(CASE WHEN estado = 'pendiente' THEN 1 ELSE 0 END) AS tareas_pendientes
            FROM tareas
            WHERE id_curso = %s
        """, (id_curso,))
        metricas = cursor.fetchone()

        total = metricas["total_tareas"] or 0
        completadas = metricas["tareas_completadas"] or 0
        pendientes = metricas["tareas_pendientes"] or 0
        porcentaje = round((completadas / total) * 100, 2) if total > 0 else 0

        cursor.close()
        conn.close()
        return jsonify({
            "total_tareas": total,
            "tareas_completadas": completadas,
            "tareas_pendientes": pendientes,
            "porcentaje": porcentaje
        }), 200

    except Exception as e:
        print("Error al obtener métricas:", e)
        return jsonify({"error": str(e)}), 500


# ===========================
# 🔹 Listar todos los estudiantes
# ===========================
@tareas_bp.route("/estudiantes", methods=["GET"])
def listar_todos_estudiantes():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, apellido, email, genero, fecha_inscripcion, rol, id_curso
            FROM estudiantes
            ORDER BY nombre, apellido
        """)
        estudiantes = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(estudiantes), 200
    except Exception as e:
        print("Error al listar estudiantes:", e)
        return jsonify({"error": str(e)}), 500


# ===========================
# 🔹 Listar estudiantes por curso
# ===========================
@tareas_bp.route("/estudiantes/curso/<int:id_curso>", methods=["GET"])
def listar_estudiantes_por_curso(id_curso):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, nombre, apellido, email, genero, fecha_inscripcion, rol, id_curso
            FROM estudiantes
            WHERE id_curso = %s
            ORDER BY nombre, apellido
        """, (id_curso,))
        estudiantes = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(estudiantes), 200
    except Exception as e:
        print("Error al listar estudiantes por curso:", e)
        return jsonify({"error": str(e)}), 500


# ===========================
# 🔹 Listar tareas por curso
# ===========================
@tareas_bp.route("/curso/<int:id_curso>", methods=["GET"])
def listar_tareas_por_curso(id_curso):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, titulo, descripcion, fecha_entrega, id_curso
            FROM tareas
            WHERE id_curso = %s
            ORDER BY fecha_entrega ASC
        """, (id_curso,))
        tareas = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(tareas), 200
    except Exception as e:
        print("Error al listar tareas por curso:", e)
        return jsonify({"error": str(e)}), 500


# ===========================
# 🔹 Crear nueva tarea (profesor)
# ===========================
@tareas_bp.route("/crear", methods=["POST"])
def crear_tarea():
    try:
        data = request.get_json()
        titulo = data.get("titulo")
        descripcion = data.get("descripcion")
        id_curso = data.get("id_curso")
        fecha_entrega = data.get("fecha_entrega")

        # 🔹 Validación de campos obligatorios
        if not titulo or not descripcion or not fecha_entrega or not id_curso:
            return jsonify({"error": "Faltan campos obligatorios"}), 400

        

        # 🔹 Conexión a la base de datos
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tareas (titulo, descripcion, fecha_entrega, estado, id_curso)
            VALUES (%s, %s, %s, %s, %s)
        """, (titulo, descripcion, fecha_entrega, id_curso))
        conn.commit()

        nueva_tarea_id = cursor.lastrowid

        # 🔹 Obtener la tarea recién creada para devolverla al frontend
        cursor.execute("SELECT * FROM tareas WHERE id = %s", (nueva_tarea_id,))
        nueva_tarea = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(nueva_tarea), 201

    except Exception as e:
        print("Error al crear tarea:", e)
        return jsonify({"error": str(e)}), 500
# ===========================
# 🔹 Editar tarea
# ===========================
@tareas_bp.route("/editar/<int:id>", methods=["PUT"])
def editar_tarea(id):
    try:
        data = request.get_json()
        titulo = data.get("titulo")
        descripcion = data.get("descripcion")
        fecha_entrega = data.get("fecha_entrega")
        estado = data.get("estado", "pendiente")
        id_curso = data.get("id_curso")

        if not titulo or not descripcion or not fecha_entrega or not id_curso:
            return jsonify({"error": "Faltan campos"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tareas
            SET titulo = %s,
                descripcion = %s,
                fecha_entrega = %s,
                id_curso = %s,
                estado = %s
            WHERE id = %s
        """, (titulo, descripcion, fecha_entrega, id_curso, estado, id))
        conn.commit()

        # 🔹 Obtener la tarea actualizada
        cursor.execute("SELECT * FROM tareas WHERE id = %s", (id,))
        tarea_actualizada = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(tarea_actualizada), 200

    except Exception as e:
        print("Error al editar tarea:", e)
        return jsonify({"error": str(e)}), 500
# ===========================
# 🔹 Eliminar tarea
# ===========================
@tareas_bp.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar_tarea(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = %s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Tarea eliminada correctamente"}), 200

    except Exception as e:
        print("Error al eliminar tarea:", e)
        return jsonify({"error": str(e)}), 500


# ===========================
# 🔹 Listar cursos
# ===========================
@tareas_bp.route("/cursos", methods=["GET"])
def listar_cursos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre FROM cursos ORDER BY id ASC")
        cursos = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(cursos), 200
    except Exception as e:
        print("Error al obtener cursos:", e)
        return jsonify({"error": "No se pudieron obtener los cursos"}), 500


# ===========================
# 🔹 Actualizar estado de tarea (por estudiante)
# ===========================
@tareas_bp.route("/<int:id_tarea>", methods=["PUT"])
def actualizar_estado_por_estudiante(id_tarea):
    try:
        data = request.get_json()
        id_estudiante = data.get("id_estudiante")
        nuevo_estado = data.get("estado")

        if not id_estudiante or not nuevo_estado:
            return jsonify({"error": "Faltan campos"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tareas_estudiantes
            SET estado = %s, fecha_actualizacion = NOW()
            WHERE id_tarea = %s AND id_estudiante = %s
        """, (nuevo_estado, id_tarea, id_estudiante))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"mensaje": "Estado actualizado correctamente"}), 200

    except Exception as e:
        print("Error al actualizar estado por estudiante:", e)
        return jsonify({"error": str(e)}), 500
