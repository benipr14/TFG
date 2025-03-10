from pymongo import MongoClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch
import warnings
from matplotlib.colors import LinearSegmentedColormap
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler

# Ocultar los warnings
warnings.filterwarnings("ignore")

# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["TFG"]
coleccion_jugadores = db["jugadores"]
coleccion_equipos = db["equipos"]

def obtener_rival_campo(posicion):
    if posicion == "LD":
        return "EI"
    elif posicion == "DFC":
        return "DC"
    elif posicion == "LI":
        return "ED"
    elif posicion == "MCD" or posicion == "MC" or posicion == "MCO" or posicion == "MI" or posicion == "MD":
        return ["MC", "MCD", "MCO", "MI", "MD", "DFC", "LD"]
    elif posicion == "ED":
        return "LI"
    elif posicion == "EI":
        return ["LD", "DFC", "MCD", "MC"]
    elif posicion == "DC":
        return "DFC"
    

def desempatar_con_knn(jugador1, jugador2, p, k=2):
    jugadores_coincidentes = coleccion_jugadores.find({
        "mapa_calor": {
            "$elemMatch": {
                "x": {"$gte": 100 - (p["x"] + 5), "$lte": 100 - (p["x"] - 5)},
                "y": {"$gte": 100 - (p["y"] + 5), "$lte": 100 - (p["y"] - 5)}
            }
        }
    })
    #print(p["x"], p["y"])
    jugador1_2 = coleccion_jugadores.find_one({"nombre": jugador1})

    posiciones1 = []
    posiciones2 = []
    for j in jugadores_coincidentes:
        if (j["posicion"] == jugador1_2["posicion"]):
            posiciones1.append(j)
        elif j["posicion"] == jugador2["posicion"]:
            posiciones2.append(j)

    if len(posiciones1) < 2 or len(posiciones2) < 2:
        print("No hay suficientes")
        return True
    
    d1 = pd.DataFrame(posiciones1)
    d2 = pd.DataFrame(posiciones2)
    
    #Entrenar modelo KNN con jugadores de la misma posicion
    if jugador1_2["posicion"] == "DC" or jugador1_2["posicion"] == "EI" or jugador1_2["posicion"] == "ED":
        datos1 = ["goles", "asistencias", "goles_esperados", "pases_clave", "regates_completados", "tiros_porteria", "pases"]
    elif jugador1_2["posicion"] == "MC" or jugador1_2["posicion"] == "MCO" or jugador1_2["posicion"] == "MCD" or jugador1_2["posicion"] == "MD" or jugador1_2["posicion"] == "MI":
        datos1 = ["pases", "asistencias", "goles_esperados", "pases_clave", "regates_completados", "pases_largos", "duelos_ganados"]
    else:
        datos1 = ["acciones_defensivas", "regateado", "pases_clave", "regateado", "despejes", "duelos_ganados", "duelos_aereos_ganados"]

    knn = KNeighborsRegressor(n_neighbors=k)
    scaler = StandardScaler()
    X = d1[datos1]
    y = d1["rendimiento"]
    scaler.fit(X)
    X = scaler.transform(X)
    knn.fit(X, y)
    # Predecir el valor de la posición del jugador 1
    x = [[jugador1_2[datos1[0]], jugador1_2[datos1[1]], jugador1_2[datos1[2]], jugador1_2[datos1[3]], jugador1_2[datos1[4]], jugador1_2[datos1[5]], jugador1_2[datos1[6]]]]
    x = scaler.transform(x)
    value1 = knn.predict(x)

    #Entrenar modelo KNN con jugadores de la misma posicion
    if jugador2["posicion"] == "DC" or jugador2["posicion"] == "EI" or jugador2["posicion"] == "ED":
        datos2 = ["goles", "asistencias", "goles_esperados", "pases_clave", "regates_completados", "tiros_porteria", "pases"]
    elif jugador2["posicion"] == "MC" or jugador2["posicion"] == "MCO" or jugador2["posicion"] == "MCD" or jugador2["posicion"] == "MD" or jugador2["posicion"] == "MI":
        datos2 = ["pases", "asistencias", "goles_esperados", "pases_clave", "regates_completados", "pases_largos", "duelos_ganados"]
    else:
        datos2 = ["acciones_defensivas", "regateado", "pases_clave", "regateado", "despejes", "duelos_ganados", "duelos_aereos_ganados"]

    knn2 = KNeighborsRegressor(n_neighbors=k)
    scaler2 = StandardScaler()
    X2 = d2[datos2]
    y2 = d2["rendimiento"]
    scaler2.fit(X2)
    X2 = scaler2.transform(X2)
    knn2.fit(X2, y2)
    # Predecir el valor de la posición del jugador 1
    x2 = [[jugador2[datos2[0]], jugador2[datos2[1]], jugador2[datos2[2]], jugador2[datos2[3]], jugador2[datos2[4]], jugador2[datos2[5]], jugador2[datos2[6]]]]
    x2 = scaler2.transform(x2)
    value2 = knn2.predict(x2)
    
    # Comparar los valores
    if value1 > value2:
        print("Si")
        return True
    elif value2 > value1:
        print("Has perdido")
        return False
    else:
        random = np.random.randint(0, 2)
        return random == 1
     
