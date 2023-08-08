from fastapi import FastAPI, Response
import sqlite3 # pip install pysqlite3
from sqlite3 import Error
import json

# Usage : uvicorn app.main:app --reload --host 0.0.0.0

app = FastAPI()
# chemin vers la base
base = "/tmp/pijoule.db"

def lireMesuresEnBase():
  conn = None
  lignes = []
  try:
    conn = sqlite3.connect(base)
    c = conn.cursor()
    c.execute("""
        Select idPince, puissanceReelle, facteurDePuissance, Vrms, Irms from pinces;
      """)
    lignes = c.fetchall()    
  except Error as e:
    print(f"ERREUR : Erreur lors de la lecture de la base de données : {e}")
  finally:
    if conn:
      conn.close()
    return lignes

@app.get("/pinces")
async def root():
  content = ""
  mesures = lireMesuresEnBase()
  for mesure in mesures:
    idPince = mesure[0]
    puissanceReelle = mesure[1]
    facteurDePuissance = mesure[2]
    Vrms = mesure[3]
    Irms = mesure[4]
    content = content + f"pijoule_pince_puissanceReelle{{idPince=\"{idPince}\"}} {puissanceReelle}\n" 
    content = content + f"pijoule_pince_facteurDePuissance{{idPince=\"{idPince}\"}} {facteurDePuissance}\n" 
    content = content + f"pijoule_pince_vrms{{idPince=\"{idPince}\"}} {Vrms}\n" 
    content = content + f"pijoule_pince_irms{{idPince=\"{idPince}\"}} {Irms}\n" 
  return Response(content=content, media_type="text/plain")
