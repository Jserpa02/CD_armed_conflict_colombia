
# Conflicto Armado en Colombia y sus Efectos Territoriales

Análisis estadístico exploratorio del dataset **Conflicto y Paz** de la plataforma Terridata del Departamento Nacional de Planeación (DNP). Desarrollado como proyecto final del curso Programación para Ciencia de Datos — Universidad Tecnológica de Bolívar, NRC 2479.

El dashboard interactivo está construido en **Quarto** e integra la librería [`analizador`](https://github.com/Jserpa02/CD_pythonLibrary.git) desarrollada por el equipo como parte del proyecto.

---

## Dataset

| Campo | Detalle |
|---|---|
| **Fuente** | Terridata – Departamento Nacional de Planeación |
| **Descarga** | https://terridata.dnp.gov.co/index-app.html#/descargas |
| **Registros** | 86,134 |
| **Variables** | 13 |
| **Cobertura temporal** | 2002 – 2023 |

### Variables del dataset

| Variable | Tipo | Descripción |
|---|---|---|
| Código Departamento | Discreto | Código numérico del departamento (1–99) |
| Departamento | Nominal | Nombre del departamento |
| Código Entidad | Discreto | Código numérico de la entidad reportante |
| Entidad | Nominal | Nombre de la entidad |
| Dimensión | Nominal | Dimensión temática del indicador |
| Subcategoría | Nominal | Subcategoría dentro de la dimensión |
| Indicador | Nominal | Nombre del indicador medido |
| Dato Numérico | Continuo | Valor cuantitativo del indicador |
| Dato Cualitativo | Ordinal | Clasificación cualitativa del indicador |
| Año | Discreto | Año de registro (2002–2023) |
| Mes | Ordinal | Mes de registro |
| Fuente | Nominal | Entidad fuente del dato |
| Unidad de Medida | Nominal | Unidad en que se expresa el indicador |

---

## Hallazgos relevantes

### Cobertura territorial
El dataset cubre los **32 departamentos de Colombia** con códigos entre 1 y 99. La media del código departamental es 37.7, lo que indica una distribución moderadamente uniforme entre departamentos, con mayor concentración en los rangos bajos (Q1 = 15, mediana = 25).

### Cobertura temporal
Los registros abarcan **21 años** de datos (2002–2023). La media temporal es 2016, con el 50% de los registros concentrados entre 2011 y 2022, lo que refleja un mayor volumen de reportes en la última década — consistente con el fortalecimiento institucional del sistema de monitoreo post-acuerdo de paz.

### Estacionalidad
El mes predominante es **diciembre (mes 12)**, con Q1, mediana y Q3 todos en 12. Esto sugiere que la mayoría de los indicadores se reportan con corte anual a fin de año, más que con seguimiento mensual continuo.

### Entidades reportantes
Con más de 38,000 entidades distintas en promedio (media Código Entidad = 38,112), el dataset consolida información de un amplio ecosistema institucional a nivel nacional y territorial.

### Calidad de los datos
Se identificaron **6 oportunidades de mejora**:
- Valores faltantes en columnas territoriales (Código Departamento, Departamento, Entidad)
- Identificadores numéricos registrados como decimales (ej. `5.0`)
- Alta repetición en variables categóricas (Dimensión, Subcategoría, Indicador)
- Gran volumen que puede requerir agregaciones para análisis específicos
- Ausencia de diccionario de datos con definiciones formales de indicadores
- Redundancia territorial que se beneficiaría de una estructura relacional

---

## Cómo reproducir el análisis

### 1. Requisitos

- Python >= 3.9
- Quarto >= 1.4
- Git

### 2. Clonar el repositorio

```bash
git clone https://github.com/Jserpa02/CD_armed_conflict_colombia
cd CD_armed_conflict_colombia
```

### 3. Instalar la librería analizador

```bash
pip install git+https://github.com/Jserpa02/CD_pythonLibrary
```

### 4. Instalar dependencias adicionales

```bash
pip install pandas numpy matplotlib openpyxl
```

### 5. Renderizar el dashboard

```bash
quarto render Estudio.qmd
```

O para previsualización en vivo:

```bash
quarto preview Estudio.qmd
```

El dashboard se genera como `Estudio.html` — un archivo autocontenido que puede abrirse en cualquier navegador sin servidor.

---

## Estructura del repositorio

```
CD_armed_conflict_colombia/
│
├── conflicto_y_paz.xlsx     ← dataset
├── Estudio.qmd              ← dashboard principal (Quarto)
├── Estudio.html             ← dashboard renderizado
├── logotub.png              ← logo institucional
├── styles.css               ← estilos del dashboard
├── portadaa.tex             ← portada LaTeX
├── LICENSE
└── README.md
```

---

## Tecnologías

| Herramienta | Uso |
|---|---|
| Python 3.x | Lenguaje principal |
| Quarto | Dashboard interactivo |
| pandas | Manipulación de datos |
| numpy | Cálculo estadístico |
| matplotlib | Visualizaciones |
| analizador | Librería propia de análisis EDA |

---

## Autores

| Integrante | Código |
|---|---|
| Juan Diego Serpa Medina | T00076352 |

**Universidad Tecnológica de Bolívar**  
Programación para Ciencia de Datos — NRC 2479  
Revisado por: Prof. Jorge Luis Villalba  
Cartagena de Indias, 2026

---

## Licencia

MIT License — ver archivo [LICENSE](LICENSE)
