import requests
from flask import Blueprint, jsonify

integracion_bp = Blueprint('integracion', __name__)

@integracion_bp.route('/integracion/hubspot', methods=['GET'])
def obtener_datos_hubspot():
    """
    Simula una integración real con HubSpot consumiendo un servicio público (Fake Store API).
    Devuelve una lista de usuarios y productos, representando clientes y campañas de marketing.
    """
    try:
        # Endpoint real gratuito que simula datos de usuarios
        url_usuarios = 'https://fakestoreapi.com/users'
        url_productos = 'https://fakestoreapi.com/products'
        
        # Hacemos las peticiones a las APIs externas
        respuesta_usuarios = requests.get(url_usuarios)
        respuesta_productos = requests.get(url_productos)

        if respuesta_usuarios.status_code == 200 and respuesta_productos.status_code == 200:
            usuarios = respuesta_usuarios.json()
            productos = respuesta_productos.json()
            
            # Procesamos los usuarios
            contactos = [
                {
                    "nombre": f"{u['name']['firstname'].capitalize()} {u['name']['lastname'].capitalize()}",
                    "correo": u["email"],
                    "ciudad": u["address"]["city"].capitalize()
                }
                for u in usuarios[:5]
            ]
            
            # Procesamos los productos e incluimos imágenes
            campañas = [
                {
                    "nombre_campaña": p["title"],
                    "categoria": p["category"].capitalize(),
                    "precio_promocional": f"${p['price'] * 0.9:.2f}",  # 10% descuento simulado
                    "imagen": p["image"]  # 👈 Aquí añadimos la imagen
                }
                for p in productos[:5]
            ]
            
            return jsonify({
                "integracion": "Simulación avanzada de HubSpot (Fake Store API)",
                "contactos": contactos,
                "campañas": campañas
            }), 200

        else:
            return jsonify({
                "error": "No se pudieron obtener los datos del servicio externo."
            }), 500

    except Exception as e:
        return jsonify({
            "error": f"Ocurrió un error interno: {str(e)}"
        }), 500
