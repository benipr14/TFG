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

# Conecion a mongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["TFG"]
coleccion_jugadores = db["jugadores"]

# Buscar un jugador por nombre
jugador = coleccion_jugadores.find_one({"nombre": "Raphinha"})

# Verificar si se encontró el jugador
if jugador:

    mapa_calor_lista = jugador["mapa_calor"]
    mapa_calor_df = pd.DataFrame(mapa_calor_lista)

    colors = [(0, "white"), (0.5, "orange"), (1, "red")]
    custom_cmap = LinearSegmentedColormap.from_list("custom_cmap", colors)

    fig, ax = plt.subplots(figsize=(16, 9))

    pitch = Pitch(pitch_type='opta')
    pitch.draw(ax=ax)
    pitch.kdeplot(mapa_calor_df.x, mapa_calor_df.y, ax=ax,
                fill = True,
                levels=100,
                thresh=0.08,
                zorder=-1,
                bw_adjust=0.13,
                cmap="OrRd")

    plt.show() 

else:
    print("Jugador no encontrado.")
