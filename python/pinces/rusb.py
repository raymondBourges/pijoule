import serial, json

# Configuration du port série
port = '/dev/ttyACM0'  # Remplacez par le bon port série
baudrate = 1222  # Vitesse de communication en bauds

# Initialisation de la liaison série
ser = serial.Serial(port)#, baudrate, parity=serial.PARITY_EVEN, bytesize=serial.SEVENBITS, stopbits=serial.STOPBITS_ONE, xonxoff=False, rtscts=False)

data = []

# Lecture en boucle
while True:
    # Lire une ligne depuis la liaison série
    line = ser.readline()

    # Afficher la ligne lue
    print("****")
    print(line)
    print("ou")
    print(line.decode('ascii'))  # Utilisez le bon encodage selon vos besoins
    try:
        str = line.decode('ascii')
        data = json.loads(str)
    except json.decoder.JSONDecodeError:
        print("ERREUR ! Impossible de lire comme un tableau : ", str)
    print(data[0], " + ", data[1], " = ", data[0] + data[1])
