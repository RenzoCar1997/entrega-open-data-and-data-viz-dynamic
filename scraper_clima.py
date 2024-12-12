# -*- coding: utf-8 -*-
"""
Created on Wed Nov 13 19:52:45 2024

@author: Renzo
"""
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from io import StringIO


def get_climate_url(parameter='tavg', first_year=1979, last_year=2024):
    """
    Genera una URL para acceder a datos climáticos del sitio web de la NOAA.

    Parámetros:
    parameter (str): Tipo de parámetro climático a consultar. 
                     'tavg' para anomalía de temperatura promedio.
                     'pcp' para anomalía de precipitación.
    first_year (int): Primer año del rango de datos (por defecto, 1979).
    last_year (int): Último año del rango de datos (por defecto, 2024).

    Retorna:
    str: URL para acceder a los datos climáticos en el formato especificado.
    """
    return r'https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/global/time-series/globe/{parameter}/land_ocean/1/0/{first_year}-{last_year}'.format(parameter=parameter, first_year=first_year, last_year=last_year)
             


def scrape_climate_data(climate_url):
    """
    Scraper de datos climáticos desde una URL específica.

    Esta función utiliza Selenium para abrir una URL de datos climáticos,
    espera a que la página cargue completamente, extrae el contenido HTML
    y utiliza BeautifulSoup para encontrar y leer una tabla HTML específica
    en un DataFrame de pandas.

    Parámetros:
    climate_url (str): La URL desde donde se obtendrán los datos climáticos.
    wait_time (int): Tiempo de espera para que la página cargue completamente (en segundos).

    Retorna:
    DataFrame: Un DataFrame de pandas que contiene los datos de la tabla HTML.
               Devuelve un DataFrame vacío si no se encuentra la tabla.
    """
    try:
        # Iniciar el navegador
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)


        driver.get(climate_url)

        # Esperar unos segundos para que la página cargue completamente
        driver.implicitly_wait(10)  # Esperar hasta wait_time segundos

        # Obtener el HTML de la página
        html_content = driver.page_source

        # Parsear el HTML con BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        table = soup.find('table', {'id': 'values-table'})

        if table:
            # Leer la tabla HTML en un DataFrame
            df = pd.read_html(StringIO(str(table)))[0]
            return df
        else:
            print("No se encontró la tabla con el id 'values-table'.")
            return pd.DataFrame()  # Devolver un DataFrame vacío si no se encuentra la tabla

    except Exception as e:
        print(f"Ocurrió un error: {e}")
        return pd.DataFrame()

    finally:
        # Cerrar el navegador
        driver.quit()
    