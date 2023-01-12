import Adafruit_ADS1x15 as ADS #pip install adafruit_ADS1x15
import time

# Crée un objet ADS1115
ads = ADS.ADS1115()
facteurCorrection = 4.096 / (2**15) # 4.096 car c'est la valeur max accepté par le ADS115
                                    # et 2**15 car c'est une valeur en 16 bits de -2**15 a +2**15

# Infinite loop
while True:
    # Lit la valeur de l'entrée
    A1 = ads.read_adc(1)

    # Affiche la valeur sur la console
    print("-----")
    print("Valeur de l'entrée A1: {:0.2f}".format(A1 * facteurCorrection))

    # Attend 1 seconde avant de lire à nouveau
    time.sleep(1)