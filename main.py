import time
import fitz
import pandas as pd

from pipeline.geometry import geometry
from pipeline.visual import image_coverage
from pipeline.textlayer import text_coverage
from pipeline.classify import classify_page
from pipeline.scoring import (
    text_score,
    repetition_score
)
from pipeline.qa import qa

doc = fitz.open("07.pdf")

rows = []

for i, page in enumerate(doc):

    start = time.perf_counter()

    geo = geometry(page)

    image_ratio, image_count = image_coverage(
        page,
        geo["area"]
    )

    text_ratio, block_count = text_coverage(
        page,
        geo["area"]
    )

    native_text = page.get_text()

    native_score = text_score(native_text)

    repetition = repetition_score(native_text)

    page_type = classify_page(
        image_ratio,
        text_ratio
    )

    density = (
        block_count / geo["area"]
    )

    quality = qa(
        native_text,
        native_score
    )

    elapsed = (
        time.perf_counter() - start
    )

    rows.append({

        "page": i + 1,

        "width": geo["width"],
        "height": geo["height"],
        "page_area": geo["area"],

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

        "processing_time": elapsed,

        "qa_valid": quality["valid"],
        "qa_flags": quality["flags"],

        "text": native_text
    })

df = pd.DataFrame(rows)

print(df.head())

df.to_csv("output.csv", index=False)
