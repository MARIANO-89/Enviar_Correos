import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import re

# Cargar las variables de entorno
load_dotenv()
CORREO_EMISOR = os.getenv("EMAIL_SENDER")
CONTRASEÑA_APLICACION = os.getenv("EMAIL_PASSWORD")

if not CORREO_EMISOR or not CONTRASEÑA_APLICACION:
    print("Error: Las credenciales de correo no están configuradas.")
    exit()

# Configuración de Flask
app = Flask(__name__, static_folder='static')

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/enviar', methods=['POST'])
def enviar_correos():
    try:
        asunto = request.form['asunto']
        mensaje = request.form['mensaje']
        archivo_csv = request.files['csv']

        # Guardar el archivo CSV de forma temporal
        filename = secure_filename(archivo_csv.filename)
        filepath = os.path.join("static", filename)
        archivo_csv.save(filepath)

        # Leer el archivo CSV
        df = pd.read_csv(filepath, sep=';')

        if 'Email' not in df.columns or 'Nombre' not in df.columns:
            return jsonify({"message": "El CSV debe contener las columnas 'Email' y 'Nombre'"}), 400

        # Configurar el servidor SMTP
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(CORREO_EMISOR, CONTRASEÑA_APLICACION)

        total = len(df)
        enviados = 0
        errores = 0

        for index, row in df.iterrows():
            email = row['Email'].strip()
            nombre = row['Nombre'].strip()

            if not validar_email(email):
                errores += 1
                continue

            msg = MIMEMultipart()
            msg['From'] = CORREO_EMISOR
            msg['Subject'] = asunto
            msg['To'] = email
            mensaje_personalizado = f"""
            <html>
            <body>
                <p>Hola {nombre},</p>
                <p>{mensaje}</p>
                <p>¡Esperamos verte pronto 🥳!</p>
            </body>
            </html>
            """
            msg.attach(MIMEText(mensaje_personalizado, 'html'))
            server.sendmail(CORREO_EMISOR, email, msg.as_string())
            enviados += 1

        server.quit()

        # Eliminar el archivo temporal
        os.remove(filepath)

        return jsonify({"message": f"Correos enviados: {enviados}\nErrores en emails: {errores}"}), 200

    except Exception as e:
        return jsonify({"message": f"Error al enviar correos: {str(e)}"}), 500


# Función para validar emails
def validar_email(email):
    patron = r"^[a-zA-Z0-9_.+-]+@[a-zAZ0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(patron, email)


if __name__ == '__main__':
    app.run(debug=True)
