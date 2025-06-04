from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np

# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["TFG"]
coleccion_jugadores = db["jugadores"]
resultados = db["resultados"]

zonas = [1,2,3,4,5,6,
        7,8,9,10,11,12,
        13,14,15,16,17,18,
        19,20,21,22,23,24]
zonas_valores_e1 = [0,0,0,0,0,0,
        0,0,0,0,0,0,
        0,0,0,0,0,0,
        0,0,0,0,0,0]
zonas_valores_e2 = [0,0,0,0,0,0,
        0,0,0,0,0,0,
        0,0,0,0,0,0,
        0,0,0,0,0,0]
total_rival = [0] * 24
total_local = [0] * 24
zonas_coeficientes = [
        0.1,0.25,0.4,0.6,0.7,0.8,
        0.2,0.3,0.5,0.7,0.85,1.0,
        0.2,0.3,0.5,0.7,0.85,1.0,
        0.1,0.25,0.4,0.6,0.7,0.8,  #Ataque
        
        0.8,0.7,0.5,0.4,0.3,0.1,
        1.0,0.8,0.7,0.6,0.4,0.2,
        1.0,0.8,0.7,0.6,0.4,0.2,
        0.8,0.7,0.5,0.4,0.3,0.1]  #Defensa

zonas_coeficientes_defensivos = []

partido = resultados.find_one({"Local": "Real Betis", "Visitante": "Getafe", "Temporada": "2024/2025"})

local = partido["Local"]
visitante = partido["Visitante"]
resultado = partido["Resultado"]
temporada = partido["Temporada"]

jugadores1 = list(coleccion_jugadores.find({"equipo": local, "rival": visitante, "temporada": temporada}))
jugadores2 = list(coleccion_jugadores.find({"equipo": visitante, "rival": local, "temporada": temporada}))

# Variable global para almacenar los jugadores en caché
JUGADORES_CACHE = {}

def inicializar_cache_jugadores():
    """
    Carga todos los jugadores de la colección en una caché global.
    """
    global JUGADORES_CACHE
    jugadores = coleccion_jugadores.find()  # Obtener todos los jugadores de la base de datos
    JUGADORES_CACHE = {jugador["_id"]: jugador for jugador in jugadores}

# Modificar getEstadisticasOfensivas para usar la caché
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

    return total

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

def calcularPorcentaje(jugador, zona):
    """
    Obtiene el porcentaje preprocesado de contribución de un jugador en una zona específica.
    """
    zonas_porcentajes = jugador.get("zonas_porcentajes", {})
    return zonas_porcentajes.get(zona, 0)


def normalizar_estadisticas(jugadores, maximos):
    """
    Normaliza las estadísticas de todos los jugadores utilizando NumPy.
    """
    # Convertir las estadísticas de los jugadores en un array de NumPy
    estadisticas = ["tiros", "asistencias", "pases", "duelos_ganados", "regates", "pases_clave",
                    "acciones_defensivas", "despejes", "recuperaciones", "entradas_existosas", "paradas"]

    for jugador in jugadores:
        for est in estadisticas:
            maximo = maximos.get(est, 0)
            jugador[est] = jugador.get(est, 0) / maximo if maximo != 0 else 0

    return jugadores

