import subprocess
import time
from concurrent.futures import ProcessPoolExecutor, as_completed

#Programa para ejecutar el algoritmo genético con diferentes combinaciones de parámetros

# Parámetros a combinar
tamanios_poblacion = [40, 80]
num_generaciones = [20, 40, 80]
tasas_cruzamiento = [1, 0.9]

output_file = "resultados_algoritmo_genetico.txt"

def ejecutar_combinacion(tam_pob, num_gen, tasa_cruz):
    start_time = time.time()
    command = [
        "python3", "algoritmo_genetico_lambda.py",
        str(tam_pob), str(num_gen), str(tasa_cruz)
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    end_time = time.time()
    elapsed_time = end_time - start_time
    return (tam_pob, num_gen, tasa_cruz, elapsed_time, result.stdout)

combinaciones = [
    (tam_pob, num_gen, tasa_cruz)
    for tam_pob in tamanios_poblacion
    for num_gen in num_generaciones
    for tasa_cruz in tasas_cruzamiento
]

with ProcessPoolExecutor(max_workers=16) as executor, open(output_file, "w") as f:
    f.write("Resultados del Algoritmo Genético\n")
    f.write("=" * 40 + "\n\n")
    futuros = [executor.submit(ejecutar_combinacion, *comb) for comb in combinaciones]
    for future in as_completed(futuros):
        tam_pob, num_gen, tasa_cruz, elapsed_time, stdout = future.result()
        f.write(f"TAMANIO_POBLACION: {tam_pob}, NUM_GENERACIONES: {num_gen}, TASA_CRUZAMIENTO: {tasa_cruz}\n")
        f.write(f"Tiempo de ejecución: {elapsed_time:.2f} segundos\n")
        f.write(stdout)
        f.write("\n" + "=" * 40 + "\n\n")

print(f"Resultados guardados en {output_file}")