"""
windowing.py -- TODO: poner uso.
Proyecto Equity_Signals ·  Python 3.11
"""

from __future__ import annotations
from typing import List, Tuple
import numpy as np
import pandas as pd


def infer_feature_cols(df: pd.DataFrame, target_col: str) -> List[str]:
    """
    Devuelve la lista de columnas de features excluyendo el target.
    """
    return [c for c in df.columns if c != target_col]


def build_windows(
    df: pd.DataFrame,
    feature_cols: List[str],
    target_col: str,
    window_size: int,
    horizon: int = 1,
    step: int = 1,
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Convierte un DataFrame temporal en tensores (X, y) para modelos secuenciales (LSTM, TFT).

    Parámetros
    ----------
    df : pd.DataFrame
        DataFrame ordenado temporalmente (índice = Date o columna equivalente).
        Debe contener al menos feature_cols y target_col.
    feature_cols : list of str
        Nombres de las columnas que se usarán como features.
    target_col : str
        Nombre de la columna objetivo (ej. 'BinaryTarget').
    window_size : int
        Número de pasos temporales por ventana (ej. 30 o 60 días).
    horizon : int, por defecto 1
        Cuántos pasos en el futuro se predice el target.
        horizon = 1 → target en t+1.
    step : int, por defecto 1
        Paso con el que se desliza la ventana (1 = todas las fechas).

    Returns
    -------
    X : np.ndarray
        Array de shape (n_samples, window_size, n_features).
    y : np.ndarray
        Array de shape (n_samples,).
    """
    
    # Asegurar orden temporal (por si acaso)
    if not df.index.is_monotonic_increasing:
        df = df.sort_index()

    feature_values = df[feature_cols].values
    target_values = df[target_col].values

    X, y = [], []
    n = len(df)

    # Último índice que permite ventana + horizonte completo
    max_start = n - horizon

    for end in range(window_size, max_start, step):
        start = end - window_size
        # Ventana de features: [t-window_size+1 ... t]
        X.append(feature_values[start:end])
        # Target en t + horizon
        y.append(target_values[end + (horizon - 1)])

    X = np.asarray(X, dtype=np.float32)
    y = np.asarray(y, dtype=np.int64)

    return X, y


def build_windows_from_df(
    df: pd.DataFrame,
    target_col: str,
    window_size: int,
    horizon: int = 1,
    step: int = 1,
) -> Tuple[np.ndarray, np.ndarray, List[str]]:
    """
    Versión conveniente: infiere automáticamente las columnas de features.

    Devuelve:
        X, y, feature_cols
    para poder reutilizar feature_cols luego en otros splits.
    """
    feature_cols = infer_feature_cols(df, target_col=target_col)
    X, y = build_windows(
        df=df,
        feature_cols=feature_cols,
        target_col=target_col,
        window_size=window_size,
        horizon=horizon,
        step=step,
    )
    return X, y, feature_cols