import sqlite3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "trm.db"
FIGURES_DIR = Path(__file__).resolve().parents[1] / "reports" / "figures"


def load_data(db_path=DB_PATH):
    """Carga los datos limpios desde SQLite."""
    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql("SELECT * FROM trm", conn, parse_dates=["valid_from", "valid_to"])
    return df


def plot_evolution(df, out_dir=FIGURES_DIR):
    """Grafica la evolucion historica completa de la TRM."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df["valid_from"], df["trm"], linewidth=0.8)
    ax.set_title("Evolucion historica de la TRM (USD/COP)")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Pesos por dolar")
    ax.grid(alpha=0.3)

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "01_evolucion_historica.png"
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"Guardada: {out_path}")


def plot_monthly_average(df, out_dir=FIGURES_DIR):
    """Grafica el promedio mensual de la TRM, con un color distinto por año."""
    df["year_month"] = df["valid_from"].dt.to_period("M")
    monthly = df.groupby("year_month")["trm"].mean()
    monthly = monthly.tail(60)

    years = monthly.index.year
    unique_years = sorted(years.unique())
    cmap = plt.get_cmap("tab10")
    color_map = {year: cmap(i % 10) for i, year in enumerate(unique_years)}
    bar_colors = [color_map[y] for y in years]

    fig, ax = plt.subplots(figsize=(13, 6))
    ax.bar(
        monthly.index.astype(str),
        monthly.values,
        color=bar_colors,
        edgecolor="white",
        linewidth=0.7,
    )
    ax.set_title("Promedio mensual de la TRM (últimos 5 años)")
    ax.set_xlabel("Mes")
    ax.set_ylabel("Pesos por dólar")
    ax.tick_params(axis="x", rotation=90)

    legend_handles = [plt.Rectangle((0, 0), 1, 1, color=color_map[y]) for y in unique_years]
    ax.legend(
        legend_handles,
        [str(y) for y in unique_years],
        title="Año",
        loc="upper left",
        bbox_to_anchor=(1.01, 1),
        borderaxespad=0,
    )

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "02_promedio_mensual.png"
    fig.savefig(out_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
    print(f"Guardada: {out_path}")


if __name__ == "__main__":
    df = load_data()
    plot_evolution(df)
    plot_monthly_average(df)