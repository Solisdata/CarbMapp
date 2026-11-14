# CarbMapp

Application Android de carte des prix des carburants en France.

## Données
`script.py` télécharge chaque jour le CSV des prix (data.gouv.fr), le nettoie
(coordonnées corrigées, prix en nombres) et écrit `data/stations.json`.
Le workflow GitHub Actions (`.github/workflows/data_pipeline.yml`) l'exécute tous les jours
à 6h UTC et commite le fichier mis à jour.

L'appli lit le fichier ici :
https://raw.githubusercontent.com/Solisdata/CarbMapp/main/data/stations.json

## Lancer en local
```
pip install -r requirements.txt
python script.py
```
