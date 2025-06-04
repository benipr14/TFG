import numpy as np
import matplotlib.pyplot as plt
from deap import base, creator, tools
from pymongo import MongoClient
import random
import sys
import calcula_zonas

# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["TFG"]
coleccion_partidos = db["resultados"]

# Parámetros
#if len(sys.argv) == 4:
TAMANIO_POBLACION = 80 #int(sys.argv[1])
NUM_GENERACIONES = 80 #int(sys.argv[2])
TASA_CRUZAMIENTO = 0.9 #float(sys.argv[3])
#TASA_MUTACION = 0.3
INDPB_MUTACION = 1 / 49
TAMANO_TORNEO = 3

vector_inicial = [0.1,0.25,0.4,0.6,0.7,0.8,
                  0.2,0.3,0.5,0.7,0.85,1,
                  0.2,0.3,0.5,0.7,0.85,1,
                  0.1,0.25,0.4,0.6,0.7,0.8,

                  0.8,0.7,0.5,0.4,0.3,0.1,
                  1.0,0.8,0.7,0.6,0.4,0.2,
                  1.0,0.8,0.7,0.6,0.4,0.2,
                  0.8,0.7,0.5,0.4,0.3,0.1,

                  4.0]

# Función de evaluación
def evaluar_vector(vector_coeficientes):
    calcula_zonas.zonas_coeficientes = vector_coeficientes[:-1]
    numero_corte = vector_coeficientes[-1]  # Último valor es el número de corte
    total_aciertos = 0
    total_partidos = coleccion_partidos.count_documents({})

    for partido in coleccion_partidos.find():
        resultado = calcula_zonas.calcula_zonas(partido["Local"], partido["Visitante"], partido["Temporada"], numero_corte)
        if resultado == 1:
            pred = "local"
        elif resultado == 0:
            pred = "empate"
        else:
            pred = "visitante"

        if partido["Resultado"] == pred:
            total_aciertos += 1

    return total_aciertos / total_partidos,

# Mutación flotante personalizada
def mutacion_uniforme_flotante(individuo, low=0.0, up=1.0, indpb=0.3):
    for i in range(len(individuo)):
        if np.random.rand() < indpb:
            if i == len(individuo) - 1:  # Último valor (número de corte)
                individuo[i] = np.random.uniform(0.0, 3)  # Rango para el número de corte
            else:
                individuo[i] = np.random.uniform(low, up)
    return individuo,

# Configuración DEAP
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
def attr_float():
    return np.random.uniform(0.0, 1.0)

def attr_last():
    return np.random.uniform(0.0, 2.5)

toolbox.register("attr_float", attr_float)
toolbox.register("attr_last", attr_last)

def individual():
    return creator.Individual([toolbox.attr_float() for _ in range(48)] + [toolbox.attr_last()])

toolbox.register("individual", individual)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluar_vector)
toolbox.register("mate", tools.cxUniform, indpb=0.5)
toolbox.register("mutate", mutacion_uniforme_flotante, low=0.0, up=1.0, indpb=INDPB_MUTACION)
toolbox.register("select", tools.selTournament)

def algoritmo_genetico():
    poblacion = toolbox.population(n=TAMANIO_POBLACION)
    #poblacion.append(creator.Individual(vector_inicial))

    # Evaluación inicial
    for ind in poblacion:
        ind.fitness.values = toolbox.evaluate(ind)

    # Estadísticas
    stats = tools.Statistics(lambda ind: ind.fitness.values[0])
    stats.register("max", np.max)
    stats.register("mean", np.mean)

    logbook = tools.Logbook()
    logbook.header = ["gen", "max", "mean"]

    # Generaciones
    for gen in range(NUM_GENERACIONES):
        # Selección + clonación
        offspring = toolbox.select(poblacion, len(poblacion) - 1, TAMANO_TORNEO)  # Seleccionar menos espacio para la élite
        offspring = list(map(toolbox.clone, offspring))

        # Cruzamiento
        for i in range(1, len(offspring), 2):
            if np.random.rand() < TASA_CRUZAMIENTO:
                toolbox.mate(offspring[i-1], offspring[i])
                del offspring[i-1].fitness.values
                del offspring[i].fitness.values

        # Mutación
        for ind in offspring:
            toolbox.mutate(ind)
            del ind.fitness.values

        # Evaluar los modificados
        individuos_invalidos = [ind for ind in offspring if not ind.fitness.valid]
        for ind in individuos_invalidos:
            ind.fitness.values = toolbox.evaluate(ind)

        # Seleccionar los mejores individuos (elitismo)
        elite = tools.selBest(poblacion, k=1)  # Preservar los 2 mejores individuos

        # Reemplazar población con la élite y los descendientes
        poblacion[:] = elite + offspring

        # Registrar estadísticas
        record = stats.compile(poblacion)
        logbook.record(gen=gen+1, **record)
        print(f"Gen {gen+1}: Max = {record['max']:.4f}, Mean = {record['mean']:.4f}")

    # Mejor individuo
    mejor = tools.selBest(poblacion, k=1)[0]
    print("\nMejor vector encontrado:", mejor)
    print("Precisión:", mejor.fitness.values[0])
    return mejor, logbook

# Ejecutar
mejor_vector, logbook = algoritmo_genetico()

# Graficar evolución
def graficar_evolucion(logbook):
    generaciones = logbook.select("gen")
    maximos = logbook.select("max")

    plt.figure(figsize=(10, 6))
    plt.plot(generaciones, maximos, label="Máximo", color="blue")
    plt.xlabel("Generación")
    plt.ylabel("Precisión")
    plt.title("Evolución de la Precisión")
    plt.grid()
    plt.legend()
    plt.tight_layout()
    plt.show()

graficar_evolucion(logbook)
