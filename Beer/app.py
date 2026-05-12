import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Beer Selector Pro", page_icon="🍺", layout="wide")

# 2. TÍTULO Y DESCRIPCIÓN
st.title("🍺 Seleccionador de Cervezas")
st.markdown("""
Esta aplicación utiliza **Machine Learning (K-Means Clustering)** para agrupar estilos de cerveza 
por su perfil técnico y ayudarte a encontrar la opción ideal según tus gustos.
""")

# 3. CARGA DE DATOS (Lee el archivo generado por el Notebook)
@st.cache_data
def preparar_datos():
    # Intenta cargar el archivo directamente
    nombre_archivo = "beer_data_cleaned.csv"
    
    # Si falla, intenta buscarlo en la subcarpeta (ruta relativa para Streamlit)
    if os.path.exists(nombre_archivo):
        return pd.read_csv(nombre_archivo)
    elif os.path.exists(f"Beer/{nombre_archivo}"):
        return pd.read_csv(f"Beer/{nombre_archivo}")
    else:
        st.error("⚠️ No se encontró el archivo CSV.")
        st.stop()
    # Nombre del archivo que exportaste desde el .ipynb
    nombre_archivo = "beer_data_cleaned.csv"
    
    if os.path.exists(nombre_archivo):
        return pd.read_csv(nombre_archivo)
    else:
        # Si el archivo no existe, mostramos instrucciones y detenemos la app
        st.error(f"⚠️ No se encontró el archivo '{nombre_archivo}'.")
        st.info("""
        **Instrucciones para solucionar esto:**
        1. Abre tu archivo `seleccionador_cervezas.ipynb`.
        2. Ve a la última celda y asegúrate de guardar tu DataFrame procesado ejecutando: 
           `df_model.to_csv("beer_data_cleaned.csv", index=False)`
        3. Asegúrate de que el archivo CSV esté en la misma carpeta que este script `app.py`.
        """)
        st.stop()

df = preparar_datos()

# 4. BARRA LATERAL (FILTROS)
st.sidebar.header("🎯 Define tu Perfil")

with st.sidebar:
    # Creamos listas de opciones únicas para los selectores
    sabor_list = sorted(df['sabor'].dropna().unique())
    color_list = sorted(df['color'].dropna().unique())
    
    sabor_input = st.selectbox("¿Qué sabor buscas?", options=sabor_list)
    color_input = st.selectbox("Color preferido:", options=color_list)
    
    # Slider para el grado de alcohol
    abv_input = st.slider("Graduación Alcohólica deseada (ABV %)", 
                          min_value=float(df['abv_prom_%'].min()), 
                          max_value=float(df['abv_prom_%'].max()), 
                          value=5.0, 
                          step=0.5)
    
    # Radio para el tipo de fermentación
    opciones_ferm = ["Todas"] + sorted(df['fermentacion'].dropna().unique().tolist())
    tipo_ferm = st.radio("Tipo de Fermentación:", options=opciones_ferm)

# 5. LÓGICA DE FILTRADO
margen = 1.5 # Margen de error para el ABV
filtro = (
    (df['sabor'].str.contains(sabor_input, case=False, na=False)) & 
    (df['color'].str.contains(color_input, case=False, na=False)) &
    (df['abv_prom_%'].between(abv_input - margen, abv_input + margen))
)

if tipo_ferm != "Todas":
    filtro &= (df['fermentacion'] == tipo_ferm)

recomendaciones = df[filtro].copy()

# 6. MOSTRAR RESULTADOS
st.subheader(f"📊 Resultados encontrados: {len(recomendaciones)}")

if not recomendaciones.empty:
    # Calculamos la proximidad al ABV deseado para ordenar los mejores resultados
    recomendaciones['Proximidad'] = abs(recomendaciones['abv_prom_%'] - abv_input)
    resultados = recomendaciones.sort_values(by='Proximidad').head(5)

    # Crear columnas dinámicas según la cantidad de resultados
    cols = st.columns(len(resultados))
    
    for i, (idx, row) in enumerate(resultados.iterrows()):
        with cols[i]:
            st.info(f"**{row['estilo'].upper()}**")
            st.metric("ABV", f"{row['abv_prom_%']}%")
            st.write(f"**Amargor:** {int(row['ibu_prom'])} IBU")
            st.write(f"**Categoría:** {row['fermentacion'].capitalize()}")
            st.caption(f"Cluster: {row['nombre_cluster']}")
            
    #
