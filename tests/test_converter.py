#tests para converter.py
#ejecutar con: pytest test_converter.py -v
import os
import pytest
from PIL import Image
from converter import cambiar_formato_imagen, FORMATOS_SOPORTADOS


# fixtures

@pytest.fixture
def imagen_rgb(tmp_path):
    #imagen RGB de prueba sin canal alfa
    ruta = tmp_path / "test_rgb.png"
    img = Image.new("RGB", (100, 100), color=(200, 100, 50))
    img.save(ruta)
    return str(ruta)

@pytest.fixture
def imagen_rgba(tmp_path):
    #imagen RGBA de prueba con canal alfa (transparencia)
    ruta = tmp_path / "test_rgba.png"
    img = Image.new("RGBA", (100, 100), color=(200, 100, 50, 128))
    img.save(ruta)
    return str(ruta)


# conversiones basicas

class TestConversionesBasicas:

    def test_png_a_jpg(self, imagen_rgb):
        resultado = cambiar_formato_imagen(imagen_rgb, "jpg")
        assert resultado.endswith(".jpg")
        assert os.path.exists(resultado)

    def test_png_a_webp(self, imagen_rgb):
        resultado = cambiar_formato_imagen(imagen_rgb, "webp")
        assert resultado.endswith(".webp")
        assert os.path.exists(resultado)

    def test_png_a_bmp(self, imagen_rgb):
        resultado = cambiar_formato_imagen(imagen_rgb, "bmp")
        assert resultado.endswith(".bmp")
        assert os.path.exists(resultado)

    def test_png_a_tiff(self, imagen_rgb):
        resultado = cambiar_formato_imagen(imagen_rgb, "tiff")
        assert resultado.endswith(".tiff")
        assert os.path.exists(resultado)

    def test_png_a_gif(self, imagen_rgb):
        resultado = cambiar_formato_imagen(imagen_rgb, "gif")
        assert resultado.endswith(".gif")
        assert os.path.exists(resultado)

    def test_jpeg_normaliza_a_jpg(self, imagen_rgb):
        #el alias "jpeg" debe generar un archivo .jpg para evitar confusiones
        resultado = cambiar_formato_imagen(imagen_rgb, "jpeg")
        assert resultado.endswith(".jpg")

    def test_formato_con_punto_delante(self, imagen_rgb):
        #debe aceptar formatos con punto al inicio, como ".png"
        resultado = cambiar_formato_imagen(imagen_rgb, ".png")
        assert resultado.endswith(".png")

    def test_formato_en_mayusculas(self, imagen_rgb):
        #debe aceptar formatos en mayusculas, los normalizamos internamente
        resultado = cambiar_formato_imagen(imagen_rgb, "JPG")
        assert resultado.endswith(".jpg")


# manejo de transparencia

class TestTransparencia:

    def test_rgba_a_jpg_sin_error(self, imagen_rgba):
        #jpg no soporta alfa, la funcion debe aplanar el canal sin explotar
        resultado = cambiar_formato_imagen(imagen_rgba, "jpg")
        img = Image.open(resultado)
        assert img.mode == "RGB"

    def test_rgba_a_bmp_sin_error(self, imagen_rgba):
        #bmp tampoco soporta alfa
        resultado = cambiar_formato_imagen(imagen_rgba, "bmp")
        assert os.path.exists(resultado)

    def test_rgba_a_png_conserva_alfa(self, imagen_rgba):
        #png si soporta transparencia, no debe perderla
        resultado = cambiar_formato_imagen(imagen_rgba, "png")
        img = Image.open(resultado)
        assert img.mode == "RGBA"


# control de calidad

class TestCalidad:

    def test_calidad_baja_genera_archivo_mas_pequeno(self, imagen_rgb):
        #un jpg con calidad 10 deberia pesar menos que uno con calidad 90
        alta = cambiar_formato_imagen(imagen_rgb, "jpg", calidad=90)
        ruta2 = imagen_rgb.replace("test_rgb", "test_rgb2")
        Image.new("RGB", (100, 100), color=(200, 100, 50)).save(ruta2)
        baja = cambiar_formato_imagen(ruta2, "jpg", calidad=10)
        assert os.path.getsize(baja) <= os.path.getsize(alta)

    def test_calidad_valida_minima(self, imagen_rgb):
        resultado = cambiar_formato_imagen(imagen_rgb, "jpg", calidad=1)
        assert os.path.exists(resultado)

    def test_calidad_valida_maxima(self, imagen_rgb):
        resultado = cambiar_formato_imagen(imagen_rgb, "jpg", calidad=95)
        assert os.path.exists(resultado)


# errores esperados

class TestErrores:

    def test_formato_invalido(self, imagen_rgb):
        #debe lanzar ValueError con un mensaje claro si el formato no existe
        with pytest.raises(ValueError, match="no soportado"):
            cambiar_formato_imagen(imagen_rgb, "exe")

    def test_calidad_fuera_de_rango_alto(self, imagen_rgb):
        with pytest.raises(ValueError, match="calidad"):
            cambiar_formato_imagen(imagen_rgb, "jpg", calidad=100)

    def test_calidad_fuera_de_rango_bajo(self, imagen_rgb):
        with pytest.raises(ValueError, match="calidad"):
            cambiar_formato_imagen(imagen_rgb, "jpg", calidad=0)

    def test_archivo_inexistente(self, tmp_path):
        #debe lanzar FileNotFoundError si la imagen no existe en el sistema
        with pytest.raises(FileNotFoundError):
            cambiar_formato_imagen(str(tmp_path / "no_existe.png"), "jpg")


# integridad del archivo resultado

class TestIntegridadArchivo:

    def test_archivo_resultado_no_esta_vacio(self, imagen_rgb):
        resultado = cambiar_formato_imagen(imagen_rgb, "webp")
        assert os.path.getsize(resultado) > 0

    def test_imagen_resultado_es_legible(self, imagen_rgb):
        #pillow debe poder abrir el archivo convertido sin errores
        resultado = cambiar_formato_imagen(imagen_rgb, "jpg")
        img = Image.open(resultado)
        img.verify()

    def test_dimensiones_se_conservan(self, imagen_rgb):
        #la conversion no debe alterar el tamaño de la imagen
        resultado = cambiar_formato_imagen(imagen_rgb, "webp")
        img = Image.open(resultado)
        assert img.size == (100, 100)

    @pytest.mark.parametrize("formato", FORMATOS_SOPORTADOS)
    def test_todos_los_formatos_soportados(self, imagen_rgb, formato):
        #cada formato en FORMATOS_SOPORTADOS debe convertirse sin errores
        resultado = cambiar_formato_imagen(imagen_rgb, formato)
        assert os.path.exists(resultado)