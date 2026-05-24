"""
core.py
-------
Función orquestadora principal de la librería `analizador`.
Coordina la carga de datos y la ejecución de todos los módulos
de análisis, devolviendo un diccionario estructurado con resultados.
"""

from __future__ import annotations

from pathlib import Path
from typing import Union

import pandas as pd

from .calidad import porcentaje_datos_faltantes, valores_repetidos
from .descriptiva import calcular_mdtc, calcular_mdd, calcular_mdl, calcular_mdf
from .frecuencias import tabla_frecuencias_categoricas
from .graficos import (
    histogramas,
    curvas_kde,
    boxplots,
    barras_todas_categoricas,
)


# ---------------------------------------------------------------------------
# Carga de datos
# ---------------------------------------------------------------------------

def cargar_datos(fuente: Union[str, Path, pd.DataFrame]) -> pd.DataFrame:
    """
    Carga un DataFrame desde CSV, Excel o devuelve el DataFrame
    directamente si ya es uno.

    Parameters
    ----------
    fuente : str | Path | pd.DataFrame
        Ruta a un archivo .csv / .xlsx, o un DataFrame ya cargado.

    Returns
    -------
    pd.DataFrame

    Raises
    ------
    ValueError
        Si la extensión del archivo no es compatible.
    TypeError
        Si el tipo de `fuente` no es reconocido.
    """
    if isinstance(fuente, pd.DataFrame):
        return fuente

    ruta = Path(fuente)
    extension = ruta.suffix.lower()

    loaders = {
        ".csv":  lambda p: pd.read_csv(p),
        ".xlsx": lambda p: pd.read_excel(p),
        ".xls":  lambda p: pd.read_excel(p),
    }

    if extension not in loaders:
        raise ValueError(
            f"Extensión '{extension}' no soportada. "
            f"Usa: {list(loaders)}"
        )

    return loaders[extension](ruta)


# ---------------------------------------------------------------------------
# Orquestador principal
# ---------------------------------------------------------------------------

def analizar(
    fuente: Union[str, Path, pd.DataFrame],
    top_n_categorias: int = 10,
    bins_histograma: int = 30,
    ncols_graficos: int = 2,
    incluir_graficos: bool = True,
) -> dict:
    """
    Ejecuta el análisis exploratorio completo de un dataset.

    Parameters
    ----------
    fuente : str | Path | pd.DataFrame
        Ruta a archivo CSV/Excel o DataFrame en memoria.
    top_n_categorias : int
        Top N de categorías para frecuencias y gráficos cualitativos.
    bins_histograma : int
        Número de bins para los histogramas.
    ncols_graficos : int
        Número de columnas en las cuadrículas de gráficos.
    incluir_graficos : bool
        Si False, omite la generación de figuras (útil en pipelines headless).

    Returns
    -------
    dict con claves:
        "calidad"     → dict con DataFrames de calidad de datos
        "descriptiva" → dict con DataFrames de estadística descriptiva
        "frecuencias" → dict[str, pd.DataFrame] por variable categórica
        "graficos"    → dict con figuras matplotlib (si incluir_graficos=True)
    """
    df = cargar_datos(fuente)

    resultado = {
        "calidad":     _analizar_calidad(df),
        "descriptiva": _analizar_descriptiva(df),
        "frecuencias": _analizar_frecuencias(df, top_n=top_n_categorias),
    }

    if incluir_graficos:
        resultado["graficos"] = _generar_graficos(
            df,
            bins=bins_histograma,
            ncols=ncols_graficos,
            top_n=top_n_categorias,
        )

    return resultado


# ---------------------------------------------------------------------------
# Sub-orquestadores internos
# ---------------------------------------------------------------------------

def _analizar_calidad(df: pd.DataFrame) -> dict:
    return {
        "datos_faltantes": porcentaje_datos_faltantes(df),
        "valores_repetidos": valores_repetidos(df),
    }


def _analizar_descriptiva(df: pd.DataFrame) -> dict:
    return {
        "mdtc": calcular_mdtc(df),   # Media, Mediana, Moda, Rango
        "mdd":  calcular_mdd(df),    # Varianza, Desv. Std, CV, Rango
        "mdl":  calcular_mdl(df),    # Cuartiles Q1, Q2, Q3, IQR
        "mdf":  calcular_mdf(df),    # Asimetría, Curtosis
    }


def _analizar_frecuencias(df: pd.DataFrame, top_n: int) -> dict[str, pd.DataFrame]:
    cols_cat = df.select_dtypes(include="object").columns.tolist()
    return {
        col: tabla_frecuencias_categoricas(df, col, top_n=top_n)
        for col in cols_cat
    }


def _generar_graficos(
    df: pd.DataFrame,
    bins: int,
    ncols: int,
    top_n: int,
) -> dict:
    graficos: dict = {}

    if df.select_dtypes(include="number").shape[1] > 0:
        graficos["histogramas"] = histogramas(df, bins=bins, ncols=ncols)
        graficos["kde"]         = curvas_kde(df, ncols=ncols)
        graficos["boxplots"]    = boxplots(df, ncols=ncols)

    if df.select_dtypes(include="object").shape[1] > 0:
        graficos["barras"] = barras_todas_categoricas(df, top_n=top_n)

    return graficos