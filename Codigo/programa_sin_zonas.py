from pymongo import MongoClient

# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["TFG"]
coleccion_jugadores = db["jugadores"]
coleccion_partidos = db["resultados"]

total = 0

# Variable global para almacenar los jugadores en caché
JUGADORES_CACHE = {}

def inicializar_cache_jugadores():
    """
    Carga todos los jugadores de la colección en una caché global.
    """
    global JUGADORES_CACHE
    jugadores = coleccion_jugadores.find()  # Obtener todos los jugadores de la base de datos
    JUGADORES_CACHE = {jugador["_id"]: jugador for jugador in jugadores}


def calcularMaximos(jugadores1, jugadores2):
    # Inicializar los máximos en 0
    maximos = {
        "goles": 0,
        "asistencias": 0,
        "pases": 0,
        "duelos_ganados": 0,
        "regates": 0,
        "pases_clave": 0,
        "acciones_defensivas": 0,
        "despejes": 0,
        "recuperaciones": 0,
        "entradas_existosas": 0,
        "paradas": 0
    }

    # Combinar las listas de jugadores
    todos_los_jugadores = jugadores1 + jugadores2

    # Calcular los máximos para cada estadística
    for jugador in todos_los_jugadores:
        for key in maximos.keys():
            maximos[key] = max(maximos[key], jugador.get(key, 0))

    return maximos

def normalizar_estadisticas(jugadores, maximos):
    """
    Normaliza las estadísticas de todos los jugadores utilizando NumPy.
    """
    # Convertir las estadísticas de los jugadores en un array de NumPy
    estadisticas = ["goles", "asistencias", "pases", "duelos_ganados", "regates", "pases_clave",
                    "acciones_defensivas", "despejes", "recuperaciones", "entradas_existosas", "paradas"]

    for jugador in jugadores:
        for est in estadisticas:
            maximo = maximos.get(est, 0)
            jugador[est] = jugador.get(est, 0) / maximo if maximo != 0 else 0

    return jugadores

def getEstadisticasOfensivas(jugador, maximos, jugador_obj=None):
    """
    Calcula las estadísticas ofensivas normalizadas de un jugador.
    """
    # Si no se proporciona el objeto del jugador, obtenerlo de la caché
    if jugador_obj is None:
        jugador_obj = JUGADORES_CACHE.get(jugador)
        if not jugador_obj:
            raise ValueError(f"Player '{jugador}' not found in the cache.")

    # Normalizar las estadísticas del jugador
    estadisticas = ["tiros", "asistencias", "pases", "duelos_ganados", "regates", "pases_clave"]
    total = 0
    for est in estadisticas:
        if maximos.get(est, 0) == 0:
            total += 0
        else:
            total += jugador_obj.get(est, 0) / maximos.get(est, 1) # Evitar división por cero

    return 0

# Modificar getEstadisticasDefensivas para usar la caché
def getEstadisticasDefensivas(jugador, maximos, jugador_obj=None):
    """
    Calcula las estadísticas defensivas normalizadas de un jugador.
    """
    # Si no se proporciona el objeto del jugador, obtenerlo de la caché
    if jugador_obj is None:
        jugador_obj = JUGADORES_CACHE.get(jugador)
        if not jugador_obj:
            raise ValueError(f"Player '{jugador}' not found in the cache.")
        
    estadisticas = ["acciones_defensivas", "despejes", "recuperaciones", "entradas_existosas", "paradas"]   
    total = 0
    for est in estadisticas:
        if maximos.get(est, 0) == 0:
            total += 0
        else:
            total += jugador_obj.get(est, 0) / maximos.get(est, 1) # Evitar división por cero
             
    multiplicador = 1
    if jugador_obj.get("posicion", False) == "POR":
        multiplicador = 2
    else:
        multiplicador = 1
    
    return (total * multiplicador)
 
# Inicializar la caché si no está inicializada
if not JUGADORES_CACHE:
    inicializar_cache_jugadores()
#Bucle que recorre todos los partidos
for partido in coleccion_partidos.find():
    jugadores1 = [jug for jug in JUGADORES_CACHE.values() if jug["equipo"] == partido["Local"] and jug["rival"] == partido["Visitante"] and jug["temporada"] == partido["Temporada"]]
    jugadores2 = [jug for jug in JUGADORES_CACHE.values() if jug["equipo"] == partido["Visitante"] and jug["rival"] == partido["Local"] and jug["temporada"] == partido["Temporada"]]
    
    maximos = calcularMaximos(jugadores1, jugadores2)

    suma_total_ofensiva_e1 = 0
    suma_total_defensiva_e1 = 0
    suma_total_ofensiva_e2 = 0
    suma_total_defensiva_e2 = 0

    for j in jugadores1:
        estadisticas_ofensivas = getEstadisticasOfensivas(j["_id"], maximos)
        estadisticas_defensivas = getEstadisticasDefensivas(j["_id"], maximos)
        suma_total_ofensiva_e1 += estadisticas_ofensivas
        suma_total_defensiva_e1 += estadisticas_defensivas
    for j in jugadores2:
        estadisticas_ofensivas = getEstadisticasOfensivas(j["_id"], maximos)
        estadisticas_defensivas = getEstadisticasDefensivas(j["_id"], maximos)
        suma_total_ofensiva_e2 += estadisticas_ofensivas
        suma_total_defensiva_e2 += estadisticas_defensivas
    
    total_e1 = suma_total_ofensiva_e1 - suma_total_defensiva_e2
    total_e2 = suma_total_ofensiva_e2 - suma_total_defensiva_e1

    resultado = total_e1 - total_e2

    if resultado > 2:
        resultado = "local"
    elif resultado < -2:
        resultado = "visitante"
    else:
        resultado = "empate"
    
    ganador_real = partido["Resultado"]

    if ganador_real == resultado:
        total += 1

print("Total de partidos acertados:", (total / coleccion_partidos.count_documents({})) * 100, "%")