"""
sync_data.py -- Script para sincronizar todas las fuentes de datos del proyecto.
Proyecto Equity-Signals · Python 3.12
"""

from src.data_ingest.yahoo import update_cache
from src.utils.config import load_config

def _refresh_yahoo():
    cfg = load_config()
    universe = cfg["data"]["tickers"] + cfg["data"].get("indexes", [])
    for tkr in universe:
        update_cache(tkr, spot_intervals=["1d"])
    print("Datos de Yahoo Finance actualizados.")

def main():
    # Yahoo Finance (spot OHLCV)
    _refresh_yahoo()
    # Aquí se podrían añadir otras fuentes en el futuro:
    # _refresh_otras_fuentes()
    print("Todos los datos actualizados.")

if __name__ == "__main__":
    main()

    # Ejecución:
    # python -m src.data_ingest.sync_data  