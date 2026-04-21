import csv
import time
import random
import pyodbc
import os
from datetime import datetime
from dotenv import load_dotenv
from pymodbus.client import ModbusTcpClient

# 1. Ladataan asetukset .env-tiedostosta
load_dotenv()

# Yleiset asetukset
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = os.getenv('SERVER_PORT')
FILE_NAME = 'modbus_combined_data.csv'

# --- TIETOKANTAVALINTA ---
print("--- Select Database Destination ---")
print("1. Local Database (Trusted Connection)")
print("2. Azure VM Database (SQL Authentication via VPN)")
db_choice = input("Select (1/2): ")

if db_choice == "1":
    # Haetaan lokaalit asetukset
    DB_NAME = os.getenv('DB_NAME_LOCAL')
    SQL_CONFIG = (
        f"DRIVER={{SQL Server}};"
        f"SERVER=localhost;"
        f"DATABASE={DB_NAME};"
        f"Trusted_Connection=yes;"
    )
    print(f">> Target set to LOCAL: {DB_NAME}")
else:
    # Haetaan Azure-asetukset .env-tiedostosta
    DB_SERVER = os.getenv('DB_SERVER')
    DB_NAME = os.getenv('DB_NAME_AZURE')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    
    SQL_CONFIG = (
        f"DRIVER={{ODBC Driver 17 for SQL Server}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_NAME};"
        f"UID={DB_USER};"
        f"PWD={DB_PASS};"
        f"Encrypt=no;"
    )
    print(f">> Target set to AZURE: {DB_NAME} ({DB_SERVER})")

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
    client = ModbusTcpClient(SERVER_IP, port=SERVER_PORT)
    print(f"--- Järjestelmä käynnistetty ---")
    print("Paina Ctrl + C lopettaaksesi.")

    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Aikaleima', 'Temp', 'Press', 'Flow', 'Pump', 'Valve', 'RPM', 'Power', 'Volt'])

    try:
        while True:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            if client.connect():
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
                time.sleep(1) 
                
                result = client.read_holding_registers(address=0, count=8)
                if not result.isError():
                    data = result.registers
                    
                    with open(FILE_NAME, mode='a', newline='', encoding='utf-8') as f:
                        writer = csv.writer(f)
                        writer.writerow([timestamp] + data)
                    
                    log_to_sql(data)
                
                client.close()
            else:
                print(f"[{timestamp}] Virhe: Modbus Slaveen ei saada yhteyttä.")
            
            time.sleep(3) 

    except KeyboardInterrupt:
        print("\nJärjestelmä pysäytetty käyttäjän toimesta.")

if __name__ == "__main__":
    run_system()