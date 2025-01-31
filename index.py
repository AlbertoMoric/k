import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
import time

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
st.write("""
______________________________________________________________________________________________________________________________________________
""")
# Crear índice
menu = ['Primeras Conlusiones', 'Control de Clientes', 'Control de Articulos', 'Predicciones 2025']
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

    articulos_por_cliente = {}
    for cli in df['CLI'].unique():
        articulos_cliente = df[df['CLI'] == cli].iloc[:, 1:]  # Tomamos todas las columnas de años (2015-2024)
        articulos_comprados = df.loc[df['CLI'] == cli].iloc[:, 1:].gt(0).any(axis=1).index[df.loc[df['CLI'] == cli].iloc[:, 1:].gt(0).any(axis=1)].tolist()
        articulos_por_cliente[cli] = articulos_comprados

    df_articulos_cliente = pd.DataFrame(list(articulos_por_cliente.items()), columns=['CLI', 'Articulos_Comprados'])

    # Mostrar los artículos comprados por cada cliente
    st.write("Artículos comprados por cada cliente:")
    st.dataframe(df_articulos_cliente)

# Página de Gráfico de Ventas
elif selection == 'Control de Articulos':
    # Análisis de compras por artículo
    df_art = df.groupby('CODIGO ARTICULO').sum()
    df_art = df_art.drop(columns=['2020'])  # Eliminar columna de 2020
    compras_2016_2019 = df_art[['2016', '2017', '2018', '2019']].sum(axis=1)
    compras_2021_2024 = df_art[['2021', '2022', '2023', '2024']].sum(axis=1)
    
    # Crear DataFrame de compras por artículo
    df_compras_articulo = pd.DataFrame({
        'compras_2016_2019': compras_2016_2019,
        'compras_2021_2024': compras_2021_2024
    })
    
    # Calcular la diferencia y comparar los periodos
    df_compras_articulo['diferencia'] = df_compras_articulo['compras_2021_2024'] - df_compras_articulo['compras_2016_2019']
    df_compras_articulo['comparacion'] = df_compras_articulo['diferencia'].apply(
        lambda x: 'más en 2021-2024' if x > 0 else ('más en 2016-2019' if x < 0 else 'igual en ambos periodos')
    )
    
    # Filtrar artículos con más compras en cada periodo
    df_art_des = df_compras_articulo[df_compras_articulo['comparacion'] == 'más en 2016-2019']
    df_art_asc = df_compras_articulo[df_compras_articulo['comparacion'] == 'más en 2021-2024']
    
    # Mostrar resultados en Streamlit
    st.write("Artículos con más compras en el periodo 2016-2019:")
    st.dataframe(df_art_des)
    
    st.write("Artículos con más compras en el periodo 2021-2024:")
    st.dataframe(df_art_asc)

# Página de Resumen
elif selection == 'Predicciones 2025':

    X = df[['2015', '2016', '2017', '2018', '2019', '2021', '2022', '2023', '2024']].values
    X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Mostrar el DataFrame original en Streamlit
    st.subheader("Datos originales")
    st.dataframe(df)
        
    with st.spinner('Entrenando el modelo...'):
        time.sleep(2)  # Simula un pequeño retraso al inicio
    
        # Crear el modelo de red neuronal
        model = Sequential()
        model.add(Dense(64, input_dim=X_train_scaled.shape[1], activation='relu'))  # 64 neuronas en la capa oculta
        model.add(Dense(32, activation='relu'))  # 32 neuronas
        model.add(Dense(1))  # Capa de salida con una neurona (predicción)
    
        # Compilación y entrenamiento del modelo
        model.compile(optimizer='adam', loss='mean_squared_error')
    
        # Definir EarlyStopping para detener el entrenamiento cuando no haya mejora
        early_stopping = EarlyStopping(monitor='val_loss',    # Se monitorea el loss de validación
                                        patience=5,          # Número de épocas sin mejora
                                        restore_best_weights=True)  # Restaura los mejores pesos cuando se detiene
    
        # Entrenamiento del modelo
        history = model.fit(X_train_scaled, 
                            X_train[:, -1],  # Usamos la última columna como target (ventas 2024)
                            epochs=200, 
                            batch_size=10, 
                            validation_data=(X_test_scaled, X_test[:, -1]), 
                            callbacks=[early_stopping])  # Añadir el callback de EarlyStopping
    
    # Mostrar un mensaje de éxito después de entrenar el modelo
    st.success('Modelo entrenado exitosamente')
    
    # Evaluación del modelo
    loss = model.evaluate(X_test_scaled, X_test[:, -1])
    st.write(f'Pérdida en el conjunto de prueba: {loss}')
    
    # Predicción de ventas para 2025
    df['prediccion_2025'] = model.predict(scaler.transform(df[['2015', '2016', '2017', '2018', '2019', '2021', '2022', '2023', '2024']].values))
    
    # Mostrar predicción en Streamlit
    st.write("Predicción de ventas para el año 2025:")
    st.dataframe(df[['CODIGO ARTICULO','CLI','2021','2022','2023','2024', 'prediccion_2025']])
