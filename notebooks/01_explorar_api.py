import json
import requests

URL = "https://www.datos.gov.co/resource/mcec-87by.json"


def fetch_sample(limit=5):
    """Trae unas pocas filas para inspeccionar la estructura de la API."""
    params = {"$limit": limit}
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    data = fetch_sample()
    print(f"Filas recibidas: {len(data)}")
    print(json.dumps(data, indent=2, ensure_ascii=False))