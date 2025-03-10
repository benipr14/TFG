from pymongo import MongoClient

# Conecxion a mongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["TFG"]
coleccion_jugadores = db["jugadores"]

# Borrar la variable 'rendimiento' de todos los jugadores
coleccion_jugadores.update_many({}, {"$unset": {"rendimiento": ""}})
# Buscar todos los jugadores que no tienen el valor 'rendimiento'
jugadores_sin_rendimiento = coleccion_jugadores.find({"rendimiento": {"$exists": False}})

valorDelantero = 0
reglasDelanteros = [
    {
        "condicion": lambda jugador: jugador["goles"] > 0,
        "accion": lambda: valorDelantero + 0.25
    },
    {
        "condicion": lambda jugador: jugador["goles"] > 1,
        "accion": lambda: valorDelantero + 0.25
    },
    {
        "condicion": lambda jugador: jugador["goles"] > 2,
        "accion": lambda: valorDelantero + 0.25
    },
    {
        "condicion": lambda jugador: jugador["asistencias"] > 0,
        "accion": lambda: valorDelantero + 0.25
    },
    {
        "condicion": lambda jugador: jugador["asistencias"] > 1,
        "accion": lambda: valorDelantero + 0.25
    },
    {
        "condicion": lambda jugador: jugador["asistencias"] > 2,
        "accion": lambda: valorDelantero + 0.25
    },
    {
        "condicion": lambda jugador: jugador["goles_esperados"] > 0,
        "accion": lambda: valorDelantero + 0.2
    },
    {
        "condicion": lambda jugador: jugador["goles_esperados"] > 0.04,
        "accion": lambda: valorDelantero + 0.2
    },
    {
        "condicion": lambda jugador: jugador["goles_esperados"] > 0.08,
        "accion": lambda: valorDelantero + 0.2
    },
    {
        "condicion": lambda jugador: jugador["pases"] > 25,
        "accion": lambda: valorDelantero + 0.15
    },
    {
        "condicion": lambda jugador: jugador["pases"] > 35,
        "accion": lambda: valorDelantero + 0.15
    },
    {
        "condicion": lambda jugador: jugador["pases"] > 45,
        "accion": lambda: valorDelantero + 0.15
    },
    {
        "condicion": lambda jugador: jugador["pases_clave"] > 0,
        "accion": lambda: valorDelantero + 0.2
    },
    {
        "condicion": lambda jugador: jugador["pases_clave"] > 1,
        "accion": lambda: valorDelantero + 0.2
    },
    {
        "condicion": lambda jugador: jugador["pases_clave"] > 2,
        "accion": lambda: valorDelantero + 0.2
    },
    {
        "condicion": lambda jugador: jugador["acciones_defensivas"] > 0,
        "accion": lambda: valorDelantero + 0.1
    },
    {
        "condicion": lambda jugador: jugador["acciones_defensivas"] > 1,
        "accion": lambda: valorDelantero + 0.1
    },
    {
        "condicion": lambda jugador: jugador["acciones_defensivas"] > 2,
        "accion": lambda: valorDelantero + 0.1
    },
    {
        "condicion": lambda jugador: jugador["regates_completados"] > 0,
        "accion": lambda: valorDelantero + 0.2
    },
    {
        "condicion": lambda jugador: jugador["regates_completados"] > 1,
        "accion": lambda: valorDelantero + 0.2
    },
    {
        "condicion": lambda jugador: jugador["regates_completados"] > 2,
        "accion": lambda: valorDelantero + 0.2
    },
    {
        "condicion": lambda jugador: jugador["tiros_porteria"] > 0,
        "accion": lambda: valorDelantero + 0.15
    },
    {
        "condicion": lambda jugador: jugador["tiros_porteria"] > 1,
        "accion": lambda: valorDelantero + 0.15
    },
    {
        "condicion": lambda jugador: jugador["tiros_porteria"] > 2,
        "accion": lambda: valorDelantero + 0.15
    },
    {
        "condicion": lambda jugador: jugador["pases_largos"] > 0,
        "accion": lambda: valorDelantero + 0.1
    },
    {
        "condicion": lambda jugador: jugador["pases_largos"] > 1,
        "accion": lambda: valorDelantero + 0.1
    },
    {
        "condicion": lambda jugador: jugador["pases_largos"] > 2,
        "accion": lambda: valorDelantero + 0.1
    },
    {
        "condicion": lambda jugador: jugador["posesiones_perdidas"] > 0,
        "accion": lambda: valorDelantero - 0.2
    },
    {
        "condicion": lambda jugador: jugador["posesiones_perdidas"] > 1,
        "accion": lambda: valorDelantero - 0.2
    },
    {
        "condicion": lambda jugador: jugador["posesiones_perdidas"] > 2,
        "accion": lambda: valorDelantero - 0.2
    }

]

