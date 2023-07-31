import Adafruit_ADS1x15 as ADS #pip install adafruit_ADS1x15 
import argparse #pip install argparse
import threading, time, math

# Crée un objet ADS1115
ads = ADS.ADS1115(0x48)
facteurCorrection = 4.096 / 32767 # 4.096 car c'est la valeur max acceptée par le ADS115
                                  # et 2**15 car c'est une valeur en 16 bits de -2**15 a +2**15
# Gestion de la ligne de commande
parser = argparse.ArgumentParser(description='Mesure de la tension par pince.')
parser.add_argument('-id', help='ID du capteur', type=int, dest='idCapteur', required=True)
parser.add_argument('-e', '--EntreeADS1115', help='Numéro de l''entrée sur l''ADS 1115 (0..3)', type=int, dest='entreeADS', required=True)
parser.add_argument('-t', '--tours', help='Nombre de tours dans la pince', default=3000, type=int, dest='tours')
args = parser.parse_args()

def lireA0():
    global voltages, run_flag
    while run_flag:
        voltages.append(ads.read_adc(args.entreeADS) * facteurCorrection)

def calculerVrms(Vs):
    sumV = 0
    VEmax = 0
    for V in Vs:
#        print(f"{V * 1000:0.2f}")
        if V > VEmax:
            VEmax = V
        sqV = V * V
        sumV = sumV + sqV        
    return math.sqrt(sumV / len(Vs)), VEmax 

def mesure():
    global run_flag
    thread = threading.Thread(target=lireA0)
    thread.start()
    time.sleep(1)
    run_flag = False
    thread.join() # Au cas où ça prenne un peu de temps pour s'arrêter

    # Affiche la valeur sur la console
    print(f"--- PinceI2C ({args.idCapteur})---")
    print(f"Nombre de mesures : {len(voltages)}")
    Vrms, VEmax = calculerVrms(voltages)
    print(f"Tension entrée max (doit rester < 3300 V) : {VEmax * 1000:0.0f} mV")
    ISmax = VEmax / 150
    print(f"I sortie max : {ISmax * 1000:0.2f} mA")
    IEmax = ISmax * args.tours
    print(f"I entrée max : {IEmax:0.2f} A")
    IE = IEmax / 1.4142
    print(f"I entrée : {IE:0.2f} A")

    # print(f"Vrms : {Vrms * 1000:0.0f} mV")
    # IsortiePince = Vrms / 150 # Résistance de tirage de 150 homs
    # IEntreePince = IsortiePince * args.tours
    # print(f"Intencité à travers la pince : {IEntreePince:0.2f} A")
    # puissanceEntreePince = 230 * IEntreePince # on part du prince que l'on est en 230 V
    # print(f"Puissance à travers la pince : {puissanceEntreePince:0.2f} VA")

# Main
while True:
  voltages = []
  run_flag = True
  mesure()
  time.sleep(5)
  
