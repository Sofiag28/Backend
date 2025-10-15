import bcrypt
import mysql.connector

# 🔹 Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="genuineschool"
)

cursor = db.cursor()

# Nuevos administradores
admins = [
    ('Sara', 'patiño', 'saara.suarezp@admin.com', 'admin', 'Femenino'),
    ('cami', 'Cas', 'andresca.lo@admin.com', 'Administrador', 'Masculino'),
   
]

password = "12345"

for admin in admins:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    query = """
    INSERT INTO personal (nombre, apellido, email, password, rol, genero)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (admin[0], admin[1], admin[2], hashed, admin[3], admin[4]))
    print(f"✅ Administrador {admin[0]} {admin[1]} insertado correctamente.")

# Guardar cambios
db.commit()
cursor.close()
db.close()

print("\n🎉 Nuevos administradores insertados correctamente con contraseña '12345'.")