valorCentrocampista = 0
reglasCentrocampistas = [
    {
        "condicion": lambda jugador: jugador["goles"] > 0,
        "accion": lambda: valorCentrocampista + 0.4
    },
    {
        "condicion": lambda jugador: jugador["goles"] > 1,
        "accion": lambda: valorCentrocampista + 0.4
    },
    {
        "condicion": lambda jugador: jugador["goles"] > 2,
        "accion": lambda: valorCentrocampista + 0.4
    },
    {
        "condicion": lambda jugador: jugador["asistencias"] > 0,
        "accion": lambda: valorCentrocampista + 0.25
    },
    {
        "condicion": lambda jugador: jugador["asistencias"] > 1,
        "accion": lambda: valorCentrocampista + 0.25
    },
    {
        "condicion": lambda jugador: jugador["asistencias"] > 2,
        "accion": lambda: valorCentrocampista + 0.25
    },
    {
        "condicion": lambda jugador: jugador["goles_esperados"] > 0,
        "accion": lambda: valorCentrocampista + 0.3
    },
    {
        "condicion": lambda jugador: jugador["goles_esperados"] > 0.04,
        "accion": lambda: valorCentrocampista + 0.3
    },
    {
        "condicion": lambda jugador: jugador["goles_esperados"] > 0.08,
        "accion": lambda: valorCentrocampista + 0.3
    },
    {
        "condicion": lambda jugador: jugador["pases"] > 25,
        "accion": lambda: valorCentrocampista + 0.2
    },
    {
        "condicion": lambda jugador: jugador["pases"] > 35,
        "accion": lambda: valorCentrocampista + 0.2
    },
    {
        "condicion": lambda jugador: jugador["pases"] > 45,
        "accion": lambda: valorCentrocampista + 0.2
    },
    {
        "condicion": lambda jugador: jugador["pases_clave"] > 0,
        "accion": lambda: valorCentrocampista + 0.25
    },
    {
        "condicion": lambda jugador: jugador["pases_clave"] > 1,
        "accion": lambda: valorCentrocampista + 0.25
    },
    {
        "condicion": lambda jugador: jugador["pases_clave"] > 2,
        "accion": lambda: valorCentrocampista + 0.25
    },
    {
        "condicion": lambda jugador: jugador["acciones_defensivas"] > 0,
        "accion": lambda: valorCentrocampista + 0.2
    },
    {
        "condicion": lambda jugador: jugador["acciones_defensivas"] > 1,
        "accion": lambda: valorCentrocampista + 0.2
    },
    {
        "condicion": lambda jugador: jugador["acciones_defensivas"] > 2,
        "accion": lambda: valorCentrocampista + 0.2
    },
    {
        "condicion": lambda jugador: jugador["regates_completados"] > 0,
        "accion": lambda: valorCentrocampista + 0.1
    },
    {
        "condicion": lambda jugador: jugador["regates_completados"] > 1,
        "accion": lambda: valorCentrocampista + 0.1
    },
    {
        "condicion": lambda jugador: jugador["regates_completados"] > 2,
        "accion": lambda: valorCentrocampista + 0.1
    },
    {
        "condicion": lambda jugador: jugador["tiros_porteria"] > 0,
        "accion": lambda: valorCentrocampista + 0.1
    },
    {
        "condicion": lambda jugador: jugador["tiros_porteria"] > 1,
        "accion": lambda: valorCentrocampista + 0.1
    },
    {
        "condicion": lambda jugador: jugador["tiros_porteria"] > 2,
        "accion": lambda: valorCentrocampista + 0.1
    },
    {
        "condicion": lambda jugador: jugador["pases_largos"] > 0,
        "accion": lambda: valorCentrocampista + 0.1
    },
    {
        "condicion": lambda jugador: jugador["pases_largos"] > 1,
        "accion": lambda: valorCentrocampista + 0.1
    },
    {
        "condicion": lambda jugador: jugador["pases_largos"] > 2,
        "accion": lambda: valorCentrocampista + 0.1
    },
    {
        "condicion": lambda jugador: jugador["posesiones_perdidas"] > 0,
        "accion": lambda: valorCentrocampista - 0.25
    },
    {
        "condicion": lambda jugador: jugador["posesiones_perdidas"] > 1,
        "accion": lambda: valorCentrocampista - 0.25
    },
    {
        "condicion": lambda jugador: jugador["posesiones_perdidas"] > 2,
        "accion": lambda: valorCentrocampista - 0.25
    },
    {
        "condicion": lambda jugador: jugador["regateado"] > 0,
        "accion": lambda: valorCentrocampista - 0.25
    },
    {
        "condicion": lambda jugador: jugador["regateado"] > 1,
        "accion": lambda: valorCentrocampista - 0.25
    },
    {
        "condicion": lambda jugador: jugador["regateado"] > 2,
        "accion": lambda: valorCentrocampista - 0.25
    },
    {
        "condicion": lambda jugador: jugador["duelos_ganados"] > 0,
        "accion": lambda: valorCentrocampista + 0.1
    },
    {
        "condicion": lambda jugador: jugador["duelos_ganados"] > 1,
        "accion": lambda: valorCentrocampista + 0.1
    },
    {
        "condicion": lambda jugador: jugador["duelos_ganados"] > 2,
        "accion": lambda: valorCentrocampista + 0.1
    }
]

