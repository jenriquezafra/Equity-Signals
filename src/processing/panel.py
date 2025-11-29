"""
panel.py -- Construcción del panel multiactivo OHLCV limpio.
Proyecto Equity-Signals · Python 3.12
"""

from pathlib import Path
import pandas as pd
from typing import Dict

from src.utils.config import load_config

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

def _list_processed_files() -> Dict[str, Path]:
    """
    Detecta todos los ficheros procesados relevantes (yahoo) y devuelve
    un mapping {ticker: path}.
    Se asume el patrón <ticker>_spot_1d_latest.parquet
    """
    files = PROCESSED_DIR.glob("*.parquet")
    mapping = {}

    for p in files:
        name = p.name
        # ejemplo: AAPL_spot_1d_latest.parquet
        if "_spot_" not in name:
            continue
        ticker = name.split("_spot_")[0]
        mapping[ticker] = p

    return mapping


def _load_single_ticker(path: Path) -> pd.DataFrame:
    """
    Carga un parquet procesado, asegura índice de fecha y ordena.
    """
    df = pd.read_parquet(path)
    df = df.sort_index()

    # Normalizar timestamps
    if df.index.tz is not None:
        df = df.tz_convert("UTC").tz_localize(None)

    return df


# -----------------------------------------------------------------------------
# Panel builder
# -----------------------------------------------------------------------------

def build_ohlcv_panel() -> pd.DataFrame:
    """
    Construye el panel multiactivo OHLCV:
    - lee todos los ficheros procesados
    - concatena con columnas MultiIndex (ticker, campo)
    - alinea fechas
    - recorta según config
    - guarda en data/processed/prices_ohlcv_panel.parquet
    """

    cfg = load_config()
    universe = cfg["data"]["tickers"] + cfg["data"].get("indexes", [])
    start = cfg["data"]["start_date"]
    end = cfg["data"]["end_date"]

    files = _list_processed_files()
    missing = [t for t in universe if t not in files]
    if missing:
        raise FileNotFoundError(f"No se encuentran ficheros procesados para: {missing}")

    frames = {}

    for tkr in universe:
        path = files[tkr]
        df = _load_single_ticker(path)

        # MultiIndex: (ticker, campo)
        df = df.add_prefix(f"{tkr}__")  # prefijo temporal para evitar colisiones
        frames[tkr] = df

    # Concatenar columnas
    merged = pd.concat(frames.values(), axis=1)

    # Convertir columnas al MultiIndex (ticker, campo)
    new_cols = []
    for col in merged.columns:
        tkr, field = col.split("__", 1)
        new_cols.append((tkr, field))

    merged.columns = pd.MultiIndex.from_tuples(new_cols, names=["ticker", "field"])

    # Recorte temporal
    merged = merged.loc[start:end]

    # Guardar
    out_path = PROCESSED_DIR / "prices_ohlcv_panel.parquet"
    merged.to_parquet(out_path, compression="zstd")

    print(f"Panel multiactivo guardado en: {out_path}")

    return merged


if __name__ == "__main__":
    build_ohlcv_panel()