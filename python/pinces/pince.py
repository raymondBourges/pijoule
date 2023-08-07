# import argparse # pip install argparse
import sqlite3 # pip install pysqlite3
from sqlite3 import Error
import serial, json

# Configuration du port série
port = '/dev/ttyACM0'  # Remplacez par le bon port série
usb = serial.Serial(port)

# Gestion de la ligne de commande
# parser = argparse.ArgumentParser(description='Mesure de la tension par pince.')
# parser.add_argument('-i', '--id', help='ID du capteur', type=int, dest='idCapteur', required=True)
# parser.add_argument('-e', '--entreeADS1115', help='Numéro de l''entrée sur l''ADS 1115 (0..3)', type=int, dest='entreeADS', required=True)
# parser.add_argument('-t', '--tours', help='Nombre de tours dans la pince', type=int, dest='tours')
# parser.add_argument('-o', '--ohms', help='Ohms de la résistance de tirage', type=int, dest='ohms')
# parser.add_argument('-a', '--adresseI2C', help='Adresse I2C de l''ADS 1115', type=int, default=0x48, dest='adresseI2C')
# args = parser.parse_args()

# chemin vers la base
base = "/tmp/pijoule.db"

def creerBase():
  conn = None
  try:
    conn = sqlite3.connect(base)
    c = conn.cursor()
    c.execute("""
      Create table if not exists pinces(
          idPince integer PRIMARY KEY,
          puissanceReelle REAL NOT NULL,
          facteurDePuissance REAL NOT NULL,
          Vrms REAL NOT NULL,
          Irms REAL NOT NULL
      );
      """)
  except Error as e:
    print(f"ERREUR : Erreur lors de la création de la base de données : {e}")
    exit(1)
  finally:
    if conn:
      conn.close()

def ecrireEnBase(data):
  conn = None
  sql = """
    INSERT INTO pinces(idPince, puissanceReelle, facteurDePuissance, Vrms, Irms) 
        VALUES(:idPince, :puissanceReelle, :facteurDePuissance, :Vrms, :Irms)
      ON CONFLICT(idPince) DO UPDATE 
        SET idPince=:idPince, puissanceReelle=:puissanceReelle, facteurDePuissance=:facteurDePuissance,
          Vrms=:Vrms, Irms=:Irms;
    """
  try:
    conn = sqlite3.connect(base)
    c = conn.cursor()
    c.execute(
      sql,
      {
        "idPince" : data[0],
        "puissanceReelle": data[1],
        "facteurDePuissance": data[2],
        "Vrms": data[3],
        "Irms": data[4]
      }
      )
    conn.commit()    
  except Error as e:
    print(f"ERREUR : Erreur lors de l'insertion en base : {e}")
    exit(1)
  finally:
    if conn:
      conn.close()  

# Main
creerBase()
while True:
  # Lire une ligne depuis la liaison USB
  ligne = usb.readline()

  # Afficher la ligne lue
  print("****")
  print(ligne.decode('ascii'))  # Utilisez le bon encodage selon vos besoins
  try:
    str = ligne.decode('ascii')
    data = json.loads(str)
    # Stockage en base
    ecrireEnBase(data)      
  except json.decoder.JSONDecodeError:
    print("ERREUR ! Impossible de lire comme un tableau : ", str)
