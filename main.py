import os
import sys
import time

import fitz
import pandas as pd

from pipeline.classify import classify_page
from pipeline.geometry import geometry
from pipeline.qa import qa
from pipeline.scoring import repetition_score, text_score
from pipeline.textlayer import text_coverage
from pipeline.visual import image_coverage

INPUT_PDF = "07.pdf"
OUTPUT_CSV = "output.csv"


def process_page(page, page_index):
    geo = geometry(page)
    page_area = geo.get("area", 0)

    if page_area <= 0:
        raise ValueError(
            f"Page {page_index + 1} a une surface nulle ou invalide.")

    image_ratio, image_count = image_coverage(page, page_area)
    text_ratio, block_count = text_coverage(page, page_area)
    native_text = page.get_text() or ""
    native_score = text_score(native_text)
    repetition = repetition_score(native_text)
    page_type = classify_page(image_ratio, text_ratio,
                              block_count, native_score)
    density = block_count / page_area
    quality = qa(native_text, native_score)

    return {
        "page": page_index + 1,
        "width": geo.get("width", 0),
        "height": geo.get("height", 0),
        "page_area": page_area,
        "image_ratio": image_ratio,
        "image_count": image_count,
        "text_ratio": text_ratio,
        "block_count": block_count,
        "density": density,
        "native_chars": len(native_text),
        "native_words": len(native_text.split()),
        "native_score": native_score,
        "repetition_score": repetition,
        "page_type": page_type,
        "qa_valid": quality["valid"],
        "qa_flags": quality["flags"],
        "text": native_text,
    }


def load_document(path):
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Fichier introuvable : {path}")

    try:
        document = fitz.open(path)
    except Exception as exc:
        raise RuntimeError(
            f"Impossible d'ouvrir le PDF '{path}' : {exc}") from exc

    if document.page_count == 0:
        raise RuntimeError(f"Le PDF '{path}' ne contient aucune page.")

    return document


def main():
    try:
        document = load_document(INPUT_PDF)
    except Exception as exc:
        print(f"ERREUR: {exc}", file=sys.stderr)
        sys.exit(1)

    rows = []

    for i, page in enumerate(document):
        start = time.perf_counter()

        try:
            row = process_page(page, i)
        except Exception as exc:
            print(
                f"Avertissement: impossible de traiter la page {i + 1}: {exc}",
                file=sys.stderr,
            )
            continue

        row["processing_time"] = time.perf_counter() - start
        rows.append(row)

    if not rows:
        print("Aucune page valide n'a été traitée.", file=sys.stderr)
        sys.exit(1)

    df = pd.DataFrame(rows)
    print(df.head())
    df.to_csv(OUTPUT_CSV, index=False)
    print(f"Résultat écrit dans {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
