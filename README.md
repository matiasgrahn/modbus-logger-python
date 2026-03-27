# modbus-logger-python
Tämä projekti on AI (Gemini) & Python-pohjainen työkalu teollisuusdatan keräämiseen ja analysointiin.

![Projektin Graafi](Figure_1.png)

## Ominaisuudet
- **Reaaliaikainen loggaus:** Lukee 8 Modbus-rekisteriä valitulla aikavälillä.
- **Vikasietoisuus:** Jos Modbus-palvelin ei vastaa, skripti siirtyy simulointitilaan varmistaen datan jatkuvuuden.
- **Visualisointi:** Erillinen työkalu trendien tarkasteluun graafisessa muodossa.

## Asennus
1. `pip install pymodbus pandas matplotlib`
2. `python logger.py`
3. `python visualize_data.py`