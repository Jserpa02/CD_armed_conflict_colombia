"""
graficos.py
-----------
Funciones de visualización modular para análisis exploratorio de datos.
Devuelven objetos (fig, axes) en lugar de hacer plt.show() directamente,
permitiendo reutilización desde notebooks, scripts o APIs.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.figure
from typing import Optional

# ---------------------------------------------------------------------------
# Paleta y constantes de estilo centralizadas
# ---------------------------------------------------------------------------

_PALETTE_DEFAULT = [
    "#4fc3f7", "#81d4fa", "#29b6f6", "#0288d1",
    "#b3e5fc", "#e1f5fe", "#0097a7", "#26c6da",
]

_STYLE = {
    "bg_figure":  "#05091a",
    "bg_axes":    "#0b1535",
    "spine":      "#0e2060",
    "tick":       "#c9dff8",
    "label":      "#d0eeff",
    "title":      "#ffffff",
    "suptitle":   "#4fc3f7",
}


# ---------------------------------------------------------------------------
# Helpers internos
# ---------------------------------------------------------------------------

def _aplicar_estilo_base(ax: plt.Axes, title: str, xlabel: str, ylabel: str) -> None:
    """Aplica el estilo oscuro estándar a un eje."""
    ax.set_facecolor(_STYLE["bg_axes"])
    ax.set_title(title, fontsize=11, color=_STYLE["title"], fontweight="bold", pad=10)
    ax.set_xlabel(xlabel, fontsize=8, color=_STYLE["label"])
    ax.set_ylabel(ylabel, fontsize=8, color=_STYLE["label"])
    ax.tick_params(colors=_STYLE["tick"], labelsize=7)
    for spine in ax.spines.values():
        spine.set_edgecolor(_STYLE["spine"])


def _crear_grilla(
    n_items: int,
    ncols: int = 2,
    alto_por_fila: float = 5.0,
    ancho: float = 14.0,
) -> tuple[matplotlib.figure.Figure, np.ndarray]:
    """Crea una figura con subplots en cuadrícula y oculta los sobrantes."""
    nrows = int(np.ceil(n_items / ncols))
    fig, axes = plt.subplots(
        nrows, ncols,
        figsize=(ancho, alto_por_fila * nrows),
        facecolor=_STYLE["bg_figure"],
    )
    axes_flat = np.array(axes).flatten()
    for j in range(n_items, len(axes_flat)):
        axes_flat[j].set_visible(False)
    return fig, axes_flat


def _color_para_indice(i: int, palette: list[str]) -> str:
    return palette[i % len(palette)]


# ---------------------------------------------------------------------------
# Gráficos cuantitativos
# ---------------------------------------------------------------------------

def histogramas(
    df: pd.DataFrame,
    bins: int = 30,
    ncols: int = 2,
    alto_por_fila: float = 5.0,
    ancho: float = 14.0,
    palette: Optional[list[str]] = None,
) -> matplotlib.figure.Figure:
    """
    Genera histogramas para todas las variables numéricas del DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset de entrada.
    bins : int
        Número de bins del histograma.
    ncols : int
        Columnas de la cuadrícula.
    alto_por_fila : float
        Altura en pulgadas por fila de la cuadrícula.
    ancho : float
        Ancho total de la figura.
    palette : list[str] | None
        Paleta de colores personalizada. Si es None, usa la paleta interna.

    Returns
    -------
    matplotlib.figure.Figure
    """
    palette = palette or _PALETTE_DEFAULT
    cols = df.select_dtypes(include="number").columns.tolist()
    fig, axes = _crear_grilla(len(cols), ncols, alto_por_fila, ancho)

    for i, col in enumerate(cols):
        ax = axes[i]
        datos = df[col].dropna().values
        color = _color_para_indice(i, palette)
        ax.hist(datos, bins=bins, color=color, alpha=0.75, edgecolor=_STYLE["bg_figure"])
        _aplicar_estilo_base(ax, f"Histograma – {col}", col, "Frecuencia")

    fig.suptitle(
        "Histogramas – Variables Numéricas",
        fontsize=14, color=_STYLE["suptitle"], fontweight="bold", y=1.01,
    )
    fig.tight_layout()
    return fig


def curvas_kde(
    df: pd.DataFrame,
    ncols: int = 2,
    alto_por_fila: float = 5.0,
    ancho: float = 14.0,
    n_puntos: int = 300,
    palette: Optional[list[str]] = None,
) -> matplotlib.figure.Figure:
    """
    Genera curvas de densidad KDE (estimación kernel gaussiana)
    para todas las variables numéricas del DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset de entrada.
    ncols : int
        Columnas de la cuadrícula.
    alto_por_fila : float
        Altura en pulgadas por fila de la cuadrícula.
    ancho : float
        Ancho total de la figura.
    n_puntos : int
        Resolución de la curva KDE (puntos en el eje x).
    palette : list[str] | None
        Paleta de colores personalizada.

    Returns
    -------
    matplotlib.figure.Figure
    """
    palette = palette or _PALETTE_DEFAULT
    cols = df.select_dtypes(include="number").columns.tolist()
    fig, axes = _crear_grilla(len(cols), ncols, alto_por_fila, ancho)

    for i, col in enumerate(cols):
        ax = axes[i]
        datos = df[col].dropna().values
        color = _color_para_indice(i, palette)
        x_vals, kde_vals = _calcular_kde(datos, n_puntos)
        ax.plot(x_vals, kde_vals, color=color, linewidth=2)
        ax.fill_between(x_vals, kde_vals, alpha=0.2, color=color)
        _aplicar_estilo_base(ax, f"KDE – {col}", col, "Densidad")

    fig.suptitle(
        "Curvas KDE – Variables Numéricas",
        fontsize=14, color=_STYLE["suptitle"], fontweight="bold", y=1.01,
    )
    fig.tight_layout()
    return fig


def _calcular_kde(datos: np.ndarray, n_puntos: int = 300) -> tuple[np.ndarray, np.ndarray]:
    """
    Calcula la curva KDE con ancho de banda de Silverman (sin scipy).

    Returns
    -------
    (x_vals, kde_vals)
    """
    n = len(datos)
    h = 1.06 * np.std(datos) * n ** (-1 / 5)
    x_vals = np.linspace(datos.min(), datos.max(), n_puntos)
    kde_vals = np.array([
        np.sum(np.exp(-0.5 * ((x - datos) / h) ** 2))
        / (n * h * np.sqrt(2 * np.pi))
        for x in x_vals
    ])
    return x_vals, kde_vals


def boxplots(
    df: pd.DataFrame,
    ncols: int = 2,
    alto_por_fila: float = 5.0,
    ancho: float = 14.0,
    palette: Optional[list[str]] = None,
) -> matplotlib.figure.Figure:
    """
    Genera boxplots para todas las variables numéricas del DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset de entrada.
    ncols : int
        Columnas de la cuadrícula.
    alto_por_fila : float
        Altura en pulgadas por fila de la cuadrícula.
    ancho : float
        Ancho total de la figura.
    palette : list[str] | None
        Paleta de colores personalizada.

    Returns
    -------
    matplotlib.figure.Figure
    """
    palette = palette or _PALETTE_DEFAULT
    cols = df.select_dtypes(include="number").columns.tolist()
    fig, axes = _crear_grilla(len(cols), ncols, alto_por_fila, ancho)

    for i, col in enumerate(cols):
        ax = axes[i]
        datos = df[col].dropna()
        color = _color_para_indice(i, palette)
        bp = ax.boxplot(
            datos,
            patch_artist=True,
            notch=False,
            medianprops=dict(color=_STYLE["suptitle"], linewidth=2.5),
            whiskerprops=dict(color=_STYLE["label"]),
            capprops=dict(color=_STYLE["label"]),
            flierprops=dict(marker="o", color=color, alpha=0.4, markersize=3),
        )
        bp["boxes"][0].set_facecolor(color)
        bp["boxes"][0].set_alpha(0.55)
        ax.set_xticks([])
        _aplicar_estilo_base(ax, f"Boxplot – {col}", "", "Valores")

    fig.suptitle(
        "Boxplots – Variables Numéricas",
        fontsize=14, color=_STYLE["suptitle"], fontweight="bold", y=1.01,
    )
    fig.tight_layout()
    return fig


# ---------------------------------------------------------------------------
# Gráficos cualitativos
# ---------------------------------------------------------------------------

def barras_frecuencia(
    df: pd.DataFrame,
    col: str,
    top_n: int = 10,
    color: Optional[str] = None,
    figsize: tuple[float, float] = (10, 4),
) -> matplotlib.figure.Figure:
    """
    Genera un gráfico de barras horizontales con las categorías
    más frecuentes de una variable cualitativa.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset de entrada.
    col : str
        Nombre de la columna categórica.
    top_n : int
        Número máximo de categorías a mostrar.
    color : str | None
        Color de las barras. Si es None, usa el primer color de la paleta.
    figsize : tuple[float, float]
        Tamaño de la figura (ancho, alto).

    Returns
    -------
    matplotlib.figure.Figure
    """
    color = color or _PALETTE_DEFAULT[0]
    top = df[col].value_counts().head(top_n).sort_values()

    fig, ax = plt.subplots(figsize=figsize, facecolor=_STYLE["bg_figure"])
    bars = ax.barh(
        top.index.astype(str),
        top.values,
        color=color,
        alpha=0.85,
        edgecolor=_STYLE["bg_figure"],
        height=0.65,
    )

    # Gradiente de opacidad para dar profundidad visual
    for j, bar in enumerate(bars):
        bar.set_alpha(0.5 + 0.5 * j / len(bars))

    # Etiquetas de valor al final de cada barra
    margen = top.max() * 0.01
    for bar, val in zip(bars, top.values):
        ax.text(
            bar.get_width() + margen,
            bar.get_y() + bar.get_height() / 2,
            f"{val:,}",
            va="center",
            fontsize=8,
            color=_STYLE["label"],
            fontweight="bold",
        )

    ax.set_facecolor(_STYLE["bg_axes"])
    ax.set_title(f"Top {top_n} – {col}", fontsize=12, color=_STYLE["title"], fontweight="bold", pad=10)
    ax.set_xlabel("Frecuencia absoluta", fontsize=9, color=_STYLE["label"])
    ax.tick_params(axis="y", labelsize=8, colors=_STYLE["tick"])
    ax.tick_params(axis="x", colors=_STYLE["tick"], labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor(_STYLE["spine"])
    ax.set_xlim(0, top.max() * 1.18)

    fig.tight_layout()
    return fig


def barras_todas_categoricas(
    df: pd.DataFrame,
    top_n: int = 10,
    figsize: tuple[float, float] = (10, 4),
    palette: Optional[list[str]] = None,
) -> dict[str, matplotlib.figure.Figure]:
    """
    Genera gráficos de barras para todas las variables categóricas del DataFrame.

    Parameters
    ----------
    df : pd.DataFrame
        Dataset de entrada.
    top_n : int
        Número máximo de categorías por variable.
    figsize : tuple[float, float]
        Tamaño de cada figura individual.
    palette : list[str] | None
        Paleta de colores personalizada.

    Returns
    -------
    dict[str, matplotlib.figure.Figure]
        Diccionario {nombre_columna: figura}.
    """
    palette = palette or _PALETTE_DEFAULT
    cols = df.select_dtypes(include="object").columns.tolist()
    return {
        col: barras_frecuencia(
            df, col,
            top_n=top_n,
            color=_color_para_indice(i, palette),
            figsize=figsize,
        )
        for i, col in enumerate(cols)
    }