valorDefensa = 0
reglasDefensa = [
    {
        "condicion": lambda jugador: jugador["pases_clave"] > 0,
        "accion": lambda: valorDefensa + 0.25
    },
    {
        "condicion": lambda jugador: jugador["pases_clave"] > 1,
        "accion": lambda: valorDefensa + 0.25
    },
    {
        "condicion": lambda jugador: jugador["pases_clave"] > 2,
        "accion": lambda: valorDefensa + 0.25
    },
    {
        "condicion": lambda jugador: jugador["acciones_defensivas"] > 0,
        "accion": lambda: valorDefensa + 0.25
    },
    {
        "condicion": lambda jugador: jugador["acciones_defensivas"] > 1,
        "accion": lambda: valorDefensa + 0.25
    },
    {
        "condicion": lambda jugador: jugador["acciones_defensivas"] > 2,
        "accion": lambda: valorDefensa + 0.25
    },
    {
        "condicion": lambda jugador: jugador["pases_largos"] > 0,
        "accion": lambda: valorDefensa + 0.1
    },
    {
        "condicion": lambda jugador: jugador["pases_largos"] > 1,
        "accion": lambda: valorDefensa + 0.1
    },
    {
        "condicion": lambda jugador: jugador["pases_largos"] > 2,
        "accion": lambda: valorDefensa + 0.1
    },
    {
        "condicion": lambda jugador: jugador["posesiones_perdidas"] > 0,
        "accion": lambda: valorDefensa - 0.3
    },
    {
        "condicion": lambda jugador: jugador["posesiones_perdidas"] > 1,
        "accion": lambda: valorDefensa - 0.3
    },
    {
        "condicion": lambda jugador: jugador["posesiones_perdidas"] > 2,
        "accion": lambda: valorDefensa - 0.3
    },
    {
        "condicion": lambda jugador: jugador["faltas"] > 0,
        "accion": lambda: valorDefensa - 0.2
    },
    {
        "condicion": lambda jugador: jugador["faltas"] > 1,
        "accion": lambda: valorDefensa - 0.2
    },
    {
        "condicion": lambda jugador: jugador["faltas"] > 2,
        "accion": lambda: valorDefensa - 0.2
    },
    {
        "condicion": lambda jugador: jugador["regateado"] > 0,
        "accion": lambda: valorDefensa - 0.25
    },
    {
        "condicion": lambda jugador: jugador["regateado"] > 1,
        "accion": lambda: valorDefensa - 0.25
    },
    {
        "condicion": lambda jugador: jugador["regateado"] > 2,
        "accion": lambda: valorDefensa - 0.25
    },
    {
        "condicion": lambda jugador: jugador["tiros_bloqueados"] > 0,
        "accion": lambda: valorDefensa + 0.25
    },
    {
        "condicion": lambda jugador: jugador["tiros_bloqueados"] > 1,
        "accion": lambda: valorDefensa + 0.25
    },
    {
        "condicion": lambda jugador: jugador["tiros_bloqueados"] > 2,
        "accion": lambda: valorDefensa + 0.25
    },
    {
        "condicion": lambda jugador: jugador["despejes"] > 3,
        "accion": lambda: valorDefensa + 0.15
    },
    {
        "condicion": lambda jugador: jugador["despejes"] > 5,
        "accion": lambda: valorDefensa + 0.15
    },
    {
        "condicion": lambda jugador: jugador["despejes"] > 8,
        "accion": lambda: valorDefensa + 0.15
    },
    {
        "condicion": lambda jugador: jugador["duelos_ganados"] > 1,
        "accion": lambda: valorDefensa + 0.15
    },
    {
        "condicion": lambda jugador: jugador["duelos_ganados"] > 3,
        "accion": lambda: valorDefensa + 0.15
    },
    {
        "condicion": lambda jugador: jugador["duelos_ganados"] > 5,
        "accion": lambda: valorDefensa + 0.15
    },
    {
        "condicion": lambda jugador: jugador["duelos_aereos_ganados"] > 0,
        "accion": lambda: valorDefensa + 0.15
    },
    {
        "condicion": lambda jugador: jugador["duelos_aereos_ganados"] > 1,
        "accion": lambda: valorDefensa + 0.15
    },
    {
        "condicion": lambda jugador: jugador["duelos_aereos_ganados"] > 2,
        "accion": lambda: valorDefensa + 0.15
    }

]