# Buscar equipos por nombre
equipo1 = coleccion_equipos.find_one({"equipo": "Barcelona"})
equipo2 = coleccion_equipos.find_one({"equipo": "Getafe"})
jugadores1 = equipo1["jugadores"]
jugadores2 = equipo2["jugadores"]

# Procesar jugadores del primer equipo
dataframes1 = []
mapa_calor_lista = []
mapa_calor_lista_2 = []
mapa_final = []
pos_a_buscar = ""
for j in jugadores1:
    jugador = coleccion_jugadores.find({"nombre": j})
    for k in jugador:
        mapa_calor_lista.extend(k["mapa_calor"])
        for t in mapa_calor_lista:
            t["borrar"] = False
        mapa_calor_lista = [dict(t) for t in {tuple(d.items()) for d in mapa_calor_lista}]

        pos_a_buscar = obtener_rival_campo(k["posicion"])
    
    # Procesar jugadores del segundo equipo
    for i in jugadores2:
        jugador = coleccion_jugadores.find({"nombre": i, "posicion": {"$in": pos_a_buscar}})
        for k in jugador:
            mapa_calor_lista_2.extend(k["mapa_calor"])
        mapa_calor_lista_2 = [dict(t) for t in {tuple(d.items()) for d in mapa_calor_lista_2}]
        for t in mapa_calor_lista_2:
            t["x"] = 100 - t["x"]
            t["y"] = 100 - t["y"]

        for p in mapa_calor_lista:
            for s in mapa_calor_lista_2:
                if (p["x"] == s["x"] or p["x"] == (s["x"]+1) or p["x"] == (s["x"]+2) or p["x"] == (s["x"]+3) or p["x"] == (s["x"]+4) or p["x"] == (s["x"]+5)
                    or p["x"] == (s["x"]-1) or p["x"] == (s["x"]-2) or p["x"] == (s["x"]-3) or p["x"] == (s["x"]-4) or p["x"] == (s["x"]-5)) and \
                    (p["y"] == s["y"] or p["y"] == (s["y"]+1) or p["y"] == (s["y"]+2)or p["y"] == (s["y"]+3) or p["y"] == (s["y"]+4) or p["y"] == (s["y"]+5)
                    or p["y"] == (s["y"]-1) or p["y"] == (s["y"]-2) or p["y"] == (s["y"]-3) or p["y"] == (s["y"]-4) or p["y"] == (s["y"]-5)):
                        resultado = desempatar_con_knn(j, k, p)
                        if not resultado:
                            p["borrar"] = True

        mapa_calor_lista_2 = []

    mapa_final += mapa_calor_lista
    mapa_calor_lista = []
    

print(len(mapa_final))
# Eliminar las superposiciones
mapa_final = [p for p in mapa_final if not p.get("borrar", False)]
print(len(mapa_final))
mapa_calor_df = pd.DataFrame(mapa_final)
# Eliminar filas duplicadas
mapa_calor_df.drop_duplicates(inplace=True)

# Visualizar el mapa de calor combinado
colors = [(0, "white"), (0.5, "orange"), (1, "red")]
custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

fig, ax = plt.subplots(figsize=(16, 9))

pitch = Pitch(pitch_type='opta')
pitch.draw(ax=ax)
pitch.kdeplot(mapa_calor_df.x, mapa_calor_df.y, ax=ax,
            fill=True,
            levels=100,
            thresh=0.08,
            zorder=-1,
            bw_adjust=0.1,
            cmap="OrRd")

plt.show()