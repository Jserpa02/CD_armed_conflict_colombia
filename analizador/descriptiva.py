import numpy as np
import pandas as pd

def calcular_mdtc(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula Media, Mediana, Moda y Rango
    para variables numéricas.
    """
    resultados = []
    columnas_numericas = df.select_dtypes(include="number").columns
    for columna in columnas_numericas:

        serie = df[columna].dropna().sort_values()

        n = len(serie)

        # Evitar columnas vacías
        if n == 0:
            continue

        # MEDIA
        media = serie.sum() / n

        # MEDIANA
        if n % 2 != 0:

            mediana = serie.iloc[n // 2]

        else:

            pos = n // 2

            mediana = (
                serie.iloc[pos - 1] +
                serie.iloc[pos]
            ) / 2

        # MODA
        frecuencias = serie.value_counts()

        frecuencia_maxima = frecuencias.max()

        modas = frecuencias[
            frecuencias == frecuencia_maxima
        ].index.tolist()

        moda_str = ", ".join(
            map(str, modas[:3])
        )

        # RANGO
        rango = serie.max() - serie.min()

        resultados.append({
            "Variable": columna,
            "Media": round(media, 4),
            "Mediana": round(mediana, 4),
            "Moda(s)": moda_str,
            "Rango": round(rango, 4)
        })

    return pd.DataFrame(resultados)



def calcular_mdd(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula:
    - Varianza
    - Desviación estándar
    - Coeficiente de variación
    - Rango

    para variables numéricas.
    """

    resultados = []

    columnas_numericas = df.select_dtypes(
        include="number"
    ).columns

    for columna in columnas_numericas:

        serie = df[columna].dropna()

        n = len(serie)

        # Evitar columnas vacías
        # o con un solo valor
        if n <= 1:
            continue

        # MEDIA
        media = serie.sum() / n

        # VARIANZA MUESTRAL
        varianza = (
            ((serie - media) ** 2).sum()
            / (n - 1)
        )

        # DESVIACIÓN ESTÁNDAR
        desv_std = varianza ** 0.5

        # COEFICIENTE DE VARIACIÓN
        if media != 0:

            cv = (
                desv_std / media
            ) * 100

        else:

            cv = float("nan")

        # RANGO
        rango = serie.max() - serie.min()

        resultados.append({
            "Variable": columna,
            "Varianza": round(varianza, 4),
            "Desv. Estándar": round(desv_std, 4),
            "CV (%)": round(cv, 2),
            "Rango": round(rango, 4)
        })

    return pd.DataFrame(resultados)




def calcular_mdl(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula Q1, Q2, Q3 e IQR para variables numéricas
    usando interpolación lineal (método estándar).
    """
    resultados = []

    for columna in df.select_dtypes(include="number").columns:

        serie = df[columna].dropna().sort_values().reset_index(drop=True)

        n = len(serie)

        if n == 0:
            continue

        # CUARTILES por interpolación lineal
        # Posición real (0-indexada): L = (p/100) * (n - 1)
        def cuartil(p):
            L = (p / 100) * (n - 1)   # posición flotante
            i = int(L)                  # índice inferior
            f = L - i                   # fracción decimal

            if i + 1 < n:
                return serie.iloc[i] + f * (serie.iloc[i + 1] - serie.iloc[i])
            else:
                return serie.iloc[i]

        q1 = cuartil(25)
        q2 = cuartil(50)
        q3 = cuartil(75)
        iqr = q3 - q1

        resultados.append({
            "Variable":     columna,
            "Q1":           round(q1,  4),
            "Q2 (Mediana)": round(q2,  4),
            "Q3":           round(q3,  4),
            "IQR":          round(iqr, 4),
        })

    return pd.DataFrame(resultados)




def calcular_mdf(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula:
    - Asimetría
    - Curtosis
    - Interpretación descriptiva

    para variables numéricas.
    """

    resultados = []

    columnas_numericas = df.select_dtypes(
        include="number"
    ).columns

    for columna in columnas_numericas:

        serie = df[columna].dropna()

        n = len(serie)

        # Evitar problemas estadísticos
        if n <= 1:
            continue

        media = serie.mean()

        desv = serie.std()

        # Evitar división entre cero
        if desv == 0:
            continue

        # ASIMETRÍA
        asimetria = (
            ((serie - media) ** 3).sum()
            / (n * (desv ** 3))
        )

        # CURTOSIS
        curtosis = (
            ((serie - media) ** 4).sum()
            / (n * (desv ** 4))
        ) - 3

        # INTERPRETACIÓN ASIMETRÍA
        if asimetria > 0:

            tipo_asimetria = "Positiva →"

        elif asimetria < 0:

            tipo_asimetria = "Negativa ←"

        else:

            tipo_asimetria = "Simétrica"

        # INTERPRETACIÓN CURTOSIS
        if curtosis > 0:

            tipo_curtosis = "Leptocúrtica"

        elif curtosis < 0:

            tipo_curtosis = "Platicúrtica"

        else:

            tipo_curtosis = "Mesocúrtica"

        resultados.append({
            "Variable": columna,
            "Asimetría": round(asimetria, 4),
            "Curtosis": round(curtosis, 4),
            "Tipo asimetría": tipo_asimetria,
            "Tipo curtosis": tipo_curtosis
        })

    return pd.DataFrame(resultados)