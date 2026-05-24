import pandas as pd
import numpy as np


def tabla_frecuencias_categoricas(
    df: pd.DataFrame,
    col: str,
    top_n: int = 10
) -> pd.DataFrame:
    serie = df[col].dropna()
    frec_abs  = serie.value_counts().head(top_n)
    frec_rel  = (frec_abs / len(serie) * 100).round(2)
    frec_acum = frec_rel.cumsum().round(2)
    return pd.DataFrame({
        "Frecuencia absoluta":    frec_abs.values,
        "Frecuencia relativa (%)": frec_rel.values,
        "Frecuencia acumulada (%)": frec_acum.values
    }, index=frec_abs.index)