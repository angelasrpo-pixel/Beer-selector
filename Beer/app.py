import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Beer Selector Pro", page_icon="🍺", layout="wide")

# 2. TÍTULO Y DESCRIPCIÓN
st.title("🍺 Seleccionador de Cervezas")
st.markdown("""
<<<<<<< HEAD
Esta aplicación utiliza **Machine Learning (K-Means Clustering)** para agrupar estilos de cerveza 
por su perfil técnico y ayudarte a encontrar la opción ideal según tus gustos.
""")

# 3. CARGA DE DATOS (Lee el archivo generado por el Notebook)
@st.cache_data
def preparar_datos():
    # Intenta cargar el archivo directamente
    nombre_archivo = "beer_data_cleaned.csv"
    
    # Si falla, intenta buscarlo en la subcarpeta (ruta relativa para Streamlit)
=======
Esta aplicación usa un algoritmo de Machine Learning para agrupar estilos de cerveza 
por su perfil técnico y ayudarte a encontrar la opción ideal según tus gustos.
""")

# 3. CARGA DE DATOS
@st.cache_data
def preparar_datos():
    nombre_archivo = "beer_data_cleaned.csv"
    
>>>>>>> 85238fe (Guardar progreso local)
    if os.path.exists(nombre_archivo):
        return pd.read_csv(nombre_archivo)
    elif os.path.exists(f"Beer/{nombre_archivo}"):
        return pd.read_csv(f"Beer/{nombre_archivo}")
    else:
        st.error("⚠️ No se encontró el archivo CSV.")
        st.stop()
<<<<<<< HEAD
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

# 4. BARRA (FILTROS)



st.header("🎯 Define tu Perfil")

with st.sidebar:
=======

df = preparar_datos()

# 4. FILTROS EN LA PARTE SUPERIOR (mejorado para móviles)
# Envolvemos los filtros en un contenedor estético con borde
with st.container(border=True):
    st.subheader("🎯 Define tu perfil de cerveza")
    st.write("Configura tus preferencias aquí abajo para sugerirte la cerveza ideal:")
    
>>>>>>> 85238fe (Guardar progreso local)
    # Creamos listas de opciones únicas para los selectores
    sabor_list = sorted(df['sabor'].dropna().unique())
    color_list = sorted(df['color'].dropna().unique())
    
<<<<<<< HEAD
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
=======
    # Distribución en columnas horizontales (en PC irán lado a lado, en celular se apilarán verticalmente)
    col1, col2 = st.columns(2)
    with col1:
        sabor_input = st.selectbox("¿Qué sabor buscas?", options=sabor_list)
    with col2:
        color_input = st.selectbox("¿Qué color prefieres en tu cerveza?", options=color_list)
    
    st.markdown("---") # Separador sutil
    
    col3, col4 = st.columns([1.5, 1]) # La columna del slider es un poco más ancha
    with col3:
        abv_input = st.slider("Graduación Alcohólica deseada (ABV %)", 
                              min_value=float(df['abv_prom_%'].min()), 
                              max_value=float(df['abv_prom_%'].max()), 
                              value=5.0, 
                              step=0.2)
    with col4:
        opciones_ferm = ["Todas"] + sorted(df['fermentacion'].dropna().unique().tolist())
        tipo_ferm = st.radio("Tipo de Fermentación:", options=opciones_ferm, horizontal=True) # horizontal=True ahorra espacio vertical

# 5. LÓGICA DE FILTRADO
margen = 0.8  # Margen de error para el ABV
>>>>>>> 85238fe (Guardar progreso local)
filtro = (
    (df['sabor'].str.contains(sabor_input, case=False, na=False)) & 
    (df['color'].str.contains(color_input, case=False, na=False)) &
    (df['abv_prom_%'].between(abv_input - margen, abv_input + margen))
)

if tipo_ferm != "Todas":
    filtro &= (df['fermentacion'] == tipo_ferm)

recomendaciones = df[filtro].copy()

<<<<<<< HEAD
# 6. MOSTRAR RESULTADOS
st.subheader(f"📊 Resultados encontrados: {len(recomendaciones)}")
=======
# 6. MOSTRAR RESULTADOS (Diseño de Tarjetas Cuadrículas optimizado)
st.subheader(f"📊 Cervezas recomendadas: {len(recomendaciones)}")
>>>>>>> 85238fe (Guardar progreso local)

if not recomendaciones.empty:
    # Calculamos la proximidad al ABV deseado para ordenar los mejores resultados
    recomendaciones['Proximidad'] = abs(recomendaciones['abv_prom_%'] - abv_input)
<<<<<<< HEAD
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
=======
    resultados = recomendaciones.sort_values(by='Proximidad').head(10)

    # 💡 MEJORA MOBILE-FIRST: Mostramos los resultados en filas de hasta 3 columnas máximo
    # Evita que las columnas colapsen si hay muchos resultados
    columnas_por_fila = 3
    
    for i in range(0, len(resultados), columnas_por_fila):
        chunk_resultados = resultados.iloc[i : i + columnas_por_fila]
        cols = st.columns(columnas_por_fila)
        
        for idx_col, (idx, row) in enumerate(chunk_resultados.iterrows()):
            with cols[idx_col]:
                # Estilo de tarjeta individual usando st.container
                with st.container(border=True):
                    st.markdown(f"### 🍺 {row['estilo'].upper()}")
                    st.metric("ABV", f"{row['abv_prom_%']}%")
                    st.write(f"**Amargor:** {int(row['ibu_prom'])} IBU")
                    st.write(f"**Categoría:** {row['fermentacion'].capitalize()}")
                    st.caption(f"Cluster ML: {row['nombre_cluster']}")
                    
else:
    st.warning("No se encontraron cervezas que coincidan con tus preferencias. Intenta ajustar los filtros.")
    
# Para ejecturar en stramlit, en la terminal ejecutar: streamlit run app.py
>>>>>>> 85238fe (Guardar progreso local)
