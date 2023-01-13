from fastapi import FastAPI, Response
import sqlite3 # pip install pysqlite3
from sqlite3 import Error
import json

# Usage : uvicorn app.main:app --reload --host 0.0.0.0

app = FastAPI()
# chemin vers la base
base = "../data/pijoule.db"

def lireMesuresEnBase():
    conn = None
    ret = None
    try:
        conn = sqlite3.connect(base)
        c = conn.cursor()
        c.execute("""
            Select id, data from mesures;
            """)
        ret = c.fetchall()    
    except Error as e:
        print(f"ERREUR : Erreur lors de la lecture de la base de données : {e}")
    finally:
        if conn:
            conn.close()
        return ret

@app.get("/metrics")
async def root():
    content = ""
    for mesure in lireMesuresEnBase():
        id = mesure[0]
        data = json.loads(mesure[1])
        labels = f"{{point=\"{id}\", type=\"{data['meta']['type']}\"}}"
        value = data["value"]
        content = content + f"pijoule_sensor_power{labels} {value}\n" 
    prometheusData = f"pijoule_sensor_power{labels} {value}"
    return Response(content=prometheusData, media_type="text/plain")
