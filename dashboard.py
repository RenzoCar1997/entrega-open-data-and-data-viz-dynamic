# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 23:24:47 2024

@author: Renzo
"""
import pandas as pd
import streamlit as st
import locale
import plotly.graph_objects as go
import statsmodels.api as sm 

# Configurar localización a español
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')  

                 
# Configuración del dashboard
st.set_page_config(page_title='Series de Tiempo Globales para Anomalías de Temperatura y Precipitación', layout='wide')

# Estilo personalizado
st.markdown("""
<style>
    .main {
        background-color: #f4f4f4;
        color: #333333;
    }
    .sidebar .sidebar-content {
        background-color: #e8e8e8;
        color: #333333;
    }
    .right-title {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Título del dashboard
st.markdown('<h1 class="right-title">Series de Tiempo Globales</h1>', unsafe_allow_html=True)

# Leyendo DataFrames
df_tavg = pd.read_csv('./data/df_tavg.csv', parse_dates=['fecha'])
df_pcp = pd.read_csv('./data/df_pcp.csv', parse_dates=['fecha'])

# Añadir una barra lateral con descripciones
st.sidebar.title("Descripción")
st.sidebar.write("Este dashboard muestra anomalías en temperatura y precipitación globales a lo largo del tiempo.")
st.sidebar.write("Puedes utilizar los siguientes filtros de fecha para explorar cómo han variado las condiciones climáticas a lo largo del tiempo:")

# Filtros interactivos con configuración de fechas mínimas y máximas
start_date = st.sidebar.date_input("Fecha de inicio", value=df_tavg['fecha'].min(), min_value=df_tavg['fecha'].min(), max_value=df_tavg['fecha'].max())
end_date = st.sidebar.date_input("Fecha de fin", value=df_tavg['fecha'].max(), min_value=df_tavg['fecha'].min(), max_value=df_tavg['fecha'].max())

# Filtrar datos
df_tavg_filtered = df_tavg[(df_tavg['fecha'] >= pd.to_datetime(start_date)) & (df_tavg['fecha'] <= pd.to_datetime(end_date))]
df_pcp_filtered = df_pcp[(df_pcp['fecha'] >= pd.to_datetime(start_date)) & (df_pcp['fecha'] <= pd.to_datetime(end_date))]

# Organizar visualizaciones en pestañas
tab1, tab2 = st.tabs(["Temperatura", "Precipitación"])

with tab1:
    # Aplicando el filtro Hodrick-Prescott para separar en tendencia y  componente ciclico.
    df_tavg_filtered_ciclo, df_tavg_filtered_tend = sm.tsa.filters.hpfilter(df_tavg_filtered['anomalía'])
    df_tavg_filtered['tend'] = df_tavg_filtered_tend
    
    # Crear una figura 
    fig1 = go.Figure() 
    
    # Agregar un gráfico de barras de la anomalía
    fig1.add_trace(go.Bar(x = df_tavg_filtered['fecha'], y = df_tavg_filtered['anomalía'], marker_color = "#B2182A", name = 'Anomalía')) 
    
    # Agregar un gráfico de líneas de la tendencia
    fig1.add_trace(go.Scatter(x = df_tavg_filtered['fecha'], y = df_tavg_filtered['tend'], mode = 'lines', line = dict(color = '#E55137'), name = 'Tendencia'))
    
    # Personalizar el gráfico para anomalía de temperatura promedio
    fig1.update_layout(
        title="Anomalía de temperatura promedio",
        xaxis_title="Fecha",
        yaxis_title="Anomalía de Temperatura Promedio (°C)",
        template="plotly_white",
        width=900,
        height=420
    )
    
    # Mostrar gráfico de lineas para anomalía de temperatura promedio
    st.plotly_chart(fig1)
    
    # Ordenar DataFrame filtrado por anomalía de temperatura promedio
    df_tavg_filtered_sorted = df_tavg_filtered.sort_values('anomalía', ascending=False)

    # Mejorando el formato 
    df_tavg_filtered_sorted['fecha'] = df_tavg_filtered_sorted['fecha'].apply(lambda x: x.strftime('%B %Y'))

    # Añadiendo columna Ranking
    df_tavg_filtered_sorted['Ranking'] = range(1, len(df_tavg_filtered_sorted)+1)

    # Seleccionar y renombrar columnas para mostrar
    df_tavg_filtered_sorted = df_tavg_filtered_sorted[['Ranking', 'fecha','anomalía']].reset_index(drop=True).rename(columns={'fecha':"Mes y año",'anomalía':"Anomalía de temperatura promedio (°C)"})

    # Mostrar 10 meses con mayor anomalía de temperatura promedio
    st.write(f"Top 10 Meses con mayor anomalía de temperatura promedio desde {start_date.strftime('%B %Y')} a {end_date.strftime('%B %Y')}")
    st.dataframe(df_tavg_filtered_sorted.head(10))

with tab2:
    # Aplicando el filtro Hodrick-Prescott para separar en tendencia y  componente ciclico.
    df_pcp_filtered_ciclo, df_pcp_filtered_tend = sm.tsa.filters.hpfilter(df_pcp_filtered['anomalía'])
    df_pcp_filtered['tend'] = df_pcp_filtered_tend
    
    # Crear una figura 
    fig2 = go.Figure() 
    
    # Agregar un gráfico de barras de la anomalía
    fig2.add_trace(go.Scatter(x = df_pcp_filtered['fecha'], y = df_pcp_filtered['anomalía'], mode = 'lines', line = dict(color = "#1F77B4"), name = 'Anomalía')) 
    
    # Agregar un gráfico de líneas de la tendencia
    fig2.add_trace(go.Scatter(x = df_pcp_filtered['fecha'], y = df_pcp_filtered['tend'], mode = 'lines', line = dict(color = '#E55137'), name = 'Tendencia'))
    
    # Personalizar el gráfico para anomalía de precipitación
    fig2.update_layout(
        title='Anomalía de precipitación',
        xaxis_title="Fecha",
        yaxis_title="Anomalía de precipitación (mm)",
        template="plotly_white",
        width=900,
        height=420
    )

    # Mostrar gráfico de lineas para anomalía de precipitación
    st.plotly_chart(fig2)

    # Ordenar DataFrame filtrado por anomalía de precipitación
    df_pcp_filtered_sorted = df_pcp_filtered.sort_values('anomalía', ascending=False)

    # Mejorando el formato 
    df_pcp_filtered_sorted['fecha'] = df_pcp_filtered_sorted['fecha'].apply(lambda x: x.strftime('%B %Y'))

    # Añadiendo columna Ranking
    df_pcp_filtered_sorted['Ranking'] = range(1, len(df_tavg_filtered_sorted)+1)

    # Seleccionar y renombrar columnas para mostrar
    df_pcp_filtered_sorted = df_pcp_filtered_sorted[['Ranking', 'fecha','anomalía']].reset_index(drop=True).rename(columns={'fecha':"Mes y año",'anomalía':"Anomalía de precipitación (mm)"})

    # Mostrar 10 meses con mayor anomalía de precipitación
    st.write(f"Top 10 Meses con mayor anomalía de precipitación desde {start_date.strftime('%B %Y')} a {end_date.strftime('%B %Y')}")
    st.dataframe(df_pcp_filtered_sorted.head(10))
