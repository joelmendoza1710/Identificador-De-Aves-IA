from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from openai import OpenAI
import base64
import os

app = Flask(__name__)
CORS(app)

# 🔑 Configura tu API Key de OpenAI (usa variable de entorno si prefieres)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/identificar', methods=['POST'])
def identificar_ave():
    try:
        # Verificar si el usuario subió una imagen
        if 'image' not in request.files:
            return jsonify({'error': 'No se envió ninguna imagen'}), 400

        # Leer la imagen del formulario
        image_file = request.files['image']
        image_bytes = image_file.read()

        # Convertir la imagen a base64
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        # Enviar la imagen y el texto a OpenAI
        response = client.responses.create(
            model="gpt-4o-mini",  # o "gpt-4o" si lo tienes habilitado
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": (
                                "Eres un ornitólogo experto. "
                                "Analiza esta imagen y dime qué ave aparece. "
                                "Describe su especie, color, tamaño, hábitat y comportamiento típico. "
                                "Responde en español."
                            ),
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{image_b64}",
                        },
                    ],
                }
            ],
        )

        # Obtener el texto generado
        descripcion = response.output_text

        return jsonify({'descripcion': descripcion})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Error procesando la imagen', 'detalle': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)


