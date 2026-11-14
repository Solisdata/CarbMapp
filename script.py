"""Télécharge le CSV des prix des carburants (data.gouv.fr), le nettoie
et écrit data/stations.json pour l'application Android."""
import io
import json
import os

import pandas as pd
import requests

URL = "https://www.data.gouv.fr/fr/datasets/r/edd67f5b-46d0-4663-9de9-e5db1c880160"
OUTPUT_PATH = os.path.join("data", "stations.json")

# Colonnes du CSV -> clé courte du carburant
FUELS = {
    "gazole": "Prix Gazole",
    "sp95": "Prix SP95",
    "e10": "Prix E10",
    "sp98": "Prix SP98",
    "e85": "Prix E85",
    "gplc": "Prix GPLc",
}


def main():
    local_csv = os.environ.get("LOCAL_CSV")  # pour tester sans télécharger
    if local_csv:
        content = open(local_csv, "rb").read()
    else:
        r = requests.get(URL, timeout=120)
        r.raise_for_status()
        content = r.content
    df = pd.read_csv(io.BytesIO(content), sep=";", encoding="utf-8-sig", dtype={"Code postal": str})

    # Les coordonnées sont stockées multipliées par 100 000
    df["lat"] = pd.to_numeric(df["latitude"], errors="coerce") / 100000
    df["lon"] = pd.to_numeric(df["longitude"], errors="coerce") / 100000
    df = df.dropna(subset=["lat", "lon"])
    # Garde uniquement des coordonnées plausibles (France + outre-mer)
    df = df[df["lat"].between(-90, 90) & df["lon"].between(-180, 180)]

    stations = []
    for _, row in df.iterrows():
        prices = {}
        for key, col in FUELS.items():
            price = pd.to_numeric(row.get(col), errors="coerce")
            if pd.notna(price):
                entry = {"prix": round(float(price), 3)}
                maj = row.get(f"{col} mis à jour le")
                if pd.notna(maj):
                    entry["maj"] = str(maj)
                prices[key] = entry
        if not prices:
            continue
        stations.append({
            "id": int(row["id"]),
            "lat": round(float(row["lat"]), 5),
            "lon": round(float(row["lon"]), 5),
            "adresse": row["Adresse"] if pd.notna(row["Adresse"]) else "",
            "ville": row["Ville"] if pd.notna(row["Ville"]) else "",
            "cp": row["Code postal"] if pd.notna(row["Code postal"]) else "",
            "prix": prices,
        })

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {"generated_at": pd.Timestamp.now(tz="UTC").isoformat(timespec="seconds"), "stations": stations},
            f, ensure_ascii=False, separators=(",", ":"),
        )
    print(f"{len(stations)} stations écrites dans {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
