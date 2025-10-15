import mysql.connector

# ===========================
# 🔹 Configuración de MySQL
# ===========================
MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = ""
MYSQL_DB = "genuineschool"  # 👈 cambia por el nombre real de tu base de datos

# ===========================
# 🔹 Función para obtener conexión
# ===========================
def get_db_connection():
    return mysql.connector.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB
    )
