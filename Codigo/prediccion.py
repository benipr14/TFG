from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch
from matplotlib.colors import LinearSegmentedColormap

# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["TFG"]
coleccion_jugadores = db["jugadores"]

# Obtener los datos de los jugadores
jugadores = list(coleccion_jugadores.find())
df = pd.DataFrame(jugadores)

# Seleccionar las columnas relevantes
features = ['goles', 'asistencias', 'pases']
target = 'mapa_calor'

# Convertir lista_xy en dos listas separadas de x e y
df["lista_x"] = df["lista_xy"].apply(lambda lista: [p[0] for p in lista])
df["lista_y"] = df["lista_xy"].apply(lambda lista: [p[1] for p in lista])

# Eliminar lista original
df.drop(columns=["lista_xy"], inplace=True)

max_len = max(df["lista_xy"].apply(len))  # Encuentra la lista más larga

df["lista_x"] = df["lista_xy"].apply(lambda lista: [p[0] for p in lista] + [0] * (max_len - len(lista)))
df["lista_y"] = df["lista_xy"].apply(lambda lista: [p[1] for p in lista] + [0] * (max_len - len(lista)))

for i in range(max_len):
    df[f"x_{i}"] = df["lista_x"].apply(lambda lista: lista[i])
    df[f"y_{i}"] = df["lista_y"].apply(lambda lista: lista[i])

df.drop(columns=["lista_x", "lista_y"], inplace=True)


# Actualizar las características y el objetivo
X = df[features]
y = df[mapa_calor_df.columns]

print("Datos de entrada (X):")
print(X.describe())

print("Datos de salida (y):")
print(y.describe())

# Verificar el número de muestras
if len(df) > 1:
    # Dividir los datos en conjuntos de entrenamiento y prueba
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
else:
    # Usar todos los datos para entrenamiento si hay solo una muestra
    X_train, y_train = X, y

# Crear y entrenar el modelo
model = LinearRegression()
model.fit(X_train, y_train)

# Predecir el mapa de calor para un nuevo conjunto de estadísticas
nuevas_estadisticas = [[0, 0, 1]]  # Ejemplo de estadísticas
prediccion_mapa_calor = model.predict(nuevas_estadisticas)

# Verificar la predicción
print("Predicción del mapa de calor:", prediccion_mapa_calor)

# Convertir la predicción en un DataFrame
mapa_calor_df = pd.DataFrame(prediccion_mapa_calor, columns=mapa_calor_df.columns)

# Imprimir los nombres de las columnas para verificar
print("Columnas del DataFrame de predicción:", mapa_calor_df.columns)
print("Valores del DataFrame de predicción:", mapa_calor_df)

# Mostrar el mapa de calor
fig, ax = plt.subplots(figsize=(16, 9))

pitch = Pitch(pitch_type='opta')
pitch.draw(ax=ax)
pitch.kdeplot(mapa_calor_df.iloc[:, 0], mapa_calor_df.iloc[:, 1], ax=ax,
              fill=True,
              levels=100,
              thresh=0.08,
              zorder=-1,
              bw_adjust=0.2,
              cmap="OrRd")

plt.show()