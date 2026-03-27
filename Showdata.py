import pandas as pd
import matplotlib.pyplot as plt

# Luetaan se tiedosto, jonka logger.py loi
try:
    df = pd.read_csv('modbus_data.csv', encoding='utf-8')

    # Tehdään kuvaaja
    plt.figure(figsize=(12, 8)) # Hieman isompi kuva
    
    # Piirretään tärkeimmät analogiset arvot
    plt.plot(df['Aikaleima'], df['Lämpötila (Reg0)'], label='Lämpötila (Reg0)', marker='o', linewidth=2)
    plt.plot(df['Aikaleima'], df['Paine (Reg1)'], label='Paine (Reg1)', marker='s', linestyle='--')
    plt.plot(df['Aikaleima'], df['Virtaus (Reg2)'], label='Virtaus (Reg2)', marker='^', linestyle=':')
    
    # MUUTOS: Lisätään uusia rekistereitä kuvaajaan
    plt.plot(df['Aikaleima'], df['Kierrokset (Reg5)'], label='Kierrokset (Reg5)', alpha=0.5) # alpha tekee viivasta haaleamman
    plt.plot(df['Aikaleima'], df['Teho (Reg6)'], label='Teho (Reg6)', alpha=0.5)

    plt.title('Laajennettu Modbus-dataloki visualisoituna')
    plt.xlabel('Aika')
    plt.ylabel('Arvo')
    plt.xticks(rotation=45) 
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Näytetään kuva
    print("Avataan laajennettu kuvaaja...")
    plt.show()

except Exception as e:
    print(f"Virhe: {e}. Muista ajaa päivitetty logger.py ensin!")