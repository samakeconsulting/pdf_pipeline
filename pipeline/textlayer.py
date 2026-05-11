import string

PRINTABLE = set(string.printable)

TOP_IGNORE = 0.05
BOTTOM_IGNORE = 0.95

def clean_ratio(text):

    if not text:
        return 0

    valid = sum(c in PRINTABLE for c in text)

    return valid / len(text)

def text_blocks(page):

    return [
        b for b in page.get_text("blocks")
        if b[4].strip()
    ]

def text_coverage(page, page_area):

    useful = 0
    blocks = text_blocks(page)

    h = page.rect.height

    filtered = []

    for b in blocks:

        x0, y0, x1, y1, text, *_ = b

        if y1 < h * TOP_IGNORE:
            continue

        if y0 > h * BOTTOM_IGNORE:
            continue

        filtered.append(b)

        block_area = (x1 - x0) * (y1 - y0)

        useful += block_area * clean_ratio(text)

    return (
        min(useful / page_area, 1),
        len(filtered)
    )
