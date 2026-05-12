def classify_page(image_ratio, text_ratio, block_count, native_score):
    """Classifie une page en combinant plusieurs métriques.

    Le type est déterminé à partir :
    - du ratio d'images,
    - du ratio de texte,
    - du nombre de blocs de texte,
    - du score de qualité du texte.
    """

    if image_ratio > 0.85 and text_ratio < 0.1:
        return "scan"

    if text_ratio > 0.25 and image_ratio < 0.2 and block_count >= 2 and native_score > 0.6:
        return "native"

    if image_ratio > 0.3 and text_ratio > 0.05:
        return "hybrid"

    if text_ratio > 0.15 and native_score > 0.5:
        return "native"

    if image_ratio > 0.1 and text_ratio > 0.02:
        return "hybrid"

    return "complex"
