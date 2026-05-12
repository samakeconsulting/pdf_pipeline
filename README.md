# PDF Pipeline v3

Pipeline PDF légère et robuste pour analyser les pages et générer des métriques observables.

## Installation

Installez les dépendances de production :

```bash
pip install -r requirements.txt
```

> Si vous souhaitez utiliser le notebook de démonstration, installez en plus les dépendances Jupyter séparément.

## Usage

Placez un fichier `07.pdf` dans le répertoire du projet, puis lancez :

```bash
python main.py
```

La sortie est écrite par défaut dans `output.csv`.

## Comportement

Le script traite chaque page du PDF et calcule :
- `image_ratio` : proportion de la surface de la page occupée par des images.
- `text_ratio` : proportion de la surface de la page occupée par du texte utile.
- `block_count` : nombre de blocs de texte filtrés.
- `native_score` : score de qualité du texte extrait.
- `repetition_score` : mesure la répétition du texte.
- `page_type` : classification heuristique de la page en `scan`, `native`, `hybrid` ou `complex`.
  Cette classification combine plusieurs métriques : `image_ratio`, `text_ratio`, `block_count` et `native_score`.
- `qa_valid` / `qa_flags` : validation de base sur la qualité du texte.

## Fichiers de sortie

Le pipeline génère un fichier CSV avec les colonnes suivantes :

- `page` : numéro de la page dans le document.
- `width` : largeur de la page en unités de la page PDF.
- `height` : hauteur de la page en unités de la page PDF.
- `page_area` : surface totale de la page, calculée comme `width * height`.
- `image_ratio` : proportion de la surface de la page occupée par des images.
- `image_count` : nombre de zones image détectées sur la page.
- `text_ratio` : proportion de la surface de la page occupée par du texte utile après filtrage des en-têtes et pieds de page.
- `block_count` : nombre de blocs de texte considérés comme utiles.
- `density` : densité de texte, calculée comme `block_count / page_area`.
- `native_chars` : nombre de caractères extraits du texte de la page.
- `native_words` : nombre de mots extraits du texte de la page.
- `native_score` : score heuristique évaluant la qualité du texte extrait (ratio de caractères alphabétiques, mots valides et longueur moyenne).
- `repetition_score` : score mesurant la répétition du texte sur la page ; un score élevé indique peu de répétition.
- `page_type` : classification de la page en `scan`, `native`, `hybrid` ou `complex` en combinant plusieurs métriques.
- `processing_time` : temps de traitement de la page en secondes.
- `qa_valid` : indicateur booléen indiquant si la page passe la validation de qualité.
- `qa_flags` : liste des drapeaux de qualité détectés (`short_text`, `low_score`, etc.).
- `text` : texte brut extrait de la page.

## Robustesse

Le script vérifie :
- que le fichier PDF existe,
- que le document peut être ouvert,
- que le PDF contient des pages,
- que chaque page a une surface valide avant de diviser par zéro.

Les pages invalides sont ignorées avec un avertissement et le traitement continue.

## Dépendances

Seules les dépendances nécessaires à l'exécution du pipeline sont conservées dans `requirements.txt` :
- `pymupdf`
- `pandas`

Les dépendances liées au notebook ou au développement (`jupyter`, `notebook`, `ipykernel`, `opencv-python`, `pillow`, `pytesseract`, `numpy`) sont retirées du fichier principal pour réduire les coûts d'installation et limiter les risques de conflits.

## Notebook

Le notebook `pdf_pipeline_demo.ipynb` reste disponible comme espace de démonstration et d'inspection, mais il n'est pas requis pour exécuter le pipeline principal.
