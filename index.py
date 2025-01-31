import streamlit as st
import pandas as pd


# Título
st.title("Kentu Ventas 2025")

# Descripción
st.write("""
Este informe presenta las predicciones de ventas de la empresa Kentu para el año 2025. 
A través de análisis y proyecciones, se anticipa el desempeño y las tendencias del mercado que impactarán en los resultados de la compañía.
""")

# Subir archivo CSV
st.sidebar.header("Subir archivo CSV")
uploaded_file = st.sidebar.file_uploader("Elige un archivo CSV", type=["csv"])

if uploaded_file is not None:
    # Cargar y procesar el archivo CSV
    df = pd.read_csv(uploaded_file)

    # Procesamiento de datos
    df['CODIGO ARTICULO'] = df['CODIGO ARTICULO'].fillna(method='ffill')
    df['CLI'] = df['CLI'].fillna(0)
    df = df.fillna(0)
    df['CODIGO ARTICULO'] = df['CODIGO ARTICULO'].str.replace('ARTICULO', '', regex=False)
    df = df.drop(df.index[-1])
    df = df.replace({',': '.'}, regex=True)
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.abs()

    # Mostrar datos procesados
    st.write("Datos procesados:")
    st.dataframe(df)
else:
    st.write("Por favor, sube un archivo CSV para procesar los datos.")
