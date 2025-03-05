import LanusStats as ls  
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mplsoccer import Pitch

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


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

# A modificar
id_partido = "https://www.sofascore.com/es/football/match/spain-sweden/yYcswXo#id:10834044"
nombre_jugador = "Olga Carmona"
posicion = "LI"
temporada = "2024/2025"
equipo = "España"

# Abrir la página
driver.get(id_partido)

# Esperar a que la página cargue completamente
driver.implicitly_wait(0.5)

# Aceptar cookies
cookies = driver.find_element(By.XPATH, '//*[@class="fc-button-label"]')
cookies.click()

#Equipos local y visitante
local = driver.find_element(By.XPATH, '(//*[@class="Text fIvzGZ"])[1]')
print(local.text)
visitante = driver.find_element(By.XPATH, '(//*[@class="Text fIvzGZ"])[2]')
print(visitante.text)

# API sofascore
sofascore = ls.SofaScore()

mapa_calor = sofascore.get_player_heatmap(id_partido, nombre_jugador)
home_team, away_team = sofascore.get_players_match_stats(id_partido)

# Campo y rival
if local.text == equipo:
    campo = "Local"
    rival = visitante.text
else:
    campo = "Visitante"
    rival = local.text

estadisticas = driver.find_element(By.XPATH, '//*[@class="Box bkrWzf Tab cbSGUp secondary " and contains(text(), "Estadísticas")]')
estadisticas.click()
driver.implicitly_wait(0.5)

objetivo = driver.find_element(By.XPATH, f'//span[@class="Text giHhMn" and text()="{nombre_jugador}"]')
padre = objetivo.find_element(By.XPATH, './../../../..')

texto_padre = padre.text
print(texto_padre)
lineas = texto_padre.split('\n')
goles = int(lineas[1]) if len(lineas) > 1 and lineas[1].isdigit() else 0
asistencias = int(lineas[2]) if len(lineas) > 2 and lineas[2].isdigit() else 0

# Cerrar el navegador
#driver.quit()


jugador = away_team[away_team['name'] == nombre_jugador]
if jugador.empty:
    jugador = home_team[home_team['name'] == nombre_jugador]

def get_stat(jugador, stat):
    value = jugador.iloc[0][stat]
    if pd.isna(value):
        return 0
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value

if not jugador.empty:
    nombre = nombre_jugador
    mapa_calor_lista = mapa_calor.to_dict(orient='records')
    if posicion == "DC" or posicion == "EI" or posicion == "ED":
        #goles = get_stat(jugador, 'goals')
        #asistencias = get_stat(jugador, 'goalAssist')
        goles_esperados = get_stat(jugador, 'expectedGoals')
        pases = get_stat(jugador, 'totalPass')
        porcentaje_pases = get_stat(jugador, 'accuratePass')
        pases_clave = get_stat(jugador, 'keyPass')
        regates_completados = get_stat(jugador, 'wonContest')
        centros = get_stat(jugador, 'totalCross')
        toques_balon = get_stat(jugador, 'touches')
        acciones_defensivas = get_stat(jugador, 'interceptionWon')
        tiros_fuera = get_stat(jugador, 'shotOffTarget')
        tiros_porteria = get_stat(jugador, 'onTargetScoringAttempt')
        pases_largos = get_stat(jugador, 'totalLongBalls')
        posesiones_perdidas = get_stat(jugador, 'dispossessed')

    elif posicion == "MC" or posicion == "MCO" or posicion == "MCD" or posicion == "MD" or posicion == "MI":
        #goles = get_stat(jugador, 'goals')
        #asistencias = get_stat(jugador, 'goalAssist')
        goles_esperados = get_stat(jugador, 'expectedGoals')
        pases = get_stat(jugador, 'totalPass')
        porcentaje_pases = get_stat(jugador, 'accuratePass')
        pases_clave = get_stat(jugador, 'keyPass')
        regates_completados = get_stat(jugador, 'wonContest')
        centros = get_stat(jugador, 'totalCross')
        toques_balon = get_stat(jugador, 'touches')
        acciones_defensivas = get_stat(jugador, 'interceptionWon')
        tiros_fuera = get_stat(jugador, 'shotOffTarget')
        tiros_porteria = get_stat(jugador, 'onTargetScoringAttempt')
        pases_largos = get_stat(jugador, 'totalLongBalls')
        duelos_ganados = get_stat(jugador, 'duelWon')
        regateado = get_stat(jugador, 'challengeLost')
        posesiones_perdidas = get_stat(jugador, 'dispossessed')

    elif posicion == "DFC" or posicion == "LI" or posicion == "LD":
        if campo == "Visitante":
            tiros_bloqueados = get_stat(jugador, 'outfielderBlock')
        else: 
            tiros_bloqueados = get_stat(jugador, 'blockedScoringAttempt')

        entradas = get_stat(jugador, 'totalTackle')
        duelos_ganados = get_stat(jugador, 'duelWon')
        duelos_aereos_ganados = get_stat(jugador, 'aerialWon')
        despejes = get_stat(jugador, 'totalClearance') 
        acciones_defensivas = get_stat(jugador, 'interceptionWon')
        faltas = get_stat(jugador, 'fouls')
        regateado = get_stat(jugador, 'challengeLost')
        posesiones_perdidas = get_stat(jugador, 'dispossessed')

        #goles = get_stat(jugador, 'goals')
        #asistencias = get_stat(jugador, 'goalAssist')
        pases = get_stat(jugador, 'totalPass')
        porcentaje_pases = get_stat(jugador, 'accuratePass')
        pases_clave = get_stat(jugador, 'keyPass')
        toques_balon = get_stat(jugador, 'touches')
        tiros_fuera = get_stat(jugador, 'shotOffTarget')
        tiros_porteria = get_stat(jugador, 'onTargetScoringAttempt')
        pases_largos = get_stat(jugador, 'totalLongBalls')

    elif posicion == "POR":
        paradas = get_stat(jugador, 'saves')
        goles_evitados = get_stat(jugador, 'goalsPrevented')
        if campo == "Visitante":
            despejes =  get_stat(jugador, 'punches')
        else:
            despejes = get_stat(jugador, 'goodHighClaim')
        #salidas = get_stat(jugador, 'totalKeeperSweeper')
    
    else:
        print("Tipo de jugador no soportado")
else:
    print(f"No se encontraron datos para el jugador {nombre_jugador}")
