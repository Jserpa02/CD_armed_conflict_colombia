"""
analizador
----------
Librería modular de análisis estadístico exploratorio para datasets CSV y Excel.

Uso rápido
----------
>>> from analizador import analizar
>>> resultado = analizar("mi_dataset.csv")

Módulos disponibles
-------------------
- calidad      : datos faltantes, duplicados
- descriptiva  : media, mediana, moda, varianza, cuartiles, asimetría, curtosis
- frecuencias  : tablas de frecuencia para variables categóricas
- graficos     : histogramas, KDE, boxplots, barras de frecuencia
- core         : orquestador principal `analizar()`
"""

# Función principal — punto de entrada recomendado
from .core import analizar, cargar_datos

# Calidad de datos
from .calidad import (
    porcentaje_datos_faltantes,
    valores_repetidos,
)

# Estadística descriptiva
from .descriptiva import (
    calcular_mdtc,
    calcular_mdd,
    calcular_mdl,
    calcular_mdf,
)

# Frecuencias categóricas
from .frecuencias import tabla_frecuencias_categoricas

# Gráficos — exportar funciones de alto nivel únicamente
# Los helpers internos (_calcular_kde, etc.) no se exponen
from .graficos import (
    histogramas,
    curvas_kde,
    boxplots,
    barras_frecuencia,
    barras_todas_categoricas,
)

__all__ = [
    # core
    "analizar",
    "cargar_datos",
    # calidad
    "porcentaje_datos_faltantes",
    "valores_repetidos",
    # descriptiva
    "calcular_mdtc",
    "calcular_mdd",
    "calcular_mdl",
    "calcular_mdf",
    # frecuencias
    "tabla_frecuencias_categoricas",
    # graficos
    "histogramas",
    "curvas_kde",
    "boxplots",
    "barras_frecuencia",
    "barras_todas_categoricas",
]