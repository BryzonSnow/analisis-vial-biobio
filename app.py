import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Seguridad Vial Biobío", layout="wide")

# 2. ENCABEZADO
st.title("Vulnerabilidad Vial en el Gran Concepción")
st.markdown("""
Bienvenido al panel interactivo. Aquí puede visualizar espacialmente dónde ocurren los siniestros 
más críticos que involucran vehículos de dos ruedas. 
Utilice los parámetros a continuación para filtrar e interactuar con los datos en tiempo real.
""")

# 3. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    try:
        df = pd.read_csv('data/processed/siniestros_conce_limpio.csv')
        df['Tipo_Vehiculo'] = df['Archivo_Origen'].apply(lambda x: 'Bicicleta' if 'bici' in str(x).lower() else 'Motocicleta')
        return df
    except FileNotFoundError:
        st.error("No se encontró el archivo de datos. Por favor, asegúrese de ejecutar los scripts de limpieza primero.")
        return pd.DataFrame()

df = cargar_datos()

if not df.empty:
    st.divider()

    # ==========================================
    # SECCIÓN 1: FILTROS EVIDENTES
    # ==========================================
    st.subheader("1. Parámetros de Búsqueda")
    
    col_filtro1, col_filtro2 = st.columns(2)
    
    with col_filtro1:
        comunas_disponibles = sorted(df['Comuna'].unique().tolist())
        comunas_seleccionadas = st.multiselect(
            "Seleccione las comunas a analizar:", 
            options=comunas_disponibles, 
            default=comunas_disponibles
        )

    with col_filtro2:
        vehiculos_seleccionados = st.multiselect(
            "Seleccione los tipos de vehículo:", 
            options=["Bicicleta", "Motocicleta"], 
            default=["Bicicleta", "Motocicleta"]
        )

    # Aplicar filtros
    df_filtrado = df[
        (df['Comuna'].isin(comunas_seleccionadas)) & 
        (df['Tipo_Vehiculo'].isin(vehiculos_seleccionados))
    ]

    st.divider()

    # ==========================================
    # SECCIÓN 2: INDICADORES (KPIs)
    # ==========================================
    st.subheader("2. Resumen de Impacto (Datos Filtrados)")
    
    if df_filtrado.empty:
        st.warning("No hay datos para la combinación seleccionada. Por favor, ajuste los parámetros de búsqueda.")
    else:
        col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
        
        col_kpi1.metric("Total de Siniestros", len(df_filtrado))
        
        fallecidos = df_filtrado['Fallecidos'].sum() if 'Fallecidos' in df_filtrado.columns else 0
        graves = df_filtrado['Graves'].sum() if 'Graves' in df_filtrado.columns else 0
        
        col_kpi2.metric("Víctimas Fatales", int(fallecidos))
        col_kpi3.metric("Heridos Graves", int(graves))

    st.divider()

    # ==========================================
    # SECCIÓN 3: MAPA INTERACTIVO
    # ==========================================
    st.subheader("3. Mapa de Calor (Puntos Críticos)")
    st.markdown("*Las zonas de mayor intensidad térmica indican una alta concentración histórica de siniestros viales.*")

    # Crear el mapa
    mapa = folium.Map(location=[-36.8201, -73.0444], zoom_start=12, tiles='CartoDB dark_matter')

    # Añadir capas solo si hay datos filtrados
    if not df_filtrado.empty:
        if "Bicicleta" in vehiculos_seleccionados:
            coords_bicis = df_filtrado[df_filtrado['Tipo_Vehiculo'] == 'Bicicleta'][['Lat', 'Lon']].dropna().values.tolist()
            if coords_bicis:
                gradiente_bicis = {0.4: '#00d2ff', 0.6: '#3a7bd5', 1.0: '#00ff00'}
                HeatMap(coords_bicis, radius=15, blur=10, gradient=gradiente_bicis).add_to(folium.FeatureGroup(name='Bicicletas').add_to(mapa))

        if "Motocicleta" in vehiculos_seleccionados:
            coords_motos = df_filtrado[df_filtrado['Tipo_Vehiculo'] == 'Motocicleta'][['Lat', 'Lon']].dropna().values.tolist()
            if coords_motos:
                gradiente_motos = {0.4: '#ffff00', 0.6: '#ff9900', 1.0: '#ff0000'}
                HeatMap(coords_motos, radius=15, blur=10, gradient=gradiente_motos).add_to(folium.FeatureGroup(name='Motocicletas').add_to(mapa))

        folium.LayerControl().add_to(mapa)

    # Mostrar mapa en Streamlit
    st_folium(mapa, width=1000, height=500, returned_objects=[])
    st.caption("Fuente de datos: Catálogo de Datos Abiertos de CONASET.")