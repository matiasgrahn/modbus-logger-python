import csv
import time
import random
import pyodbc
import os
from datetime import datetime
from dotenv import load_dotenv
from pymodbus.client import ModbusTcpClient

# 1. Asetukset .env-tiedostosta
load_dotenv()
SERVER_IP = os.getenv('SERVER_IP')
PORT = os.getenv('SERVER_PORT')
DB_SERVER = os.getenv('DB_SERVER')
DB_NAME = os.getenv('DB_NAME')
FILE_NAME = 'modbus_combined_data.csv'

# SQL-yhteysasetukset
SQL_CONFIG = (
    f"DRIVER={{SQL Server}};"
    f"SERVER={DB_SERVER};"
    f"DATABASE={DB_NAME};"
    f"Trusted_Connection=yes;"
)

def log_to_sql(data):
    try:
        conn = pyodbc.connect(SQL_CONFIG)
        cursor = conn.cursor()
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

def run_system():
    client = ModbusTcpClient(SERVER_IP, port=PORT)
    print(f"--- Järjestelmä käynnistetty ---")
    print("Paina Ctrl + C lopettaaksesi.")

    # Alustetaan CSV-otsikot jos tiedosto on uusi
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Aikaleima', 'Temp', 'Press', 'Flow', 'Pump', 'Valve', 'RPM', 'Power', 'Volt'])

    try:
        while True:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if client.connect():
                # VAIHE 1: Kirjoitetaan uudet random-arvot väylään
                new_values = [
                    random.randint(20, 80),    # Lämpötila
                    random.randint(950, 1050), # Paine
                    random.randint(10, 60),    # Virtaus
                    random.choice([0, 1]),     # Pumppu
                    random.randint(0, 100),    # Venttiili
                    random.randint(1000, 3000),# RPM
                    random.randint(200, 800),  # Teho
                    random.randint(220, 240)   # Jännite
                ]
                client.write_registers(address=0, values=new_values)
                print(f"[{timestamp}] Kirjoitettu väylään: {new_values[:3]}...")
                print("Kirjoitettu! Odota hetki...")
                time.sleep(1) # Lisää tämä väliaikaisesti
                # VAIHE 2: Luetaan arvot takaisin (varmistus)
                result = client.read_holding_registers(address=0, count=8)
                if not result.isError():
                    data = result.registers
                    
                    # VAIHE 3: Tallennus CSV
                    with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow([timestamp] + data)
                    
                    # VAIHE 4: Tallennus SQL
                    log_to_sql(data)
                
                client.close()
            else:
                print(f"[{timestamp}] Virhe: Modbus Slaveen ei saada yhteyttä.")
            
            time.sleep(3) # Odota 3 sekuntia ennen seuraavaa kierrosta

    except KeyboardInterrupt:
        print("\nJärjestelmä pysäytetty käyttäjän toimesta.")

if __name__ == "__main__":
    run_system()