from pymongo import MongoClient
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mplsoccer import Pitch
import warnings
from matplotlib.colors import LinearSegmentedColormap

# Ocultar los warnings
warnings.filterwarnings("ignore")

# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["TFG"]
coleccion_jugadores = db["jugadores"]
coleccion_equipos = db["equipos"]

# Buscar equipos por nombre
equipo1 = coleccion_equipos.find_one({"equipo": "Barcelona"})
equipo2 = coleccion_equipos.find_one({"equipo": "Getafe"})
jugadores1 = equipo1["jugadores"]
jugadores2 = equipo2["jugadores"]

# Procesar jugadores del primer equipo
dataframes1 = []
mapa_calor_lista = []
mapa_calor_aux = []
for j in jugadores1:
    jugador = coleccion_jugadores.find({"nombre": j})
    for k in jugador:
        mapa_calor_lista.extend(k["mapa_calor"])
        for t in mapa_calor_lista:
            t["borrar"] = False
    
   # mapa_calor_lista = mapa_calor_aux
    # Procesar jugadores del segundo equipo
    for i in jugadores2:
        jugador = coleccion_jugadores.find({"nombre": i})
        for k in jugador:
            mapa_calor_lista_2 = k["mapa_calor"]
            mapa_calor_df = pd.DataFrame(mapa_calor_lista_2)
            for t in mapa_calor_lista_2:
                t["x"] = 100 - t["x"]
                t["y"] = 100 - t["y"]
            if k["posicion"] == "LD":
                 mapa_calor_df['x'] = 100 - mapa_calor_df['x']
                 mapa_calor_df['y'] = 100 - mapa_calor_df['y']
            for p in mapa_calor_lista:
                continua = True
                for s in mapa_calor_lista_2:
                    if (p["x"] == s["x"] or p["x"] == (s["x"]+1) or p["x"] == (s["x"]+2) or p["x"] == (s["x"]+3) or p["x"] == (s["x"]+4) or p["x"] == (s["x"]+5)
                        or p["x"] == (s["x"]-1) or p["x"] == (s["x"]-2) or p["x"] == (s["x"]-3) or p["x"] == (s["x"]-4) or p["x"] == (s["x"]-5)) and \
                        (p["y"] == s["y"] or p["y"] == (s["y"]+1) or p["y"] == (s["y"]+2)or p["y"] == (s["y"]+3) or p["y"] == (s["y"]+4) or p["y"] == (s["y"]+5)
                        or p["y"] == (s["y"]-1) or p["y"] == (s["y"]-2) or p["y"] == (s["y"]-3) or p["y"] == (s["y"]-4) or p["y"] == (s["y"]-5)):
                            if (k["nombre"] == "Juan Iglesias" or k["nombre"] == "Domingos Duarte"):
                               p["borrar"] = True
                               break
print(len(mapa_calor_lista))
# Eliminar las superposiciones
mapa_calor_lista = [p for p in mapa_calor_lista if not p.get("borrar", False)]
print(len(mapa_calor_lista))

mapa_calor_df = pd.DataFrame(mapa_calor_lista)
dataframes1.append(mapa_calor_df)

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