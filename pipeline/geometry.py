MAX_AREA = 25_000_000

def geometry(page):

    rect = page.rect

    return {
        "width": rect.width,
        "height": rect.height,
        "area": rect.width * rect.height
    }
