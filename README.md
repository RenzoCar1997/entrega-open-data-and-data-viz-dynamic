# Proyecto de Scraping de Datos Climáticos

Este proyecto contiene scripts para extraer y analizar datos climáticos de la NOAA, así como visualizar las anomalías de temperatura y precipitación a lo largo del tiempo utilizando Plotly y Streamlit.

## Requisitos

Asegúrate de tener instaladas las siguientes herramientas antes de comenzar:

- Python 3.x
- Pip

## Instalación

1. Clona este repositorio:

```bash
git clone https://github.com/tu-usuario/tu-proyecto.git
cd tu-proyecto
```

2. Crea y activa un entorno virtual (opcional pero recomendado):

```bash
python -m venv env
source env/bin/activate  # En Windows usa `env\Scripts\activate`
```

3. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución del Script Principal

Para ejecutar el script principal run_scraper.py y obtener los datos climáticos, utiliza el siguiente comando:

```bash
python run_scraper.py
```

Este comando realizará el scraping de los datos climáticos y guardará los resultados en archivos CSV en la carpeta ./data

## Visualización de Datos

Para visualizar los datos utilizando el dashboard de Streamlit, ejecuta el siguiente comando:

```bash
streamlit run dashboard.py
```

Esto abrirá una interfaz web interactiva donde podrás explorar las anomalías de temperatura y precipitación a lo largo del tiempo.

Es posible visualizar el dashboard a través de Streamlit Cloud en: 

## Estructura del Proyecto

```arduino
.
├── data
│   ├── df_tavg.csv
│   ├── df_pcp.csv
├── scraper_clima.py
├── run_scraper.py
├── dashboard.py
├── requirements.txt
├── README.md
```

- data/: Carpeta que contiene los archivos CSV generados.

- scraper_clima.py: Script que contiene las funciones para hacer scraping de los datos climáticos.

- run_scraper.py: Script principal para ejecutar el scraping y guardar los datos.

- dashboard.py: Script para visualizar los datos utilizando Streamlit.

- requirements.txt: Archivo que contiene las dependencias necesarias para el proyecto.

- README.md: Archivo con las instrucciones del proyecto.


## Licencia

Este proyecto está bajo la Licencia MIT - mira el archivo LICENSE para más detalles.
