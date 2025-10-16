from config import get_db_connection

def obtener_estudiantes():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estudiantes")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def obtener_estudiantes_por_curso(curso):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM estudiantes WHERE curso = %s", (curso,))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data


def agregar_estudiante(nombre, apellido, email, rol, curso):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO estudiantes (nombre, apellido, email, rol, curso) VALUES (%s, %s, %s, %s, %s)",
        (nombre, apellido, email, rol, curso)
    )
    conn.commit()
    cursor.close()
    conn.close()


def actualizar_estudiante(id, nombre, apellido, email, rol, curso):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE estudiantes SET nombre=%s, apellido=%s, email=%s, rol=%s, curso=%s WHERE id=%s",
        (nombre, apellido, email, rol, curso, id)
    )
    conn.commit()
    cursor.close()
    conn.close()


def eliminar_estudiante(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM estudiantes WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
