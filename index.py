import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

file_path = 'prueba1.csv'  # Ruta del archivo CSV
df = pd.read_csv(file_path)
df['CODIGO ARTICULO'] = df['CODIGO ARTICULO'].fillna(method='ffill')
df['CLI'] = df['CLI'].fillna(0)
df = df.fillna(0)
df['CODIGO ARTICULO'] = df['CODIGO ARTICULO'].str.replace('ARTICULO', '', regex=False)
df = df.drop(df.index[-1])
df = df.replace({',': '.'}, regex=True)
df = df.apply(pd.to_numeric, errors='coerce')
df = df.abs()

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

# Página de Datos Procesados
elif selection == 'Control de Clientes':
    st.header("Control de Clientes")

    # Análisis de compras de los diferentes periodos
    df_cli = df.groupby('CLI').sum()
    df_cli = df_cli.drop(columns=['2020'])  # Eliminar columna de 2020
    compras_2016_2019 = df_cli[['2016', '2017', '2018', '2019']].sum(axis=1)
    compras_2021_2024 = df_cli[['2021', '2022', '2023', '2024']].sum(axis=1)
    
    # Crear DataFrame de compras por periodo
    df_compras = pd.DataFrame({
        'compras_2016_2019': compras_2016_2019,
        'compras_2021_2024': compras_2021_2024
    })
    
    # Calcular la diferencia y comparar los periodos
    df_compras['diferencia'] = df_compras['compras_2021_2024'] - df_compras['compras_2016_2019']
    df_compras['comparacion'] = df_compras['diferencia'].apply(
        lambda x: 'más en 2021-2024' if x > 0 else ('más en 2016-2019' if x < 0 else 'igual en ambos periodos')
    )
    
    # Filtrar clientes con más compras en cada periodo
    df_cli_des = df_compras[df_compras['comparacion'] == 'más en 2016-2019']
    df_cli_asc = df_compras[df_compras['comparacion'] == 'más en 2021-2024']
    
    # Mostrar resultados en Streamlit
    st.write("Análisis de compras por cliente:")
    st.write("Clientes con más compras en el periodo 2016-2019:")
    st.dataframe(df_cli_des)
    
    st.write("Clientes con más compras en el periodo 2021-2024:")
    st.dataframe(df_cli_asc)
    
    # Graficar la diferencia de compras entre los dos periodos
    plt.figure(figsize=(10, 6))
    plt.bar(df_compras.index, df_compras['diferencia'], color='lightcoral')
    plt.xlabel("Cliente")
    plt.ylabel("Diferencia en compras")
    plt.title("Diferencia de compras entre los periodos 2021-2024 y 2016-2019")
    plt.xticks(rotation=90)
    
    # Mostrar el gráfico en Streamlit
    st.pyplot(plt)

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
