import pandas as pd
import folium
from folium.plugins import HeatMap
import os

print("--> Generando mapa de calor...")

# 1. CARGAR LOS DATOS LIMPIOS
ruta_datos = 'data/processed/siniestros_conce_limpio.csv'
try:
    df = pd.read_csv(ruta_datos)
except FileNotFoundError:
    print(f"[ERROR] No se encontró el archivo {ruta_datos}. Ejecuta limpieza.py primero.")
    exit()

# 2. CREAR EL MAPA BASE
# Coordenadas centrales de Concepción y un estilo de mapa claro ('CartoDB positron') 
# para que el calor resalte más.
mapa = folium.Map(location=[-36.8201, -73.0444], zoom_start=13, tiles='CartoDB positron')

# 3. PREPARAR LAS COORDENADAS
# Folium necesita una lista de pares [Latitud, Longitud]
coordenadas = df[['Lat', 'Lon']].values.tolist()

# 4. AÑADIR LA CAPA DE CALOR
# radius: tamaño del punto | blur: difuminado para que se mezclen
HeatMap(coordenadas, radius=14, blur=10, max_zoom=1).add_to(mapa)

# 5. GUARDAR EL RESULTADO
ruta_salida = 'mapa_calor_biobio.html'
mapa.save(ruta_salida)

print(f"--> ¡ÉXITO! Se han mapeado {len(coordenadas)} puntos críticos.")
print(f"--> Abre el archivo '{ruta_salida}' dándole doble clic para verlo en tu navegador.")