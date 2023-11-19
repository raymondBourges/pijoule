# Importez les modules nécessaires de PyModbus
from pymodbus.client import ModbusSerialClient
import sqlite3 # pip install pysqlite3
from sqlite3 import Error
import time
from datetime import datetime

# Paramètres de communication série Modbus
serial_port = "/dev/ttyUSB0" 
# Adresses Modbus des PZEM-OO4T
pzems = [1,2]
# chemin vers la base
base = "/tmp/pijoule.db"
# debug
debug = False

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
    maintenant = datetime.now()
    date_heure = maintenant.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{date_heure} --> ERREUR : Erreur lors de la création de la base de données : {e}")
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
    maintenant = datetime.now()
    date_heure = maintenant.strftime("%Y-%m-%d %H:%M:%S")
    print(f"{date_heure} --> ERREUR : Erreur lors de l'insertion en base : {e}")
    exit(1)
  finally:
    if conn:
      conn.close()  

# Main
creerBase()
# Créez une instance du client Modbus
client = ModbusSerialClient(method="rtu", port=serial_port, baudrate=9600, stopbits=1, bytesize=8, parity='N')
# Ouvrez la connexion série
client.connect()

while True:
  for pzem in pzems:
    try:
      data = client.read_input_registers(0, 10, slave=pzem)
      if data:
        voltage = data.getRegister(0) / 10.0 # [V]
        current = (data.getRegister(1) + (data.getRegister(2) << 16)) / 1000.0 # [A]
        power = (data.getRegister(3) + (data.getRegister(4) << 16)) / 10.0 # [W]
        energy = data.getRegister(5) + (data.getRegister(6) << 16) # [Wh]
        frequency = data.getRegister(7) / 10.0 # [Hz]
        powerFactor = data.getRegister(8) / 100.0
        alarm = data.getRegister(9) # 0 = no alarm# La réponse contient les valeurs lues
        ecrireEnBase([pzem, power, powerFactor, voltage, current])     
        if debug:
          print("********************************")
          print("ID pince : " + str(pzem))
          print("Valeurs lues : " + str(data.registers))
          print('Voltage [V]: ', voltage)
          print('Current [A]: ', current)
          print('Power [W]: ', power) # active power (V * I * power factor)
          print('Energy [Wh]: ', energy)
          print('Frequency [Hz]: ', frequency)
          print('Power factor []: ', powerFactor)
          print('Alarm : ', alarm)
      else:
        maintenant = datetime.now()
        date_heure = maintenant.strftime("%Y-%m-%d %H:%M:%S")
        print(f"{date_heure} --> ERREUR : Aucune réponse.")
    except Exception as e:
      maintenant = datetime.now()
      date_heure = maintenant.strftime("%Y-%m-%d %H:%M:%S")
      print(f"{date_heure} --> ERREUR {e}")
  time.sleep(1)

