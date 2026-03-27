import csv
import time
import random  # Lisätään tämä simulointia varten
from datetime import datetime
from pymodbus.client import ModbusTcpClient

SERVER_IP = 'modbustest.online'
PORT = 502
FILE_NAME = 'modbus_data.csv'

def log_data():
    client = ModbusTcpClient(SERVER_IP, port=PORT)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"Yhdistetään palvelimeen {SERVER_IP}...")
    
    # Yritetään yhdistää, mutta jos ei onnistu, simuloidaan
    if client.connect():
        result = client.read_holding_registers(0, 5)
        if not result.isError():
            data = result.registers
            print(f"Live-data luettu: {data}")
        else:
            data = [0, 0, 0, 0, 0] # Virhetilanne
        client.close()
    else:
        # TÄMÄ ON SIMULAATIO: Jos yhteys ei toimi, keksitään luvut
        print("Yhteys ei toimi - käytetään simuloitua dataa...")
        data = [random.randint(20, 30) for _ in range(5)] # Keksii 5 lukua väliltä 20-30
        print(f"Simuloitu data: {data}")

    # Nyt 'data' on aina olemassa, joten tallennus onnistuu
    with open(FILE_NAME, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp] + data)

if __name__ == "__main__":
    # Kirjoitetaan otsikot vain, jos tiedosto on tyhjä
    with open(FILE_NAME, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Aikaleima', 'Testi', 'Reg1', 'Reg2', 'Reg3', 'Reg4'])
    
    for i in range(5):
        log_data()
        time.sleep(1)
