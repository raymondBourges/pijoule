import Adafruit_ADS1x15 as ADS #pip install adafruit_ADS1x15
import threading, time, math

# Crée un objet ADS1115
ads = ADS.ADS1115()
#ads.data_rate = 0x00C0
facteurCorrection = 4.096 / 32767 # 4.096 car c'est la valeur max accepté par le ADS115
                                    # et 2**15 car c'est une valeur en 16 bits de -2**15 a +2**15

def lireA0():
    global voltages, run_flag
    while run_flag:
        voltages.append(ads.read_adc(0) * facteurCorrection)

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

def mesure():
    global run_flag
    thread = threading.Thread(target=lireA0)
    thread.start()
    time.sleep(1)
    run_flag = False
    thread.join() # Au cas où ça prenne un peu de temps pour s'arrêter

    # Affiche la valeur sur la console
    print("--- PinceI2C ---")
    # print(f"Valeurs de l'entrée : {voltages}")
    print(f"Nombre de mesures : {len(voltages)}")
    Vrms, maxV = calculerVrms(voltages)
    print(f"Max V (doit rester < 1,65 V) : {maxV:0.2f} V")
    print(f"Vrms : {Vrms * 1000:0.0f} mV")
    IsortiePince = Vrms / 300 # Résistance de tirage de 300 homs
    IEntrerPince = IsortiePince * 3000 # Ratio de boucle dans la pince de 3000
    puissanceEntreePince = 230 * IEntrerPince # on part du prince que l'on est en 230 V
    print(f"Puissance à travers la pince : {puissanceEntreePince:0.2f} W")

# Main
tns = time.clock_gettime_ns(0)
tnsEnd = tns + 1000000000
voltages = []
run_flag = True
mesure()