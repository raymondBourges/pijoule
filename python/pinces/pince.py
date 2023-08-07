import ADS1x15 # pip3 install ADS1x15-ADC (https://github.com/chandrawi/ADS1x15-ADC)
import argparse # pip install argparse
import sqlite3 # pip install pysqlite3
from sqlite3 import Error
import time, threading, math, time

# Gestion de la ligne de commande
parser = argparse.ArgumentParser(description='Mesure de la tension par pince.')
parser.add_argument('-i', '--id', help='ID du capteur', type=int, dest='idCapteur', required=True)
parser.add_argument('-e', '--entreeADS1115', help='Numéro de l''entrée sur l''ADS 1115 (0..3)', type=int, dest='entreeADS', required=True)
parser.add_argument('-t', '--tours', help='Nombre de tours dans la pince', type=int, dest='tours')
parser.add_argument('-o', '--ohms', help='Ohms de la résistance de tirage', type=int, dest='ohms')
parser.add_argument('-a', '--adresseI2C', help='Adresse I2C de l''ADS 1115', type=int, default=0x48, dest='adresseI2C')
args = parser.parse_args()

# Paramétrage lib ADS1x15
ADS = ADS1x15.ADS1115(1, args.adresseI2C)
ADS.setGain(ADS.PGA_4_096V)

# chemin vers la base
base = "/tmp/pijoule.db"

def lireEntree():
  global voltages, run_flag
  while run_flag:
    voltages.append(ADS.toVoltage(ADS.readADC(args.entreeADS)))

def getVEmax(Vs):
  VEmax = 0
  for V in Vs:
    # print(f"{V * 1000:0.2f} mv -> {(V - 1.65) *1000:0.2f} mv")
    V = abs(V - 1.65)
    if V > VEmax:
      VEmax = V
  return VEmax 

def mesure():
  global run_flag
  thread = threading.Thread(target=lireEntree)
  thread.start()
  time.sleep(1)
  run_flag = False
  thread.join() # Au cas où ça prenne un peu de temps pour s'arrêter
  # Affiche la valeur sur la console
  print(f"--- PinceI2C (id {args.idCapteur}, {args.ohms} ohms, {args.tours} tours, I2C {hex(args.adresseI2C)}:{args.entreeADS}) à {time.strftime('%H:%M:%S', time.localtime())} ---")
  print(f"Nombre de mesures : {len(voltages)}")
  VEmax = getVEmax(voltages)
  print(f"Tension entrée max (doit rester < 1650 mV) : {VEmax * 1000:0.0f} mV")
  ISmax = VEmax / args.ohms
  print(f"I sortie max : {ISmax * 1000:0.2f} mA")
  IEmax = ISmax * args.tours
  print(f"I entrée max : {IEmax:0.2f} A")
  IE = IEmax / 1.4142
  print(f"I entrée : {IE:0.2f} A")
  pva = 230 * IE # on part du prince que l'on est en 230 V
  print(f"Puissance à travers la pince : {pva:0.2f} VA")
  # Stockage en base
  ecrireEnBase(args.idCapteur, pva)

def creerBase():
  conn = None
  try:
    conn = sqlite3.connect(base)
    c = conn.cursor()
    c.execute("""
      Create table if not exists mesures(
          id integer PRIMARY KEY,
          data REAL NOT NULL    
      );
      """)
  except Error as e:
    print(f"ERREUR : Erreur lors de la création de la base de données : {e}")
    exit(1)
  finally:
    if conn:
      conn.close()

def ecrireEnBase(id, data):
  conn = None
  sql = """
    INSERT INTO mesures(id, data) VALUES(:id, :data)
      ON CONFLICT(id) DO UPDATE SET data=:data;
    """
  try:
    conn = sqlite3.connect(base)
    c = conn.cursor()
    c.execute(
      sql,
      {
        "id" : id,
        "data": data
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
  voltages = []
  run_flag = True
  mesure()
  time.sleep(2)
