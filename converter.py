from PIL import Image
import os
#Importamos la libreria Pillow para el manejo de imagenes
#Importamos la libreria os para el manejo de archivos, directorios y extensiones


#funcion que toma una imagen y la convierte al formato que se le indique
def cambiar_formato_imagen(directorio_imagen, formato_a_cambiar):

    #localizamos la direccion de la imagen en el sistema
    #obtenemos la extension en minusculas y sin puntos
    imagen = Image.open(directorio_imagen)
    extension_final = formato_a_cambiar.strip(".").lower()

    #si es jpg o jpeg verificamos que no tenga canal alfa (transparencia)
    if extension_final in ["jpg", "jpeg"]:
        if imagen.mode in ("RGBA", "P"):                            
            imagen = imagen.convert("RGB")

    #creamos una variable con el nombre del archivo sin su extension, os lo toma como una tupla asi que lo que importa es el primer componenete que es el nombre
    nombre_archivo, _ = os.path.splitext(directorio_imagen)

    #si la extension final es jpeg la cambiamos a jpg para evitar confusiones
    if extension_final == "jpeg":
        extension_archivo = "jpg"
    else:
        extension_archivo = extension_final

    #creamos la variable a devolver con el nombre original anidado a la nueva extension
    nombre_final = f"{nombre_archivo}.{extension_archivo}"

    #pillow usa "JPEG" para ambos formatos
    if extension_final in ["jpg", "jpeg"]:
        formato_de_pillow = "JPEG"
    else:
        #si no es jpg o jpeg usamos la extension en mayusculas como formato de pillow
        formato_de_pillow = extension_final.upper()

    #guardamos la imagen en el nuevo formato
    imagen.save(nombre_final, format=formato_de_pillow)

    return nombre_final