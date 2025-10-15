from app import db, cursor

def obtener_estudiantes():
    cursor.execute("SELECT * FROM estudiantes")
    return cursor.fetchall()

def obtener_estudiantes_por_curso(curso):
    cursor.execute("SELECT * FROM estudiantes WHERE curso = %s", (curso,))
    return cursor.fetchall()

def agregar_estudiante(nombre, apellido, email, rol, curso):
    cursor.execute(
        "INSERT INTO estudiantes (nombre, apellido, email, rol, curso) VALUES (%s, %s, %s, %s, %s)",
        (nombre, apellido, email, rol, curso)
    )
    db.commit()

def actualizar_estudiante(id, nombre, apellido, email, rol, curso):
    cursor.execute(
        "UPDATE estudiantes SET nombre=%s, apellido=%s, email=%s, rol=%s, curso=%s WHERE id=%s",
        (nombre, apellido, email, rol, curso, id)
    )
    db.commit()

def eliminar_estudiante(id):
    cursor.execute("DELETE FROM estudiantes WHERE id=%s", (id,))
    db.commit()
