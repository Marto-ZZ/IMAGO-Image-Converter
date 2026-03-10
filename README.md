# 🖼️ IMAGO — Image Convertor

Proyecto portfolio: Herramienta web minimalista para convertir imágenes de forma rápida, con frontend en **HTML/CSS** y backend en **Python/Flask**.

---

## 📁 Estructura del proyecto

```
IMAGO - Image Convertor/
├── app.py           ← Servidor Flask y manejo de rutas
├── converter.py     ← Lógica de procesamiento de imágenes (Pillow)
├── requirements.txt ← Dependencias del proyecto
├── static/          
│   └── styles.css   ← Diseño visual, variables CSS y Grid
└── templates/       
    └── index.html   ← Interfaz de usuario y lógica para archivos
```

---

## Cómo ejecutar

### 1. Instalar dependencias Python

```bash
pip install -r requirements.txt
```

### 2. Iniciar el backend

**Para desarrollo local**

```bash
python app.py
```

El servidor quedará disponible en `http://127.0.0.1:5000`.

**para entorno de producción (Linux/Mac)**

```bash
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

### 3. Abrir el frontend

Abrí `index.html` en tu navegador directamente, o usá una extensión como **Live Server** en VS Code.

---

## Funcionalidades

- Conversión Multiformato: soporte bidireccional entre JPG, PNG y WEBP
- Interfaz Drag & Drop: zona interactiva para arrastrar archivos o seleccionar mediante click con feedback visual dinámico
- Gestión Inteligente de Color: Conversión automática de canales alfa (transparencia) a color sólido al exportar a formatos que no soportan transparencia (como JPG), evitando errores de renderizado
- Experiencia de Usuario: Descarga automática e inmediata del archivo procesado sin recargas de página

## Funcionalidades a implementar

- Soporte para GIF: Implementar la conversión de frames de video o ráfagas de imágenes a formato .gif
- Modo Claro / Oscuro: Switch dinámico para cambiar la paleta de colores de la interfaz
- Procesamiento por lotes: Permitir la subida de múltiples imágenes simultáneamente y descargarlas en un archivo .zip

---

## Tecnologías utilizadas

| Capa      | Tecnología                        |
|-----------|-----------------------------------|
| Frontend  | HTML5, CSS3                       |
| Backend   | Python 3, Flask                   |
| Imagenes  | Pillow (PIL Fork)                 |

## 📝 Notas de desarrollo

Este proyecto nace de la necesidad de simplificar el flujo de trabajo/edición al encontrarse con imágenes en formato .webp, las cuales a menudo presentan problemas de compatibilidad en software de edición o visores antiguos.
Se puso especial énfasis en la privacidad: los archivos se procesan en el servidor y se envían de vuelta al usuario como un flujo de datos, sin persistencia de archivos a largo plazo en el sistema de archivos del servidor.

## Desarrollado con ❤️ por Martín Sogoloff
