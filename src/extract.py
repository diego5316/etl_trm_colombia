import json
import time
from pathlib import Path

import requests

URL = "https://www.datos.gov.co/resource/mcec-87by.json"
RAW_PATH = Path(__file__).resolve().parents[1] / "data" / "raw" / "trm_raw.json"
PAGE_SIZE = 1000


def fetch_page(offset, limit=PAGE_SIZE):
    """Trae UNA pagina de resultados, con orden estable."""
    params = {
        "$limit": limit,
        "$offset": offset,
        "$order": "vigenciadesde ASC",
    }
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_all(page_size=PAGE_SIZE):
    """Trae TODAS las filas recorriendo las paginas."""
    all_rows = []
    offset = 0
    while True:
        page = fetch_page(offset, page_size)   # TODO 1: pedir la pagina actual
        if not page:                            # TODO 2: pagina vacia -> se acabo
            break
        all_rows.extend(page)                   # TODO 3: agregar filas a la lista total
        print(f"Van {len(all_rows)} filas...")   # TODO 4: mostrar progreso
        offset += page_size                      # TODO 5: avanzar a la siguiente pagina
        if len(page) < page_size:                # TODO 6: pagina incompleta -> era la ultima
            break
        time.sleep(0.2)
    return all_rows


def save_raw(rows, path=RAW_PATH):
    """Guarda los datos EXACTAMENTE como llegaron, sin modificar."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
    print(f"Guardadas {len(rows)} filas en {path}")


if __name__ == "__main__":
    rows = fetch_all()
    save_raw(rows)