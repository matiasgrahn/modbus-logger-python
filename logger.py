import csv
import time
import random
from datetime import datetime
from pymodbus.client import ModbusTcpClient

SERVER_IP = '127.0.0.1' # Muuta takaisin jos käytät julkista
PORT = 502
FILE_NAME = 'modbus_data.csv'

def log_data():
    client = ModbusTcpClient(SERVER_IP, port=PORT)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Yritetään yhdistää, mutta jos ei onnistu, simuloidaan
    if client.connect():
        # MUUTOS: Luetaan nyt 8 rekisteriä (0-7)
        result = client.read_holding_registers(0, 8)
        if not result.isError():
            data = result.registers
        else:
            data = [0] * 8 # Virhetilanne: 8 nollaa
        client.close()
    else:
        # TÄMÄ ON SIMULAATIO: Keksitään luvut
        # MUUTOS: Generoidaan 8 satunnaislukua
        data = [random.randint(20, 30) for _ in range(3)] # Reg0-2: Lämpö/Paine
        data += [random.randint(0, 1) for _ in range(2)]   # Reg3-4: Tila (päällä/pois)
        data += [random.randint(100, 200) for _ in range(3)] # Reg5-7: Muu data
        
    # Tallennetaan data
    with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp] + data)

if __name__ == "__main__":
    # MUUTOS: Päivitetään otsikot vastaamaan 8 rekisteriä
    with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Aikaleima', 'Lämpötila (Reg0)', 'Paine (Reg1)', 'Virtaus (Reg2)', 
                         'Pumppu (Reg3)', 'Venttiili (Reg4)', 'Kierrokset (Reg5)', 
                         'Teho (Reg6)', 'Jännite (Reg7)'])
    
    print("Aloitetaan loggaus...")
    for i in range(10): # Tehdään 10 mittausta
        log_data()
        time.sleep(1)
    print("Loggaus valmis. Aja visualize_data.py seuraavaksi.")