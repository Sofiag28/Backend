from flask import Flask
from flask_cors import CORS
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from Controllers.integracion_controller import integracion_bp
from config import get_db_connection, MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DB
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567'

# ===========================
# 🔹 Configuración MySQL
# ===========================
app.config['DB_CONNECTION_CONFIG'] = {
    "host": MYSQL_HOST,
    "user": MYSQL_USER,
    "password": MYSQL_PASSWORD,
    "database": MYSQL_DB
}

# ✅ Creamos y guardamos la conexión global
app.config["DB_CONNECTION"] = get_db_connection()

# ===========================
# 🔹 Configuración de correo
# ===========================
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'laurasofiag1012@gmail.com'
app.config['MAIL_PASSWORD'] = ''  # cámbiala o usa variable de entorno
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEFAULT_SENDER'] = ('Ingeniera - Laura', 'laurasofiag1012@gmail.com')

# ===========================
# 🔹 Inicializar extensiones
# ===========================
CORS(app)
mail = Mail(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

app.extensions['mail'] = mail
app.extensions['serializer'] = serializer


# ===========================
# 🔹 Importar blueprints
# ===========================
from routes.auth_routes import auth_bp
from routes.estudiantes_routes import estudiantes_bp
from routes.personal_routes import personal_bp
from routes.metricas_routes import metricas_bp
from routes.usuarios_routes import usuarios_bp
from routes.tareas_routes import tareas_bp
from routes.administrador_routes import admin_bp
from Controllers.integracion_controller import integracion_bp

# ===========================
# 🔹 Registrar blueprints
# ===========================
app.register_blueprint(usuarios_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(estudiantes_bp)
app.register_blueprint(personal_bp)
app.register_blueprint(metricas_bp)
app.register_blueprint(integracion_bp)
app.register_blueprint(tareas_bp)

# ===========================
# 🔹 Ejecutar servidor
# ===========================
if __name__ == "__main__":
    app.run(debug=True)