def calcularMaximos(jugadores1, jugadores2):
    # Inicializar los máximos en 0
    maximos = {
        "tiros": 0,
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

def normalizar(valor, maximo):
    # Si el máximo es 0, devolver 0 para evitar división por cero
    if maximo == 0:
        return 0
    return valor / maximo

def preprocesar_mapa_calor(jugadores):
    """
    Preprocesa el mapa de calor de los jugadores para calcular el porcentaje de contribución en cada zona.
    """
    for jugador in jugadores:
        mapa_calor = jugador.get("mapa_calor", [])
        zonas_contador = {z: 0 for z in zonas}

        for p in mapa_calor:
            # Determinar la zona a la que pertenece la posición
            fila = int(p["y"] // 25)  # Fila (0 a 3)
            columna = int(p["x"] // 16)  # Columna (0 a 5)
            zona = fila * 6 + columna + 1  # Número de zona (1 a 24)

            if 1 <= zona <= 24:  # Validar que la zona esté en el rango
                zonas_contador[zona] += 1

        # Calcular el porcentaje para cada zona
        total_posiciones = len(mapa_calor)
        jugador["zonas_porcentajes"] = {z: c / total_posiciones for z, c in zonas_contador.items() if total_posiciones > 0}


def calcula_zonas(local, visitante, temporada, corte=2):
    # Inicializar la caché si no está inicializada
    if not JUGADORES_CACHE:
        inicializar_cache_jugadores()

    # Obtener el partido
    partido = resultados.find_one({"Local": local, "Visitante": visitante, "Temporada": temporada})
    if not partido:
        raise ValueError(f"No se encontró el partido entre {local} y {visitante} en la temporada {temporada}.")

    jugadores1 = [jug for jug in JUGADORES_CACHE.values() if jug["equipo"] == local and jug["rival"] == visitante and jug["temporada"] == temporada]
    jugadores2 = [jug for jug in JUGADORES_CACHE.values() if jug["equipo"] == visitante and jug["rival"] == local and jug["temporada"] == temporada]
    
    preprocesar_mapa_calor(jugadores1)
    preprocesar_mapa_calor(jugadores2)

    maximos = calcularMaximos(jugadores1, jugadores2)
    # Normalizar estadísticas de los jugadores

    for z in zonas[:-1]:
        suma_total_ofensiva_e1 = 0
        suma_total_defensiva_e1 = 0
        suma_total_ofensiva_e2 = 0
        suma_total_defensiva_e2 = 0
        for j in jugadores1:
            #_id = j["_id"]
            porc = calcularPorcentaje(j, z)
            if porc != 0:
                estadisticas_ofensivas = getEstadisticasOfensivas(j["_id"], maximos) * porc
                estadisticas_defensivas = getEstadisticasDefensivas(j["_id"], maximos) * porc
                suma_total_ofensiva_e1 += estadisticas_ofensivas
                suma_total_defensiva_e1 += estadisticas_defensivas

                # Guardar los valores en el jugador para cada zona
                if z not in j:
                    j[z] = {}
                j[z]["suma_total_ofensiva"] = estadisticas_ofensivas
                j[z]["suma_total_defensiva"] = estadisticas_defensivas

        for j2 in jugadores2:
            #_id = j["_id"]
            porc = calcularPorcentaje(j2, z)
            if porc != 0:
                estadisticas_ofensivas = getEstadisticasOfensivas(j2["_id"], maximos) * porc
                estadisticas_defensivas = getEstadisticasDefensivas(j2["_id"], maximos) * porc
                suma_total_ofensiva_e2 += estadisticas_ofensivas
                suma_total_defensiva_e2 += estadisticas_defensivas

                # Guardar los valores en el jugador para cada zona
                if z not in j2:
                    j2[z] = {}
                j2[z]["suma_total_ofensiva"] = estadisticas_ofensivas
                j2[z]["suma_total_defensiva"] = estadisticas_defensivas

        zonas_valores_e1[z-1] = (suma_total_ofensiva_e1*zonas_coeficientes[z-1] - suma_total_defensiva_e2*zonas_coeficientes[z-1+24])
        zonas_valores_e2[z-1] = (suma_total_ofensiva_e2*zonas_coeficientes[z-1] - suma_total_defensiva_e1*zonas_coeficientes[z-1+24])
        total_rival[z-1] = (suma_total_ofensiva_e2*zonas_coeficientes[z-1] + suma_total_defensiva_e2*zonas_coeficientes[z-1+24])
        total_local[z-1] = (suma_total_ofensiva_e1*zonas_coeficientes[z-1] + suma_total_defensiva_e1*zonas_coeficientes[z-1+24])

    suma_total = sum(zonas_valores_e1) - sum(zonas_valores_e2)
    print(f"Suma total: {suma_total}")

    jugador_obj = JUGADORES_CACHE.get(jugadores2[4]["_id"])
    representar_mapa_jugador(jugador_obj, total_local)

    if suma_total > corte:
        return 1
    elif suma_total < -corte:
        return 2
    else:
        return 0
        

def representar_mapa(zonas_valores_e1, zonas_valores_e2):
    # Crear una matriz de 4x6 para representar las zonas
    mapa = np.zeros((4, 6))
    
    # Calcular las diferencias entre los valores de las zonas
    diferencias = np.array(zonas_valores_e1) - np.array(zonas_valores_e2)
    
    # Normalizar las diferencias en el rango [-1, 1]
    max_diferencia = max(abs(diferencias)) if max(abs(diferencias)) != 0 else 1
    diferencias_normalizadas = diferencias / max_diferencia  # Normalizar al rango [-1, 1]
    
    # Asignar las diferencias normalizadas a la matriz
    for i in range(24):
        fila = i // 6  # Índice de fila (0 a 3)
        columna = i % 6  # Índice de columna (0 a 5)
        mapa[fila, columna] = diferencias_normalizadas[i]

    # Crear el mapa de calor
    fig, ax = plt.subplots(figsize=(8, 6))
    cmap = plt.cm.RdBu_r  # Colores azul (rival domina) y rojo (jugador domina) invertidos
    cax = ax.imshow(mapa, cmap=cmap, vmin=-1, vmax=1)

    # Agregar etiquetas a las zonas y bordes
    for i in range(4):
        for j in range(6):
            zona = i * 6 + j + 1  # Número de zona (1 a 24)
            ax.text(j, i, str(zona), ha='center', va='center', color='black')
            # Dibujar un rectángulo alrededor
            rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                 edgecolor='black', facecolor='none', linewidth=1)
            ax.add_patch(rect)

    # Configurar el gráfico
    ax.set_title("Mapa de Zonas Dominadas (Gradiente)")
    fig.colorbar(cax, label="Dominio (1: Equipo 1, -1: Equipo 2)")
    ax.invert_yaxis()  # Invertir el eje Y para que la zona 1 esté abajo
    ax.set_xticks([])
    ax.set_yticks([])

    plt.show()

def representar_mapa_jugador(jugador_obj, rival_zonas_totales):
    """
    Representa un mapa de calor para un jugador, comparando sus estadísticas en cada zona
    con la sumatoria total del equipo rival en esas mismas zonas.
    """
    #print("Valores del jugador:", jugador_obj)
    nombre_jugador = jugador_obj.get("nombre", "Jugador Desconocido")
    posicion_jugador = jugador_obj.get("posicion", "Posición Desconocida")
    # Crear una matriz de 4x6 para representar las zonas
    mapa = np.zeros((4, 6))

    print(jugador_obj)

    # Calcular las diferencias entre el jugador y el equipo rival en cada zona
    for z in zonas:
        fila = (z - 1) // 6  # Índice de fila (0 a 3)
        columna = (z - 1) % 6  # Índice de columna (0 a 5)
        jugador_ofensiva = jugador_obj.get((z), {}).get("suma_total_ofensiva", 0)
        jugador_defensiva = jugador_obj.get(str(z), {}).get("suma_total_defensiva", 0)

        rival_total = rival_zonas_totales[z-1]

        # Diferencia ofensiva y defensiva
        diferencia = (jugador_ofensiva + jugador_defensiva) - rival_total
        #print("Diferencia:", diferencia)    

        if diferencia < -0.2:
            mapa[fila, columna] = 0 # Blanco para diferencias negativas     
        else:
            mapa[fila, columna] = diferencia

    # Normalizar las diferencias en el rango [-1, 1]

    mapa_transformado = np.sign(mapa) * (np.abs(mapa) ** 0.35)

    # Crear el mapa de calor
    fig, ax = plt.subplots(figsize=(8, 6))
    cmap = plt.cm.RdBu_r  # Colores azul (rival domina) y rojo (jugador domina) invertidos
    cax = ax.imshow(mapa_transformado, cmap=cmap, vmin=-1, vmax=1)

    # Agregar etiquetas a las zonas y bordes
    for i in range(4):
        for j in range(6):
            zona = i * 6 + j + 1  # Número de zona (1 a 24)
            ax.text(j, i, str(zona), ha='center', va='center', color='black')
            # Dibujar un rectángulo alrededor
            rect = plt.Rectangle((j - 0.5, i - 0.5), 1, 1,
                                 edgecolor='black', facecolor='none', linewidth=1)
            ax.add_patch(rect)

    # Configurar el gráfico
    ax.set_title(f"Mapa de Zonas Dominadas por {nombre_jugador}, pos: {posicion_jugador}")
    fig.colorbar(cax, label="Dominio (1: Domina más, -1: Domina menos)")
    ax.invert_yaxis()  # Invertir el eje Y para que la zona 1 esté abajo
    ax.set_xticks([])
    ax.set_yticks([])

    plt.show() 

if __name__ == "__main__":
    resultado = calcula_zonas("Barcelona F", "Athletic club de Bilbao F", "2024/2025")
    print(f"Resultado del partido: {resultado}")
    representar_mapa(zonas_valores_e1, zonas_valores_e2)
