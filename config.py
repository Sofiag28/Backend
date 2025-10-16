import pymysql
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde .env
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = int(os.getenv("DB_PORT"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
SSL_CA = "ca-certificate.crt"  # Ruta al certificado CA

SSL_CA = "/etc/secrets/ca-certificate.crt"

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT,
        ssl={'ca': SSL_CA}  # Aquí indicamos el certificado SSL
    )