for jugador in jugadores_sin_rendimiento:
    posicion = jugador["posicion"]

    if  posicion == "DC" or posicion == "EI" or posicion == "ED":
        for regla in reglasDelanteros:
            if regla["condicion"](jugador):
                valorDelantero = regla["accion"]()
                rendimiento = valorDelantero
        print(rendimiento)
    elif posicion == "MC" or posicion == "MCO" or posicion == "MCD" or posicion == "MD" or posicion == "MI":
        for regla in reglasCentrocampistas:
            if regla["condicion"](jugador):
                valorCentrocampista = regla["accion"]()
                rendimiento = valorCentrocampista
        print(rendimiento)
    elif posicion == "DFC" or posicion == "LI" or posicion == "LD":
        for regla in reglasDefensa:
            if regla["condicion"](jugador):
                valorDefensa = regla["accion"]()
                rendimiento = valorDefensa
        print(rendimiento)
    else:
        rendimiento = 0
    
    # Actualizar el valor de 'rendimiento' en la base de datos
    rendimiento = round(rendimiento, 2)
    coleccion_jugadores.update_one({"_id": jugador["_id"]}, {"$set": {"rendimiento": rendimiento}})
    rendimiento = 0
    valorDelantero, valorCentrocampista, valorDefensa = 0, 0, 0
    print("Rendimiento actualizado.")
        