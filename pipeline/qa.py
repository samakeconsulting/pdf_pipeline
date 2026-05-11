def qa(text, score):

    flags = []

    if len(text) < 20:
        flags.append("short_text")

    if score < 0.65:
        flags.append("low_score")

    return {
        "valid": not flags,
        "flags": flags
    }
