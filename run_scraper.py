# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 23:47:50 2024

@author: Renzo
"""
import pandas as pd
import os
from scraper_clima import get_climate_url, scrape_climate_data


# Crear la carpeta 'data' si no existe
if not os.path.exists('./data'):
    os.makedirs('./data')

# Definiendo función para hacer scraping y obtener DataFrame
def procesar_datos(climate_url, parameter):
    """
    Procesa y guarda datos climáticos desde una URL específica.

    Esta función realiza el scraping de datos climáticos desde la URL proporcionada,
    formatea las columnas para facilitar la manipulación de datos y guarda los
    resultados en un archivo CSV.

    Parámetros:
    climate_url (str): La URL desde donde se obtendrán los datos climáticos.
    parameter (str): El parámetro climático específico (por ejemplo, 'tavg' para
                     anomalías de temperatura promedio, 'pcp' para precipitación).

    Acciones:
    - Realiza el scraping de los datos climáticos utilizando la función scrape_climate_data.
    - Renombra las columnas para facilitar la manipulación de datos.
    - Convierte la columna 'fecha' a un formato de fecha y hora.
    - Extrae la información de anomalía y la convierte a un formato decimal.
    - Extrae la información de ranking y la convierte a un entero.
    - Reordena el DataFrame.
    - Guarda el DataFrame en un archivo CSV en la carpeta './data'.

    Retorna:
    None
    """
    # Haciendo scraping y obteniendo DataFrame
    df = scrape_climate_data(climate_url)

    # Renombrando columnas para facilitar manipulación de datos
    df.columns = ['fecha', 'anomalía', 'ranking']

    # Convirtiendo la columna 'fecha' a Datetime
    df['fecha'] = pd.to_datetime(df['fecha'].str.strip(), format='%B %Y')

    # Extrayendo información de anomalía y convirtiendo a decimal
    df['anomalía'] = df['anomalía'].str.extract(r'(-?\d+\.\d+)')[0].astype('float')

    # Extrayendo información del ranking y convirtiendo a entero
    df['ranking'] = df['ranking'].astype('int')

    # Reordenar DataFrame
    df = df[['fecha', 'anomalía', 'ranking']]

    # Exportando DataFrame a CSV para su uso posterior
    archivo = f'./data/df_{parameter}.csv'
    df.to_csv(archivo, index=False)
    print(f"Datos de {parameter} guardados en {archivo}")


# Anomalías de temperatura promedio (tavg) de 1979 a 2024
climate_url_tavg = get_climate_url('tavg')
procesar_datos(climate_url_tavg, 'tavg')

# Precipitación (pcp) de 1979 a 2024
climate_url_pcp = get_climate_url('pcp')
procesar_datos(climate_url_pcp, 'pcp')
