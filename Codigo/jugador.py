from pymongo import MongoClient
import numpy as np
import get_datos_jugador as datos

# Conecxion a mongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["TFG"]
coleccion_jugadores = db["jugadores"]
posicion = datos.posicion

if  posicion == "DC" or posicion == "EI" or posicion == "ED":
    jugador_data = {
        "nombre": datos.nombre_jugador,
        "posicion": datos.posicion,
        "equipo": datos.equipo,
        "campo": datos.campo,
        "rival": datos.rival,
        "temporada": datos.temporada,

        "goles": datos.goles,
        "asistencias": datos.asistencias,
        "goles_esperados": datos.goles_esperados,
        "pases": datos.pases,
        "porcentaje_pases": datos.porcentaje_pases,
        "pases_clave": datos.pases_clave,
        "acciones_defensivas": datos.acciones_defensivas,
        "regates_completados": datos.regates_completados,
        "centros": datos.centros,
        "toques_balon": datos.toques_balon,
        "tiros_fuera": datos.tiros_fuera,
        "tiros_porteria": datos.tiros_porteria,
        "pases_largos": datos.pases_largos,
        "posesiones_perdidas": datos.posesiones_perdidas,
        "mapa_calor": datos.mapa_calor_lista,
    }

elif posicion == "MC" or posicion == "MCO" or posicion == "MCD" or posicion == "MD" or posicion == "MI":
    jugador_data = {
        "nombre": datos.nombre_jugador,
        "posicion": datos.posicion,
        "equipo": datos.equipo,
        "campo": datos.campo,
        "rival": datos.rival,
        "temporada": datos.temporada,

        "goles": datos.goles,
        "asistencias": datos.asistencias,
        "goles_esperados": datos.goles_esperados,
        "pases": datos.pases,
        "porcentaje_pases": datos.porcentaje_pases,
        "pases_clave": datos.pases_clave,
        "acciones_defensivas": datos.acciones_defensivas,
        "regates_completados": datos.regates_completados,
        "centros": datos.centros,
        "toques_balon": datos.toques_balon,
        "tiros_fuera": datos.tiros_fuera,
        "tiros_porteria": datos.tiros_porteria,
        "pases_largos": datos.pases_largos,
        "posesiones_perdidas": datos.posesiones_perdidas,
        "regateado": datos.regateado,
        "duelos_ganados": datos.duelos_ganados,
        "mapa_calor": datos.mapa_calor_lista,

    }

elif posicion == "DFC" or posicion == "LI" or posicion == "LD":
    jugador_data = {
        "nombre": datos.nombre_jugador,
        "posicion": datos.posicion,
        "equipo": datos.equipo,
        "campo": datos.campo,
        "rival": datos.rival,
        "temporada": datos.temporada,

        "goles": datos.goles,
        "asistencias": datos.asistencias,
        "pases": datos.pases,
        "porcentaje_pases": datos.porcentaje_pases,
        "pases_clave": datos.pases_clave,
        "acciones_defensivas": datos.acciones_defensivas,
        "toques_balon": datos.toques_balon,
        "tiros_fuera": datos.tiros_fuera,
        "tiros_porteria": datos.tiros_porteria,
        "pases_largos": datos.pases_largos,
        "posesiones_perdidas": datos.posesiones_perdidas,
        "faltas": datos.faltas,
        "regateado": datos.regateado,
        "tiros bloqueados": datos.tiros_bloqueados,
        "despejes": datos.despejes,
        "duelos_ganados": datos.duelos_ganados,
        "duelos_aereos_ganados": datos.duelos_aereos_ganados,
        "entradas": datos.entradas,
        "mapa_calor": datos.mapa_calor_lista,

    }

else:
    jugador_data = {
        "nombre": datos.nombre_jugador,
        "posicion": datos.posicion,
        "equipo": datos.equipo,
        "campo": datos.campo,
        "rival": datos.rival,
        "temporada": datos.temporada,

        "paradas": datos.paradas,
        "goles_evitados": datos.goles_evitados,
        "despejes": datos.despejes,
        #"salidas": datos.salidas,
        "mapa_calor": datos.mapa_calor_lista,

    }

# Insertar el diccionario en la colección
coleccion_jugadores.insert_one(jugador_data)

print("Datos insertados en MongoDB")