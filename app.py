import os
import base64
from converter import cambiar_formato_imagen
from flask import Flask, render_template, request, send_file, jsonify

#flask es un "micro framework" para crear aplicaciones web, me va a ayudar a darle funcionalidad web a mi programa

#declaramos la inizializacion de flask
app = Flask(__name__)

#declaramos la carpeta donde se van a guardar las imagenes subidas
#si la misma no existe la creamos
CARPETA_SUBIDAS = 'uploads'
os.makedirs(CARPETA_SUBIDAS, exist_ok=True)


#indica la ruta principal de la aplicacion
#inicio(): es la funcion que se va a ejecutar cuando se acceda a la ruta principal
@app.route('/')
def inicio():
    #renderiza el archivo index.html
    return render_template('index.html')


#ruta nueva: convierte la imagen y la devuelve como base64 para mostrar el preview en el navegador
#no descarga nada, solo muestra como va a quedar la imagen antes de confirmar
@app.route('/preview', methods=['POST'])
def preview():
    try:
        #obtenemos el archivo y los parametros del usuario
        archivo = request.files.get('archivo_del_usuario')
        formato = request.form.get('formato_a_cambiar', 'png')
        calidad = int(request.form.get('calidad', 85))

        #verificamos que el usuario haya subido un archivo
        if not archivo or archivo.filename == '':
            return jsonify({'error': 'no seleccionaste ningun archivo.'}), 400

        #creamos la ruta completa del archivo subido
        #guardamos el archivo en la carpeta de uploads
        ruta_original = os.path.join(CARPETA_SUBIDAS, archivo.filename)
        archivo.save(ruta_original)

        #llamamos a la funcion cambiar_formato_imagen para convertir la imagen
        ruta_convertida = cambiar_formato_imagen(ruta_original, formato, calidad)

        #leemos el archivo convertido y lo codificamos en base64 para mandarlo como data url al navegador
        with open(ruta_convertida, 'rb') as f:
            datos = f.read()

        #mapeamos la extension al tipo MIME que entiende el navegador
        mime_types = {
            'jpg': 'image/jpeg', 'jpeg': 'image/jpeg',
            'png': 'image/png',  'webp': 'image/webp',
            'bmp': 'image/bmp',  'tiff': 'image/tiff',
            'gif': 'image/gif',
        }
        ext      = formato.strip('.').lower()
        mime     = mime_types.get(ext, 'image/png')
        data_url = f"data:{mime};base64,{base64.b64encode(datos).decode()}"

        #calculamos el tamaño en KB para mostrarselo al usuario
        tamano_kb = round(len(datos) / 1024, 1)

        return jsonify({
            'preview':    data_url,
            'nombre':     os.path.basename(ruta_convertida),
            'tamano_kb':  tamano_kb,
        })

    #separamos ValueError para dar mensajes claros cuando el formato o la calidad son invalidos
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'ocurrio un error: {e}'}), 500


#indica la ruta para convertir la imagen, solo acepta el metodo POST
@app.route('/convertir', methods=['POST'])
def procesar():
    #funcion que se va a ejecutar cuando se acceda a la ruta /convertir
    try:
        #obtenemos el archivo subido por el usuario
        archivo = request.files.get('archivo_del_usuario')

        #obtenemos el formato y la calidad que el usuario quiere
        formato  = request.form.get('formato_a_cambiar', 'png')
        calidad  = int(request.form.get('calidad', 85))

        #verificamos que el usuario haya subido un archivo
        if not archivo or archivo.filename == '':
            return 'no seleccionaste ningun archivo.', 400

        #creamos la ruta completa del archivo subido
        #guardamos el archivo en la carpeta de uploads
        ruta_original = os.path.join(CARPETA_SUBIDAS, archivo.filename)
        archivo.save(ruta_original)

        #llamamos a la funcion cambiar_formato_imagen para convertir la imagen
        ruta_convertida = cambiar_formato_imagen(ruta_original, formato, calidad)

        #enviamos el archivo convertido al usuario para que lo descargue
        return send_file(ruta_convertida, as_attachment=True)

    #si no se cumple alguna de las condiciones anteriores, devolvemos un error
    except ValueError as e:
        return str(e), 400
    except Exception as e:
        return f'ocurrio un error: {e}', 500


#si el archivo es ejecutado directamente, iniciamos la aplicacion web
if __name__ == '__main__':
    app.run(debug=True)