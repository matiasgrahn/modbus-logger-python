import csv
import time
import random
import pyodbc  # Lisää tämä
import os
from dotenv import load_dotenv
from datetime import datetime
from pymodbus.client import ModbusTcpClient

load_dotenv()
SERVER_IP = os.getenv('SERVER_IP')
PORT = os.getenv('SERVER_PORT')
FILE_NAME = 'modbus_data.csv'


# SQL-yhteysasetukset (Samat kuin PowerShellissäsi)
SQL_CONFIG = (
    f"DRIVER={{SQL Server}};"
    f"SERVER={db_server};"
    f"DATABASE={db_name};"
    f"Trusted_Connection=yes;"
)

def log_to_sql(data):
    try:
        conn = pyodbc.connect(SQL_CONFIG)
        cursor = conn.cursor()
        # SQL-lause 8 rekisterille
        query = """INSERT INTO ModbusLog 
                   (Lampotila, Paine, Virtaus, Pumppu, Venttiili, Kierrokset, Teho, Jannite) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(query, data)
        conn.commit()
        cursor.close()
        conn.close()
        print(" -> Tallennettu SQL-tietokantaan.")
    except Exception as e:
        print(f" -> SQL-virhe: {e}")

def log_data():
    client = ModbusTcpClient(SERVER_IP, port=PORT)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if client.connect():
        result = client.read_holding_registers(0, 8)
        data = result.registers if not result.isError() else [0] * 8
        client.close()
    else:
        # Simulaatio (kuten alkuperäisessä koodissasi)
        data = [random.randint(20, 30) for _ in range(3)] 
        data += [random.randint(0, 1) for _ in range(2)]   
        data += [random.randint(100, 200) for _ in range(3)] 
        
    # 1. Tallennus CSV:lle (pidetään varmuuskopiona)
    with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp] + data)
    
    # 2. Tallennus SQL:lle (UUSI TOIMINTO)
    log_to_sql(data)

# ... (pidä aiemmat importit ja log_to_sql -funktio samana) ...

if __name__ == "__main__":
    # Alustetaan CSV kerran
    with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Kirjoitetaan otsikot vain jos tiedosto on uusi
        if file.tell() == 0:
            writer.writerow(['Aikaleima', 'Lämpötila', 'Paine', 'Virtaus', 
                             'Pumppu', 'Venttiili', 'Kierrokset', 'Teho', 'Jännite'])
    
    print("Käynnistetään jatkuva tiedonkeruu (CSV + SQL)...")
    print("Paina Ctrl+C lopettaaksesi.")

    try:
        while True:
            log_data()
            time.sleep(3) 
    except KeyboardInterrupt:
        print("\nLoggaus keskeytetty. Data on tallennettu tietokantaan.")