import streamlit as st
import pandas as pd
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Beer Selector Pro", page_icon="🍺", layout="wide")

# 2. TÍTULO Y DESCRIPCIÓN
st.title("🍺 Seleccionador de Cervezas")
st.markdown("""
Esta aplicación usa un algoritmo de Machine Learning para agrupar estilos de cerveza 
por su perfil técnico y ayudarte a encontrar la opción ideal según tus gustos.
""")

# 3. CARGA DE DATOS
@st.cache_data
def preparar_datos():
    nombre_archivo = "beer_data_cleaned.csv"
    
    if os.path.exists(nombre_archivo):
        return pd.read_csv(nombre_archivo)
    elif os.path.exists(f"Beer/{nombre_archivo}"):
        return pd.read_csv(f"Beer/{nombre_archivo}")
    else:
        st.error("⚠️ No se encontró el archivo CSV.")
        st.stop()

df = preparar_datos()

# 4. FILTROS EN LA PARTE SUPERIOR (Diseño responsivo para Móviles)
# Envolvemos los filtros en un contenedor estético con borde
with st.container(border=True):
    st.subheader("🎯 Define tu perfil de cerveza")
    st.write("Configura tus preferencias aquí abajo para sugerirte la cerveza ideal:")
    
    # Creamos listas de opciones únicas para los selectores
    sabor_list = sorted(df['sabor'].dropna().unique())
    color_list = sorted(df['color'].dropna().unique())
    
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
filtro = (
    (df['sabor'].str.contains(sabor_input, case=False, na=False)) & 
    (df['color'].str.contains(color_input, case=False, na=False)) &
    (df['abv_prom_%'].between(abv_input - margen, abv_input + margen))
)

if tipo_ferm != "Todas":
    filtro &= (df['fermentacion'] == tipo_ferm)

recomendaciones = df[filtro].copy()

# 6. MOSTRAR RESULTADOS (Diseño de Tarjetas Cuadrículas optimizado)
st.subheader(f"📊 Cervezas recomendadas: {len(recomendaciones)}")

if not recomendaciones.empty:
    # Calculamos la proximidad al ABV deseado para ordenar los mejores resultados
    recomendaciones['Proximidad'] = abs(recomendaciones['abv_prom_%'] - abv_input)
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