from pymongo import MongoClient
import calcula_zonas

# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["TFG"]
coleccion_partidos = db["resultados"]

total = 0

#Define el procentaje de acirto de calcula_zonas en toda la base de datos
for partido in coleccion_partidos.find():
    resultado = calcula_zonas.calcula_zonas(partido["Local"], partido["Visitante"], partido["Temporada"])
    if resultado == 1:
        resultado = "local"
    elif resultado == 0:
        resultado = "empate"
    else:
        resultado = "visitante"
    
    ganador_real = partido["Resultado"]

    if ganador_real == resultado:
        total += 1

print("Total de partidos acertados:", (total / coleccion_partidos.count_documents({})) * 100, "%")