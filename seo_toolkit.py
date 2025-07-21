
import streamlit as st
from PIL import Image
from io import BytesIO
import openai

st.set_page_config(page_title="Herramienta SEO Todo-en-Uno", layout="wide")
st.title("🧠 Herramienta SEO Todo-en-Uno")

# 🔑 Campo para API Keys
st.sidebar.title("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")
openai_api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# 🧠 Generador de artículo SEO
def generar_articulo(keyword):
    if not openai_api_key:
        return {
            "titulo": f"Cómo optimizar tu sitio para '{keyword}'",
            "meta": f"Descubre cómo mejorar el SEO de tu sitio usando la palabra clave '{keyword}'.",
            "contenido": f"""
## Introducción

El SEO es clave para aumentar el tráfico web. Hoy te mostraremos cómo usar '{keyword}' efectivamente.

### Paso 1: Investigación de palabras clave
Encuentra variaciones útiles como '{keyword} barato', '{keyword} en 2025', etc.

### Paso 2: Contenido optimizado
Escribe artículos relevantes, como este.

### Paso 3: Técnica On-Page
Incluye '{keyword}' en títulos, encabezados y descripciones.

### Conclusión
Aplicar '{keyword}' puede mejorar tus rankings notablemente.
"""
        }
    else:
        openai.api_key = openai_api_key
        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Eres un redactor experto en SEO."},
                {"role": "user", "content": f"Escribe un artículo SEO completo sobre '{keyword}' con introducción, pasos prácticos y conclusión."}
            ],
            max_tokens=900,
            temperature=0.7
        )
        contenido = respuesta["choices"][0]["message"]["content"]
        return {
            "titulo": f"Guía completa sobre '{keyword}'",
            "meta": f"Aprende cómo posicionar mejor usando la palabra clave '{keyword}'.",
            "contenido": contenido
        }

# 🖼️ Generador de imagen (puedes integrar DALL·E si tienes clave)
def generar_imagen_desde_texto(texto):
    return Image.new("RGB", (512, 300), color="gray")

# ⬇️ Descargar artículo como HTML
def descargar_como_html(titulo, contenido):
    html_content = f"<h1>{titulo}</h1>\n{contenido.replace('\n', '<br>')}"
    b = BytesIO()
    b.write(html_content.encode())
    b.seek(0)
    return b

# Interfaz de pestañas
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📝 Generador de Artículos",
    "🖼️ Generador de Imágenes",
    "🔍 Análisis SEO",
    "🔎 Simulador SERP",
    "⬇️ Exportar"
])

with tab1:
    keyword = st.text_input("Introduce una palabra clave:")
    if st.button("Generar artículo"):
        resultado = generar_articulo(keyword)
        st.subheader("Título:")
        st.write(resultado["titulo"])
        st.subheader("Meta descripción:")
        st.write(resultado["meta"])
        st.subheader("Contenido:")
        st.text_area("Artículo generado:", value=resultado["contenido"], height=300)

with tab2:
    texto_img = st.text_input("Describe la imagen que quieres generar:")
    if st.button("Generar imagen"):
        imagen = generar_imagen_desde_texto(texto_img)
        st.image(imagen, caption="Imagen generada")

with tab3:
    texto_seo = st.text_area("Pega aquí tu contenido para analizar:")
    if texto_seo:
        palabras = texto_seo.lower().split()
        long_total = len(texto_seo)
        densidad = {palabra: palabras.count(palabra) for palabra in set(palabras) if len(palabra) > 4}
        st.write("🔍 Densidad de palabras clave (longitud > 4 letras):")
        st.write(sorted(densidad.items(), key=lambda x: -x[1])[:10])
        st.write(f"🧾 Longitud total del texto: {long_total} caracteres")

with tab4:
    titulo_serp = st.text_input("Título SEO:")
    descripcion_serp = st.text_area("Meta descripción:")
    if titulo_serp or descripcion_serp:
        st.markdown("### Vista previa SERP")
        st.markdown(f"""
<div style='border:1px solid #ccc; padding:10px;'>
  <span style='color: #1a0dab; font-size:18px;'>{titulo_serp}</span><br>
  <span style='color: green;'>https://www.tusitio.com/{keyword.replace(" ", "-")}</span><br>
  <span>{descripcion_serp}</span>
</div>
""", unsafe_allow_html=True)

with tab5:
    if keyword:
        articulo = generar_articulo(keyword)
        archivo = descargar_como_html(articulo["titulo"], articulo["contenido"])
        st.download_button("📥 Descargar como HTML", data=archivo, file_name="articulo_seo.html", mime="text/html")
