import pandas as pd
import folium
from folium.plugins import HeatMap
import math

print("--> Generando mapas de calor por categoría...")

# 1. CARGAR LOS DATOS
ruta_datos = 'data/processed/siniestros_conce_limpio.csv'
try:
    df = pd.read_csv(ruta_datos)
except FileNotFoundError:
    print(f"[ERROR] No se encontró el archivo {ruta_datos}.")
    exit()

# 2. CREAR MAPA BASE (Fondo oscuro o claro, 'CartoDB dark_matter' hace resaltar mucho el calor)
mapa = folium.Map(location=[-36.8201, -73.0444], zoom_start=13, tiles='CartoDB dark_matter')

# 3. SEPARAR LAS COORDENADAS POR TIPO
# Convertimos todo a minúsculas y rellenamos nulos para evitar errores
df['Archivo_Origen'] = df['Archivo_Origen'].astype(str).str.lower()

# Filtramos y extraemos solo las listas de [Latitud, Longitud]
coords_bicis = df[df['Archivo_Origen'].str.contains('bici')][['Lat', 'Lon']].dropna().values.tolist()
coords_motos = df[df['Archivo_Origen'].str.contains('moto')][['Lat', 'Lon']].dropna().values.tolist()

# 4. CREAR LAS CAPAS (FeatureGroups)
capa_bicis = folium.FeatureGroup(name='Calor: Bicicletas')
capa_motos = folium.FeatureGroup(name='Calor: Motocicletas')

# 5. CONFIGURAR LOS MAPAS DE CALOR CON COLORES PERSONALIZADOS
# Gradiente para Bicis (Tonos azules y verdes)
gradiente_bicis = {0.4: '#00d2ff', 0.6: '#3a7bd5', 0.8: '#00ff00', 1.0: '#008000'}
HeatMap(
    coords_bicis, 
    radius=15, 
    blur=10, 
    gradient=gradiente_bicis
).add_to(capa_bicis)

# Gradiente para Motos (Tonos amarillos y rojos)
gradiente_motos = {0.4: '#ffff00', 0.6: '#ff9900', 0.8: '#ff0000', 1.0: '#8b0000'}
HeatMap(
    coords_motos, 
    radius=15, 
    blur=10, 
    gradient=gradiente_motos
).add_to(capa_motos)

# 6. AÑADIR AL MAPA BASE
capa_bicis.add_to(mapa)
capa_motos.add_to(mapa)

# 7. AÑADIR CONTROLADOR DE CAPAS
folium.LayerControl(position='topright').add_to(mapa)

# 8. GUARDAR
ruta_salida = 'mapa_calor_interactivo.html'
mapa.save(ruta_salida)

print(f"--> ¡ÉXITO! Capas generadas: {len(coords_bicis)} bicis y {len(coords_motos)} motos.")
print(f"--> Abre '{ruta_salida}' en tu navegador.")