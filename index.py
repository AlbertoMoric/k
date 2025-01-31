import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título
st.title("Kentu Ventas 2025")

# Descripción
st.write("""
Este informe presenta las predicciones de ventas de la empresa Kentu para el año 2025. 
A través de análisis y proyecciones, se anticipa el desempeño y las tendencias del mercado que impactarán en los resultados de la compañía.
""")

# Crear índice
menu = ['Primeras Conlusiones', 'Control de Clientes', 'Control de Articulos', 'Resumen']
selection = st.sidebar.radio("Indice de Contenidos:", menu)

# Página de Introducción
if selection == 'Primeras Conlusiones':
    st.header("Ventas Totales por Año")
    st.write("""
   
En el apartado "Primeras Conclusiones", he analizado las ventas totales de los años anteriores para evaluar el progreso de la empresa a lo largo del tiempo. A partir de esta información, he identificado tendencias y patrones que permiten realizar una primera estimación de las ventas para el año 2025. Este enfoque busca prever el comportamiento futuro basándose en el rendimiento histórico.
    """)

# Página de Datos Procesados
elif selection == 'Datos Procesados':
    st.header("Datos Procesados")
    
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

    # Mostrar datos procesados
    st.write("Datos procesados:")
    st.dataframe(df)

# Página de Gráfico de Ventas
elif selection == 'Gráfico de Ventas':
    st.header("Gráfico de Ventas Totales de 2015 a 2024")

    # Crear el DataFrame ven_tot con la suma de ventas de 2015 a 2024
    ven_tot = df.loc[:, '2015':'2024'].sum()
    ven_tot = {'CODIGO ARTICULO': 0, 'CLI': 0, **ven_tot.to_dict()}
    ven_tot = pd.DataFrame([ven_tot])

    # Redondear los valores de ven_tot a 2 decimales
    ven_tot = ven_tot.round(2)

    # Graficar las ventas de 2015 a 2024
    plt.figure(figsize=(10, 6))
    plt.bar(ven_tot.columns[2:], ven_tot.iloc[0, 2:], color='skyblue')
    plt.xlabel("Año")
    plt.ylabel("Ventas Totales")
    plt.title("Ventas Totales de 2015 a 2024")
    plt.xticks(rotation=45)

    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)

# Página de Resumen
elif selection == 'Resumen':
    st.header("Resumen")
    st.write("""
    En resumen, el informe presenta las proyecciones de ventas de Kentu para el año 2025 y una visión general de las tendencias del mercado. 
    Se observa un crecimiento constante en las ventas de los últimos años, con algunas fluctuaciones que deben ser monitoreadas para una mejor toma de decisiones estratégicas.
    """)
