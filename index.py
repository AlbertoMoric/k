import streamlit as st
import pandas as pd

# Título
st.title("Kentu Ventas 2025")

# Descripción
st.write("""
Este informe presenta las predicciones de ventas de la empresa Kentu para el año 2025. 
A través de análisis y proyecciones, se anticipa el desempeño y las tendencias del mercado que impactarán en los resultados de la compañía.
""")

# Cargar el archivo CSV automáticamente
file_path = 'prueba1.csv'  # Ruta del archivo CSV

# Asegúrate de que el archivo esté en la misma carpeta que el script de Streamlit
df = pd.read_csv(file_path)

# Procesamiento de datos
df['CODIGO ARTICULO'] = df['CODIGO ARTICULO'].fillna(method='ffill')
df['CLI'] = df['CLI'].fillna(0)
df = df.fillna(0)
df['CODIGO ARTICULO'] = df['CODIGO ARTICULO'].str.replace('ARTICULO', '', regex=False)
df = df.drop(df.index[-1])
df = df.replace({',': '.'}, regex=True)
df = df.apply(pd.to_numeric, errors='coerce')
df = df.abs()

# Crear el DataFrame ven_tot con la suma de ventas de 2015 a 2024
ven_tot = df.loc[:, '2015':'2024'].sum()
ven_tot = {'CODIGO ARTICULO': 0, 'CLI': 0, **ven_tot.to_dict()}
ven_tot = pd.DataFrame([ven_tot])

# Mostrar solo las columnas de 2015 a 2024 en ven_tot
st.write("Suma total de ventas de 2015 a 2024:")
st.dataframe(ven_tot.loc[:, '2015':'2024'])
