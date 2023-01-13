import busio
import digitalio
import board
import time
import json
import adafruit_mcp3xxx.mcp3008 as MCP # adafruit-circuitpython-mcp3xxx
from adafruit_mcp3xxx.analog_in import AnalogIn
import threading, time, math
import sqlite3 # pip install pysqlite3
from sqlite3 import Error

# create the spi bus
spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
# create the cs (chip select)
cs = digitalio.DigitalInOut(board.D5)
# create the mcp object
mcp = MCP.MCP3008(spi, cs)
# create an analog input channel on pin 0
chan = AnalogIn(mcp, MCP.P1)
# chemin vers la base
base = "data/pijoule.db"

def lireP1():
    global voltages, run_flag
    while run_flag:
        voltages.append(chan.voltage)

def calculerVrms(Vs):
    sumV = 0
    maxV = 0
    for mesure in Vs:
        V = mesure - 1.65 # pt milieux de la courbe à 3,3V / 2
        if V > maxV:
            maxV = V
        sqV = V * V
        sumV = sumV + sqV        
    return math.sqrt(sumV / len(Vs)), maxV 

def creerBase():
    conn = None
    try:
        conn = sqlite3.connect(base)
        c = conn.cursor()
        c.execute("""
            Create table if not exists mesures(
                id integer PRIMARY KEY,
                data text NOT NULL    
            );
            """)
    except Error as e:
        print(f"ERREUR : Erreur lors de la création de la base de données : {e}")
        exit(1)
    finally:
        if conn:
            conn.close()

def ecrireEnBase(entreeSPI, typeAppareil, puissance):
    sql = """
        INSERT INTO mesures(id, data) VALUES(:id, json(:data))
            ON CONFLICT(id) DO UPDATE SET data=json(:data);
        """
    data = {
        "meta" : {
            "point" : entreeSPI,
            "type" : typeAppareil 
        },
        "value" : round(puissance, 2)
    }
    try:
        conn = sqlite3.connect(base)
        c = conn.cursor()
        c.execute(
            sql,
            {
                "id" : entreeSPI,
                "data": json.dumps(data)
            }
            )
        conn.commit()    
    except Error as e:
        print(f"ERREUR : Erreur lors de l'insertion en base : {e}")
        exit(1)
    finally:
        if conn:
            conn.close()  

def mesure():
    global run_flag
    thread = threading.Thread(target=lireP1)
    thread.start()
    time.sleep(0.2)
    run_flag = False
    thread.join() # Au cas où ça prenne un peu de temps pour s'arrêter

    # Affiche la valeur sur la console
    print("--- PinceSPI ---")
    # print(f"Valeurs de l'entrée : {voltages}")
    print(f"Nombre de mesures : {len(voltages)}")
    Vrms, maxV = calculerVrms(voltages)
    print(f"Max V (doit rester < 1,65 V) : {maxV:0.2f} V")
    print(f"Vrms : {Vrms * 1000:0.0f} mV")
    IsortiePince = Vrms / 300 # Résistance de tirage de 300 homs
    IEntrerPince = IsortiePince * 3000 # Ratio de boucle dans la pince de 3000
    puissanceEntreePince = 230 * IEntrerPince # on part du prince que l'on est en 230 V
    print(f"Puissance à travers la pince : {puissanceEntreePince:0.2f} W")
    ecrireEnBase(1, "pince", puissanceEntreePince)

# Main loop
creerBase()
while True:
    tns = time.clock_gettime_ns(0)
    tnsEnd = tns + 1000000000
    voltages = []
    run_flag = True
    mesure()
    time.sleep(10)