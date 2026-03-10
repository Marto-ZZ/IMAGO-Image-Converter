import os
from converter import cambiar_formato_imagen
from flask import Flask, render_template, request, send_file

#flask es un "micro framework" para crear aplicaciones web, me va a ayudar a darle funcionalidad web a mi programa

#declaramos la inizializacion de flask
app = Flask(__name__)

#declaramos la carpeta donde se van a guardar las imagenes subidas
#si la misma no existe la creamos
CARPETA_SUBIDAS = 'uploads'
os.makedirs(CARPETA_SUBIDAS, exist_ok=True)


#indica la ruta principal de la aplicacion
#def_inicio(): es la funcion que se va a ejecutar cuando se acceda a la ruta principal
@app.route('/')
def inicio():
    #renderiza el archivo index.html
    return render_template('index.html')


#indica la ruta para convertir la imagen, solo acepta el metodo POST
@app.route('/convertir', methods=['POST'])
def procesar():
     #funcion que se va a ejecutar cuando se acceda a la ruta /convertir
    try:
        #obtenemos el archivo subido por el usuario
        archivo = request.files['archivo_del_usuario'] 

        #obtenemos el formato al que el usuario quiere cambiar la imagen
        formato = request.form['formato_a_cambiar']

        #verificamos que el usuario haya subido un archivo
        if archivo.filename == '':             
            return "No seleccionaste ningún archivo."

        #creamos la ruta completa del archivo subido
        #guardamos el archivo en la carpeta de uploads 
        ruta_original = os.path.join(CARPETA_SUBIDAS, archivo.filename)
        archivo.save(ruta_original)

        #llamamos a la funcion cambiar_formato_imagen para convertir la imagen
        ruta_convertida = cambiar_formato_imagen(ruta_original, formato)

        #enviamos el archivo convertido al usuario para que lo descargue
        return send_file(ruta_convertida, as_attachment=True)

    #si no se cumple alguna de las condiciones anteriores, devolvemos un error
    except Exception as e:
        return f"Ocurrió un error: {e}"

#si el archivo es ejecutado directamente, iniciamos la aplicacion web
if __name__ == '__main__':
    app.run(debug=True)