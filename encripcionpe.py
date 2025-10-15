import bcrypt
from config import get_db_connection, DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT, current_app, conf
import pymysql

# 🔹 Conexión a la base de datos
def get_db_connection():
    conf = current_app.config["DB_CONNECTION_CONFIG"]
    return pymysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
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
    conf.execute(query, (admin[0], admin[1], admin[2], hashed, admin[3], admin[4]))
    print(f"✅ Administrador {admin[0]} {admin[1]} insertado correctamente.")

# Guardar cambios
conf.commit()
conf.close()
conf.close()

print("\n🎉 Nuevos administradores insertados correctamente con contraseña '12345'.")