# analizador

Librería modular de análisis estadístico exploratorio para datasets CSV y Excel, construida sobre `pandas`, `numpy` y `matplotlib`. Diseñada con arquitectura de librería real: separación de responsabilidades, funciones puras reutilizables y salidas estructuradas.

---

## Estructura del proyecto

```
tu_proyecto/
├── analizador/
│   ├── __init__.py        # API pública
│   ├── core.py            # Orquestador principal
│   ├── calidad.py         # Calidad de datos
│   ├── descriptiva.py     # Estadística descriptiva
│   ├── frecuencias.py     # Tablas de frecuencia
│   └── graficos.py        # Visualizaciones matplotlib
│
└── tu_notebook.ipynb      # o tu_script.py / Estudio.qmd
```

> La carpeta `analizador/` debe estar en el mismo directorio desde donde ejecutas tu script o notebook.

---

## Dependencias

```
python >= 3.9
pandas
numpy
matplotlib
openpyxl      # para leer archivos .xlsx
```

Instalación:

```bash
pip install pandas numpy matplotlib openpyxl
```

---

## Uso rápido

```python
from analizador import analizar

resultado = analizar("mi_dataset.csv")
```

O con un DataFrame ya cargado:

```python
import pandas as pd
from analizador import analizar

df = pd.read_excel("mi_dataset.xlsx")
resultado = analizar(df)
```

---

## Estructura del resultado

`analizar()` devuelve un diccionario con cuatro claves principales:

```python
{
    "calidad":     { ... },   # DataFrames de calidad de datos
    "descriptiva": { ... },   # DataFrames de estadística descriptiva
    "frecuencias": { ... },   # DataFrames por variable categórica
    "graficos":    { ... }    # Figuras matplotlib
}
```

### `resultado["calidad"]`

| Clave                 | Contenido                                                                     |
| --------------------- | ----------------------------------------------------------------------------- |
| `"datos_faltantes"`   | `DataFrame` con total de registros, datos faltantes y % faltante por variable |
| `"valores_repetidos"` | `DataFrame` con variable, valor repetido y frecuencia                         |

```python
resultado["calidad"]["datos_faltantes"]
resultado["calidad"]["valores_repetidos"]
```

### `resultado["descriptiva"]`

| Clave    | Contenido                                                                            |
| -------- | ------------------------------------------------------------------------------------ |
| `"mdtc"` | Media, Mediana, Moda(s) y Rango                                                      |
| `"mdd"`  | Varianza, Desv. Estándar, CV (%) y Rango                                             |
| `"mdl"`  | Cuartiles Q1, Q2, Q3 e IQR — calculados por interpolación lineal                     |
| `"mdf"`  | Asimetría, Curtosis y su interpretación (Positiva/Negativa, Lepto/Plati/Mesocúrtica) |

```python
resultado["descriptiva"]["mdtc"]
resultado["descriptiva"]["mdd"]
resultado["descriptiva"]["mdl"]
resultado["descriptiva"]["mdf"]
```

### `resultado["frecuencias"]`

Diccionario con una entrada por cada variable categórica del dataset. Cada entrada es un `DataFrame` con frecuencia absoluta, relativa y acumulada.

```python
# Listar variables categóricas analizadas
resultado["frecuencias"].keys()

# Ver tabla de frecuencias de una variable específica
resultado["frecuencias"]["Departamento"]
```

### `resultado["graficos"]`

| Clave           | Contenido                                                 |
| --------------- | --------------------------------------------------------- |
| `"histogramas"` | `Figure` con histogramas de todas las variables numéricas |
| `"kde"`         | `Figure` con curvas de densidad KDE                       |
| `"boxplots"`    | `Figure` con boxplots                                     |
| `"barras"`      | `dict[str, Figure]` — una figura por variable categórica  |

```python
# Mostrar en notebook
resultado["graficos"]["histogramas"]
resultado["graficos"]["kde"]
resultado["graficos"]["boxplots"]

# Mostrar gráficos cualitativos
for col, fig in resultado["graficos"]["barras"].items():
    display(fig)

# Guardar una figura
resultado["graficos"]["histogramas"].savefig("histogramas.png", dpi=150)
```

---

## Parámetros de `analizar()`

```python
analizar(
    fuente,                    # str, Path o DataFrame
    top_n_categorias = 10,     # top N categorías en frecuencias y gráficos cualitativos
    bins_histograma  = 30,     # bins para histogramas
    ncols_graficos   = 2,      # columnas en las cuadrículas de gráficos
    incluir_graficos = True    # False para pipelines headless (sin matplotlib)
)
```

