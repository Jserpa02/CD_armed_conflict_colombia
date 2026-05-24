import pandas as pd
import numpy as np







def porcentaje_datos_faltantes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula el porcentaje de datos faltantes por variable.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame a analizar.

    Returns
    -------
    pd.DataFrame
        Tabla con estadísticas de datos faltantes.
    """

    calidad = []

    for col in df.columns:

        total = len(df[col])

        datos_na = df[col].isna().sum()

        pct_faltante = (datos_na / total) * 100

        calidad.append({
            "Variable": col,
            "Total registros": total,
            "Datos faltantes": datos_na,
            "% Faltante": round(pct_faltante, 3)
        })

    return pd.DataFrame(calidad)

def valores_repetidos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Detecta valores repetidos por variable y muestra
    cuántas veces se repiten.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset a analizar.

    Returns
    -------
    pd.DataFrame
        Tabla con:
        - Variable
        - Valor repetido
        - Frecuencia
    """

    resultados = []

    for columna in df.columns:

        frecuencias = df[columna].value_counts(dropna=True)

        repetidos = frecuencias[frecuencias > 1]

        for valor, frecuencia in repetidos.items():

            resultados.append({
                "Variable": columna,
                "Valor repetido": valor,
                "Frecuencia": frecuencia
            })

    return pd.DataFrame(resultados)