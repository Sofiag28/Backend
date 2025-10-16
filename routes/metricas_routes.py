from flask import Blueprint, jsonify, current_app
import pymysql

metricas_bp = Blueprint("metricas", __name__, url_prefix="/metricas")

@metricas_bp.route("/listar", methods=["GET"])
def metricas():
    """
    Devuelve métricas generales del sistema:
    - Total de estudiantes
    - Personal agrupado por rol
    - Fecha de la última inscripción
    """
    db = current_app.config['DB_CONNECTION']
    cursor = db.cursor(pymysql.cursors.DictCursor)

    try:
        # Total de estudiantes
        cursor.execute("SELECT COUNT(*) AS total FROM estudiantes")
        total_estudiantes = cursor.fetchone()["total"]

        # Personal agrupado por rol
        cursor.execute("SELECT rol, COUNT(*) AS total FROM personal GROUP BY rol")
        personal_por_rol = cursor.fetchall()

        # Última inscripción
        cursor.execute("SELECT fecha_inscripcion FROM estudiantes ORDER BY fecha_inscripcion DESC LIMIT 1")
        ultima_inscripcion = cursor.fetchone()["fecha_inscripcion"]

        return jsonify({
            "total_estudiantes": total_estudiantes,
            "personal_por_rol": personal_por_rol,
            "ultima_inscripcion": ultima_inscripcion
        }), 200

    except Exception as e:
        print(f"❌ Error al obtener métricas: {e}")
        return jsonify({"error": "No se pudieron obtener las métricas"}), 500

    finally:
        cursor.close()
