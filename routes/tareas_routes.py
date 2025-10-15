from flask import Blueprint, jsonify, current_app, request
import mysql.connector
from datetime import datetime

tareas_bp = Blueprint("tareas_bp", __name__)

# ===========================
# 🔹 Función para conexión MySQL
# ===========================
def get_db_connection():
    conf = current_app.config['DB_CONNECTION_CONFIG']
    return mysql.connector.connect(
        host=conf['host'],
        user=conf['user'],
        password=conf['password'],
        database=conf['database']
    )


# ===========================
# 🔹 Obtener todas las tareas asignadas a un estudiante (incluye estado en tareas_estudiantes)
# ===========================
@tareas_bp.route("/curso-estudiante/<int:id_estudiante>", methods=["GET"])
def obtener_tareas_curso_estudiante(id_estudiante):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 1️⃣ Obtener el curso del estudiante
        cursor.execute("SELECT id_curso FROM estudiantes WHERE id = %s", (id_estudiante,))
        estudiante = cursor.fetchone()
        if not estudiante:
            return jsonify({"error": "Estudiante no encontrado"}), 404

        id_curso = estudiante["id_curso"]

        # 2️⃣ Traer todas las tareas del curso
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
    
# 🔹 Actualizar el estado de una tarea
@tareas_bp.route("/tareas/<int:id_tarea>/estado", methods=["PUT"])
def actualizar_estado_tarea(id_tarea):
    try:
        data = request.json
        nuevo_estado = data.get("estado")
        if nuevo_estado not in ["pendiente", "completada"]:
            return jsonify({"error": "Estado inválido"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE tareas SET estado = %s WHERE id = %s",
            (nuevo_estado, id_tarea)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Estado actualizado correctamente"}), 200

    except Exception as e:
        print("Error al actualizar estado de tarea:", e)
        return jsonify({"error": str(e)}), 500
# ===========================
# 🔹 Métricas personales (por estudiante)
# ===========================
@tareas_bp.route("/metricas/<int:id_estudiante>", methods=["GET"])
def metricas_estudiante(id_estudiante):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Obtener el curso del estudiante
        cursor.execute("SELECT id_curso FROM estudiantes WHERE id = %s", (id_estudiante,))
        estudiante = cursor.fetchone()

        if not estudiante:
            return jsonify({"error": "Estudiante no encontrado"}), 404

        id_curso = estudiante["id_curso"]

        # Contar tareas totales y completadas del curso
        cursor.execute("""
            SELECT 
                COUNT(*) AS total_tareas,
                SUM(CASE WHEN estado = 'completada' THEN 1 ELSE 0 END) AS tareas_completadas,
                SUM(CASE WHEN estado = 'pendiente' THEN 1 ELSE 0 END) AS tareas_pendientes
            FROM tareas
            WHERE id_curso = %s
        """, (id_curso,))
        metricas = cursor.fetchone()

        cursor.close()
        conn.close()

        # Calcular porcentaje
        total = metricas["total_tareas"] or 0
        completadas = metricas["tareas_completadas"] or 0
        pendientes = metricas["tareas_pendientes"] or 0
        porcentaje = round((completadas / total) * 100, 2) if total > 0 else 0

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
        cursor = conn.cursor(dictionary=True)
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
        print("Error al listar todos los estudiantes:", e)
        return jsonify({"error": str(e)}), 500


# ===========================
# 🔹 Listar estudiantes por curso
# ===========================
@tareas_bp.route("/estudiantes/curso/<int:id_curso>", methods=["GET"])
def listar_estudiantes_por_curso(id_curso):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
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
# 🔹 Listar tareas por curso (para el profesor) — tareas principales (no estados por alumno)
# ===========================
@tareas_bp.route("/tareas/curso/<int:id_curso>", methods=["GET"])
def listar_tareas_por_curso(id_curso):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
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
        print("Error al obtener tareas por curso:", e)
        return jsonify({"error": str(e)}), 500

# ===========================
# 🔹 Listar todas las tareas (sin importar el curso)
# ===========================
@tareas_bp.route("/tareas", methods=["GET"])
def listar_todas_tareas():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, titulo, descripcion, fecha_entrega, id_curso
            FROM tareas
            ORDER BY fecha_entrega ASC
        """)
        tareas = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(tareas), 200

    except Exception as e:
        print("Error al obtener todas las tareas:", e)
        return jsonify({"error": str(e)}), 500
    
    ######### CREAR 
@tareas_bp.route("/crear", methods=["POST"])
def crear_tarea():
    try:
        data = request.get_json()
        titulo = data.get("titulo")
        descripcion = data.get("descripcion")
        id_curso = data.get("id_curso")
        fecha_entrega = data.get("fecha_entrega")

        if not titulo or not descripcion or not fecha_entrega or not id_curso:
            return jsonify({"error": "Faltan campos obligatorios (titulo, descripcion, fecha_entrega, id_curso)"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Crear tarea
        cursor.execute("""
            INSERT INTO tareas (titulo, descripcion, fecha_entrega, id_curso)
            VALUES (%s, %s, %s, %s)
        """, (titulo, descripcion, fecha_entrega, id_curso))
        id_tarea = cursor.lastrowid

        # Obtener estudiantes del curso
        cursor.execute("SELECT id FROM estudiantes WHERE id_curso = %s", (id_curso,))
        estudiantes = cursor.fetchall()

        # Asignar tarea a cada estudiante
        for row in estudiantes:
            student_id = row["id"]
            cursor.execute("""
                INSERT INTO tareas_estudiantes (id_tarea, id_estudiante, estado, fecha_actualizacion)
                VALUES (%s, %s, %s, NOW())
            """, (id_tarea, student_id, "pendiente"))

        conn.commit()

        # 🔹 Obtener la tarea recién creada para devolverla al frontend
        cursor.execute("""
            SELECT id, titulo, descripcion, fecha_entrega, id_curso, 'Pendiente' AS estado
            FROM tareas
            WHERE id = %s
        """, (id_tarea,))
        nueva_tarea = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(nueva_tarea), 201

    except Exception as e:
        print("Error al crear tarea:", e)
        return jsonify({"error": str(e)}), 500
# ===========================
# 🔹 Editar tarea (profesor) — si cambia id_curso reasigna a nuevos estudiantes
# ===========================
@tareas_bp.route("/editar/<int:id>", methods=["PUT"])
def editar_tarea_profesor(id):
    try:
        data = request.get_json()
        titulo = data.get("titulo")
        descripcion = data.get("descripcion")
        fecha_entrega = data.get("fecha_entrega")
        nuevo_id_curso = data.get("id_curso")  # opcional

        if not titulo or not descripcion or not fecha_entrega:
            return jsonify({"error": "Faltan campos obligatorios (titulo, descripcion, fecha_actualizacion)"}), 400

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Obtener curso actual de la tarea
        cursor.execute("SELECT id_curso FROM tareas WHERE id = %s", (id,))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            return jsonify({"error": "Tarea no encontrada"}), 404
        id_curso_actual = row["id_curso"]

        # Actualizar tabla tareas
        cursor2 = conn.cursor()
        cursor2.execute("""
            UPDATE tareas
            SET titulo = %s, descripcion = %s, fecha_entrega = %s, id_curso = %s
            WHERE id = %s
        """, (titulo, descripcion, fecha_entrega, nuevo_id_curso or id_curso_actual, id))
        conn.commit()

        # Si cambió de curso, reasignar tareas_estudiantes:
        if nuevo_id_curso and int(nuevo_id_curso) != int(id_curso_actual):
            # 1) Eliminar asignaciones previas
            cursor2.execute("DELETE FROM tareas_estudiantes WHERE id_tarea = %s", (id,))

            # 2) Obtener estudiantes del nuevo curso y crear asignaciones
            cursor2.execute("SELECT id FROM estudiantes WHERE id_curso = %s", (nuevo_id_curso,))
            estudiantes_nuevos = cursor2.fetchall()
            for row in estudiantes_nuevos:
                student_id = row[0] if isinstance(row, tuple) else row.get('id')
                cursor2.execute("""
                    INSERT INTO tareas_estudiantes (id_tarea, id_estudiante, fecha_actualizacion)
                    VALUES (%s, %s, %s, NOW())
                """, (id, student_id, 'pendiente'))
            conn.commit()

        # Devolver tarea actualizada
        cursor.execute("SELECT * FROM tareas WHERE id = %s", (id,))
        tarea_actualizada = cursor.fetchone()
        cursor.close()
        cursor2.close()
        conn.close()
        return jsonify(tarea_actualizada), 200

    except Exception as e:
        print("Error al editar tarea:", e)
        return jsonify({"error": str(e)}), 500


# ===========================
# 🔹 Eliminar tarea (profesor) — elimina asignaciones y la tarea
# ===========================
@tareas_bp.route("/eliminar/<int:id>", methods=["DELETE"])
def eliminar_tarea_profesor(id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # eliminar de tareas_estudiantes primero (si existe)
        cursor.execute("DELETE FROM tareas_estudiantes WHERE id_tarea = %s", (id,))
        # eliminar de tareas
        cursor.execute("DELETE FROM tareas WHERE id = %s", (id,))

        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Tarea y asignaciones eliminadas correctamente"}), 200

    except Exception as e:
        print("Error al eliminar tarea:", e)
        return jsonify({"error": str(e)}), 500

#___________________________
#Cursos
#________________

@tareas_bp.route("/cursos", methods=["GET"])
def listar_cursos():
    try:
        db = current_app.config["DB_CONNECTION"]
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, nombre FROM cursos ORDER BY id ASC")
        cursos = cursor.fetchall()
        cursor.close()

        return jsonify(cursos), 200
    except Exception as e:
        print("Error al obtener cursos:", e)
        return jsonify({"error": "No se pudieron obtener los cursos"}), 500

# ===========================
# 🔹 Actualizar estado de una tarea para un estudiante (checkbox -> completada/pendiente)
# ===========================
@tareas_bp.route("/tareas/<int:id_tarea>", methods=["PUT"])
def actualizar_estado_por_estudiante(id_tarea):
    try:
        data = request.get_json()
        id_estudiante = data.get("id_estudiante")
        nuevo_estado = data.get("estado")

        if not id_estudiante or not nuevo_estado:
            return jsonify({"error": "Faltan campos (id_estudiante, estado)"}), 400

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
        return jsonify({"message": "Estado actualizado correctamente"}), 200


    except Exception as e:
        print("Error al actualizar estado por estudiante:", e)
        return jsonify({"error": str(e)}), 500
