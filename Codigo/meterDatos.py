from pymongo import MongoClient
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import re


# Conexión a MongoDB
cliente = MongoClient("mongodb://localhost:27017")
db = cliente["TFG"]
coleccion_jugadores = db["jugadores"]

def insertar_jugador(nombre, posicion, equipo, rival, condicion, temporada, tiros, asistencias, pases, duelos_ganados, regates, pases_clave, 
                     acciones_defensivas, despejes, recuperaciones, entradas_exitosas, paradas, mapa_calor):
    if posicion == "POR":
        jugador = {
            "nombre": nombre,
            "posicion": posicion,
            "equipo": equipo,
            "rival": rival,
            "condicion": condicion,
            "temporada": temporada,
            "tiros": tiros,
            "asistencias": asistencias,
            "pases": pases,
            "duelos_ganados": duelos_ganados,
            "regates": regates,
            "pases_clave": pases_clave,
            "acciones_defensivas": acciones_defensivas,
            "despejes": despejes,
            "paradas": paradas,
            "mapa_calor": mapa_calor
    }
    else:
        jugador = {
            "nombre": nombre,
            "posicion": posicion,
            "equipo": equipo,
            "rival": rival,
            "condicion": condicion,
            "temporada": temporada,
            "tiros": tiros,
            "asistencias": asistencias,
            "pases": pases,
            "duelos_ganados": duelos_ganados,
            "regates": regates,
            "pases_clave": pases_clave,
            "acciones_defensivas": acciones_defensivas,
            "despejes": despejes,
            "recuperaciones": recuperaciones,
            "entradas_exitosas": entradas_exitosas,
            "mapa_calor": mapa_calor
    }

    coleccion_jugadores.insert_one(jugador)
    print("Jugador insertado correctamente.")

# Datos para insertar
id_partido = "https://www.sofascore.com/es/football/match/real-madrid-valencia/jiGsbbxc#id:12716835"

nombre = "Eva Maria Navarro"
posicion = "ED"
equipo = "Real Madrid F"
rival = "Valencia F"
condicion = "visitante"
paradas = 0

# Configuración de Selenium
options = Options()
options.headless = True  # Ejecutar en modo headless (sin interfaz gráfica)
service = Service(ChromeDriverManager().install())

try:
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
except Exception as e:
    print(f"Error al iniciar el WebDriver: {e}")
    exit(1)


# Abrir la página
driver.get(id_partido)

# Esperar a que la página cargue completamente
driver.implicitly_wait(0.5)

# Aceptar cookies
cookies = driver.find_element(By.XPATH, '//*[@class="fc-button-label"]')
cookies.click()

estadisticas = driver.find_element(By.XPATH, '//*[@class="Box bkrWzf Tab cbSGUp secondary " and contains(text(), "Estadísticas")]')
estadisticas.click()
driver.implicitly_wait(0.5)
objetivo = driver.find_element(By.XPATH, f'//span[@class="Text giHhMn" and text()="{nombre}"]')
padre = objetivo.find_element(By.XPATH, './../../../..')

texto_padre = padre.text
lineas = texto_padre.split('\n')

for linea in lineas:
    if '/' in linea:  # Verificar si la línea contiene el carácter '/'
        # Usar una expresión regular para extraer el número antes de '/'
        match = re.match(r'(\d+)/\d+', linea)
        if match:
            pases = int(match.group(1))  # Extraer el número como entero
            break

for linea in lineas:
    if '(' in linea and ')' in linea:  # Verificar si la línea contiene paréntesis
        # Usar una expresión regular para extraer el número antes del paréntesis
        match = re.match(r'(\d+)\s*\(\d+\)', linea)
        if match:
            duelos_ganados = int(match.group(1))  # Extraer el número como entero
            break

asistencias = int(lineas[2]) if len(lineas) > 2 and lineas[2].isdigit() else 0

#ATAQUE
ataque = driver.find_element(By.XPATH, '//*[@class="Text lzQaM" and contains(text(), "Atacante")]')
ataque.click()
driver.implicitly_wait(0.5)

objetivo = driver.find_element(By.XPATH, f'//span[@class="Text giHhMn" and text()="{nombre}"]')
padre = objetivo.find_element(By.XPATH, './../../../..')

texto_padre = padre.text
lineas = texto_padre.split('\n')

tiros = int(lineas[1]) if len(lineas) > 1 and lineas[1].isdigit() else 0

for linea in lineas:
    if '(' in linea and ')' in linea:  # Verificar si la línea contiene paréntesis
        # Usar una expresión regular para extraer el número antes del paréntesis
        match = re.match(r'(\d+)\s*\(\d+\)', linea)
        if match:
            regates = int(match.group(1))  # Extraer el número como entero
            break

#Pases clave
ataque = driver.find_element(By.XPATH, '//*[@class="Text lzQaM" and contains(text(), "Pases")]')
ataque.click()
driver.implicitly_wait(0.5)

objetivo = driver.find_element(By.XPATH, f'//span[@class="Text giHhMn" and text()="{nombre}"]')
padre = objetivo.find_element(By.XPATH, './../../../..')

texto_padre = padre.text
lineas = texto_padre.split('\n')
pases_clave = int(lineas[3]) if len(lineas) > 1 and lineas[3].isdigit() else 0

#Defensa
defensa = driver.find_element(By.XPATH, '//*[@class="Text lzQaM" and contains(text(), "Defensa")]')
defensa.click()
driver.implicitly_wait(0.5)

objetivo = driver.find_element(By.XPATH, f'//span[@class="Text giHhMn" and text()="{nombre}"]')
padre = objetivo.find_element(By.XPATH, './../../../..')

texto_padre = padre.text
lineas = texto_padre.split('\n')
acciones_defensivas = int(lineas[1]) if len(lineas) > 1 and lineas[1].isdigit() else 0
despejes = int(lineas[2]) if len(lineas) > 2 and lineas[2].isdigit() else 0
recuperaciones = int(lineas[4]) if len(lineas) > 3 and lineas[3].isdigit() else 0
entradas_exitosas = int(lineas[5]) if len(lineas) > 4 and lineas[4].isdigit() else 0

#Porteria
if posicion == "POR":
    defensa = driver.find_element(By.XPATH, '//*[@class="Text lzQaM" and contains(text(), "Portería")]')
    defensa.click()
    driver.implicitly_wait(0.5)

    try:
        objetivo = driver.find_element(By.XPATH, f'//span[@class="Text giHhMn" and text()="{nombre}"]')
        padre = objetivo.find_element(By.XPATH, './../../../..')

        texto_padre = padre.text
        lineas = texto_padre.split('\n')
        paradas = int(lineas[1]) if len(lineas) > 1 and lineas[1].isdigit() else 0
    except Exception as e:
        print(f"No se encontró al jugador en la sección de Portería: {e}")

temporada = "2024/2025"


# API sofascore
import LanusStats as ls  
sofascore = ls.SofaScore()
mapa_calor = sofascore.get_player_heatmap(id_partido, nombre)

insertar_jugador(nombre, posicion, equipo, rival, condicion, temporada, tiros, asistencias, pases, duelos_ganados, regates, pases_clave, 
                acciones_defensivas, despejes, recuperaciones, entradas_exitosas, paradas, mapa_calor)
