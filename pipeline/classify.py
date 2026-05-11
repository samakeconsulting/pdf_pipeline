def classify_page(image_ratio, text_ratio):

    if image_ratio > 0.85:
        return "scan"

    if text_ratio > 0.25 and image_ratio < 0.2:
        return "native"

    if image_ratio > 0.3 and text_ratio > 0.05:
        return "hybrid"

    return "complex"
