from PIL import Image                                               
import os                                                           
#importamos la libreria Pillow para el manejo de imagenes
#importamos la libreria os para el manejo de archivos, directorios y extensiones

#lista de formatos soportados, la exportamos para usarla en los tests
FORMATOS_SOPORTADOS = ["png", "jpg", "jpeg", "webp", "bmp", "tiff", "gif"]

#funcion que toma una imagen y la convierte al formato que se le indique
#ahora tambien acepta un parametro de calidad para jpg y webp
def cambiar_formato_imagen(directorio_imagen, formato_a_cambiar, calidad=85):

    #verificamos que el archivo exista antes de intentar abrirlo
    if not os.path.exists(directorio_imagen):
        raise FileNotFoundError(f"no se encontro el archivo: {directorio_imagen}")

    #obtenemos la extension en minusculas y sin puntos
    extension_final = formato_a_cambiar.strip(".").lower()

    #verificamos que el formato pedido este dentro de los soportados
    if extension_final not in FORMATOS_SOPORTADOS:
        raise ValueError(f"formato '{extension_final}' no soportado. usa: {FORMATOS_SOPORTADOS}")

    #la calidad solo tiene sentido entre 1 y 95, fuera de ese rango pillow se comporta raro
    if not (1 <= calidad <= 95):
        raise ValueError(f"la calidad debe estar entre 1 y 95. se recibio: {calidad}")

    #localizamos la imagen en el sistema
    imagen = Image.open(directorio_imagen)

    #jpg y bmp no soportan canal alfa (transparencia), los convertimos a RGB para evitar errores
    if extension_final in ["jpg", "jpeg", "bmp"]:
        if imagen.mode in ("RGBA", "P", "LA"):
            imagen = imagen.convert("RGB")

    #tiff en modo paleta puede tener problemas, lo pasamos a RGBA para preservar la transparencia
    if extension_final == "tiff" and imagen.mode == "P":
        imagen = imagen.convert("RGBA")

    #creamos una variable con el nombre del archivo sin su extension, os lo toma como una tupla asi que lo que importa es el primer componente que es el nombre
    nombre_archivo, _ = os.path.splitext(directorio_imagen)

    #si la extension final es jpeg la cambiamos a jpg para evitar confusiones
    extension_archivo = "jpg" if extension_final == "jpeg" else extension_final

    #creamos la variable a devolver con el nombre original anidado a la nueva extension
    nombre_final = f"{nombre_archivo}.{extension_archivo}"

    #mapeamos cada extension al nombre que usa pillow internamente
    mapa_formatos = {
        "jpg":  "JPEG",
        "jpeg": "JPEG",
        "png":  "PNG",
        "webp": "WEBP",
        "bmp":  "BMP",
        "tiff": "TIFF",
        "gif":  "GIF",
    }
    formato_de_pillow = mapa_formatos[extension_final]

    #la calidad solo aplica a jpg y webp, para el resto pillow la ignora o da error
    if formato_de_pillow in ("JPEG", "WEBP"):
        imagen.save(nombre_final, format=formato_de_pillow, quality=calidad)
    else:
        imagen.save(nombre_final, format=formato_de_pillow)

    return nombre_final