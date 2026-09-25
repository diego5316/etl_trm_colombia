import json
from pathlib import Path

import pandas as pd

RAW_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "trm_raw.json"
PROCESSED_PATH = Path(__file__).resolve().parents[1] / "data" / "processed" / "trm_clean.csv"

COLUMN_MAP = {
    "vigenciadesde": "valid_from",
    "vigenciahasta": "valid_to",
    "valor": "trm",
}


def load_raw(path=RAW_PATH):
    """Carga el JSON crudo tal como se guardo en el Extract."""
    with open(path, "r", encoding="utf-8") as f:
        rows = json.load(f)
    return pd.DataFrame(rows)


def clean(df):
    """Limpia y transforma el DataFrame crudo."""
    df = df.rename(columns=COLUMN_MAP)

    # TODO 1: quedarte solo con las columnas 'valid_from', 'valid_to', 'trm'
    df = df[["valid_from", "valid_to", "trm"]]

    # TODO 2: convertir 'trm' a float
    df["trm"] = df["trm"].astype(float)

    # TODO 3: convertir fechas a datetime
    df["valid_from"] = pd.to_datetime(df["valid_from"])
    df["valid_to"] = pd.to_datetime(df["valid_to"])

    # TODO 4: ordenar por 'valid_from' ascendente
    df = df.sort_values("valid_from")

    # TODO 5: eliminar duplicados exactos
    df = df.drop_duplicates()

    # TODO 6: validar que 'trm' no tenga nulos
    assert df["trm"].isna().sum() == 0, "Hay valores nulos en trm"

    # TODO 7: validar que todos los 'trm' sean mayores a 0
    assert (df["trm"] > 0).all(), "Hay valores de trm menores o iguales a 0"

    return df


def save_processed(df, path=PROCESSED_PATH):
    """Guarda el DataFrame limpio en CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Guardadas {len(df)} filas limpias en {path}")


if __name__ == "__main__":
    raw_df = load_raw()
    clean_df = clean(raw_df)
    print("Filas con vigencia > 1 dia:", (clean_df["valid_from"] != clean_df["valid_to"]).sum())
    save_processed(clean_df)
    print(clean_df.head())
    print(clean_df.dtypes)