---

## Uso de funciones individuales

Todas las funciones pueden usarse de forma independiente sin pasar por `analizar()`.

### Calidad de datos

```python
from analizador import porcentaje_datos_faltantes, valores_repetidos

porcentaje_datos_faltantes(df)
valores_repetidos(df)
```

### Estadística descriptiva

```python
from analizador import calcular_mdtc, calcular_mdd, calcular_mdl, calcular_mdf

calcular_mdtc(df)   # Media, Mediana, Moda, Rango
calcular_mdd(df)    # Varianza, Desv. Std, CV, Rango
calcular_mdl(df)    # Q1, Q2, Q3, IQR
calcular_mdf(df)    # Asimetría, Curtosis
```

### Frecuencias categóricas

```python
from analizador import tabla_frecuencias_categoricas

tabla_frecuencias_categoricas(df, "Departamento", top_n=10)
```

### Gráficos

```python
from analizador import histogramas, curvas_kde, boxplots
from analizador import barras_frecuencia, barras_todas_categoricas

# Cuantitativos
fig = histogramas(df, bins=20, ncols=3)
fig = curvas_kde(df)
fig = boxplots(df)

# Cualitativos
fig = barras_frecuencia(df, "Departamento", top_n=15, color="#1BB9EB")
figs = barras_todas_categoricas(df, top_n=10)
```

#### Paleta personalizada

Todas las funciones de gráficos aceptan el parámetro `palette`:

```python
mi_paleta = ["#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4"]
fig = histogramas(df, palette=mi_paleta)
```

---

## Módulos internos

| Módulo           | Responsabilidad                                                                     |
| ---------------- | ----------------------------------------------------------------------------------- |
| `core.py`        | Orquesta todos los módulos. Carga datos y devuelve el diccionario de resultados.    |
| `calidad.py`     | Detecta datos faltantes y valores repetidos.                                        |
| `descriptiva.py` | Calcula todas las medidas de tendencia central, dispersión, posición y forma.       |
| `frecuencias.py` | Genera tablas de frecuencia para variables categóricas.                             |
| `graficos.py`    | Produce figuras matplotlib reutilizables. No hace `plt.show()` — devuelve `Figure`. |

### Helpers privados en `graficos.py`

Las siguientes funciones son internas y no forman parte de la API pública:

| Función                  | Descripción                                                  |
| ------------------------ | ------------------------------------------------------------ |
| `_aplicar_estilo_base()` | Aplica el tema oscuro a un eje matplotlib                    |
| `_crear_grilla()`        | Crea subplots en cuadrícula y oculta ejes sobrantes          |
| `_calcular_kde()`        | Kernel gaussiano con ancho de banda de Silverman (sin scipy) |
| `_color_para_indice()`   | Cicla sobre una paleta dado un índice                        |

---

## Notas técnicas

- **Sin dependencias estadísticas externas**: `calcular_mdl` implementa interpolación lineal manualmente; `_calcular_kde` implementa el kernel gaussiano con la regla de Silverman — ninguno depende de `scipy`.
- **Varianza muestral**: `calcular_mdd` usa `n - 1` en el denominador (estimador insesgado de Bessel).
- **Gráficos headless**: pasar `incluir_graficos=False` a `analizar()` evita cualquier inicialización de matplotlib, útil en servidores o pipelines sin display.
- **Caché de Python**: si reemplazas archivos `.py` y los cambios no se reflejan, elimina la carpeta `analizador/__pycache__/` y vuelve a ejecutar.

---

## Ejemplo completo en notebook

```python
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
from analizador import analizar

# Cargar y analizar
df = pd.read_excel("conflicto_y_paz.xlsx")
resultado = analizar(df, top_n_categorias=10, bins_histograma=30)

# Calidad
display(resultado["calidad"]["datos_faltantes"])
display(resultado["calidad"]["valores_repetidos"])

# Descriptiva
display(resultado["descriptiva"]["mdtc"])
display(resultado["descriptiva"]["mdl"])
display(resultado["descriptiva"]["mdf"])

# Gráficos cuantitativos
display(resultado["graficos"]["histogramas"])
display(resultado["graficos"]["kde"])
display(resultado["graficos"]["boxplots"])

# Gráficos cualitativos
for col, fig in resultado["graficos"]["barras"].items():
    display(fig)
    plt.close(fig)

# Guardar una figura
resultado["graficos"]["histogramas"].savefig("output/histogramas.png", dpi=150, bbox_inches="tight")
```
