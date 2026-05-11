from collections import namedtuple

Rect = namedtuple("Rect", "x0 y0 x1 y1")

MIN_IMAGE_RATIO = 0.01

def overlap(a, b):

    return not (
        a.x1 < b.x0
        or a.x0 > b.x1
        or a.y1 < b.y0
        or a.y0 > b.y1
    )

def merge(a, b):

    return Rect(
        min(a.x0, b.x0),
        min(a.y0, b.y0),
        max(a.x1, b.x1),
        max(a.y1, b.y1),
    )

def union_rects(rects):

    merged = []

    for r in rects:

        for i, m in enumerate(merged):

            if overlap(r, m):

                merged[i] = merge(r, m)

                break

        else:
            merged.append(r)

    return merged

def significant_rects(rects, page_area):

    for r in rects:

        area = (
            (r.x1 - r.x0)
            * (r.y1 - r.y0)
        )

        if area / page_area > MIN_IMAGE_RATIO:
            yield r

def image_coverage(page, page_area):

    rects = []

    for img in page.get_images(full=True):

        for r in page.get_image_rects(img[0]):

            rects.append(
                Rect(r.x0, r.y0, r.x1, r.y1)
            )

    rects = list(
        significant_rects(rects, page_area)
    )

    rects = union_rects(rects)

    total = sum(
        (r.x1 - r.x0) * (r.y1 - r.y0)
        for r in rects
    )

    return min(total / page_area, 1), len(rects)
