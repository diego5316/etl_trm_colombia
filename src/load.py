import sqlite3
from pathlib import Path

import pandas as pd

PROCESSED_CSV = Path(__file__).resolve().parents[1] / "data" / "processed" / "trm_clean.csv"
DB_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "trm.db"
TABLE_NAME = "trm"


def load_clean_csv(path=PROCESSED_CSV):
    """Carga el CSV ya limpio, con los tipos de fecha correctos."""
    df = pd.read_csv(path, parse_dates=["valid_from", "valid_to"])
    return df


def load_to_sqlite(df, db_path=DB_PATH, table_name=TABLE_NAME):
    """Guarda el DataFrame en una base SQLite, reemplazando la tabla completa."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Guardadas {len(df)} filas en la tabla '{table_name}' de {db_path}")


if __name__ == "__main__":
    df = load_clean_csv()
    load_to_sqlite(df)