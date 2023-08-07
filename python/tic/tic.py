import serial

# Configuration du port série
port = '/dev/ttyUSB0'  # Remplacez par le bon port série
baudrate = 1222  # Vitesse de communication en bauds

# Initialisation de la liaison série
ser = serial.Serial(port, baudrate, parity=serial.PARITY_EVEN, bytesize=serial.SEVENBITS, stopbits=serial.STOPBITS_ONE, xonxoff=False, rtscts=False)

# Lecture en boucle
while True:
    # Lire une ligne depuis la liaison série
    line = ser.readline()

    # Afficher la ligne lue
    print("****")
    print(line.decode('ascii'))  # Utilisez le bon encodage selon vos besoins
