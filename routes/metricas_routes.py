from flask import Blueprint, jsonify, current_app

metricas_bp = Blueprint("metricas", __name__, url_prefix="/metricas")

@metricas_bp.route("/listar", methods=["GET"])
def metricas():
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor(dictionary=True)

    # Total de estudiantes
    cursor.execute("SELECT COUNT(*) as total FROM estudiantes")
    total_estudiantes = cursor.fetchone()["total"]

    # Personal por rol
    cursor.execute("SELECT rol, COUNT(*) as total FROM personal GROUP BY rol")
    personal_por_rol = cursor.fetchall()

    # Última inscripción
    cursor.execute("SELECT fecha_inscripcion FROM estudiantes ORDER BY fecha_inscripcion DESC LIMIT 1")
    ultima_inscripcion = cursor.fetchone()["fecha_inscripcion"]

    return jsonify({
        "total_estudiantes": total_estudiantes,
        "personal_por_rol": personal_por_rol,
        "ultima_inscripcion": ultima_inscripcion
    }), 200
