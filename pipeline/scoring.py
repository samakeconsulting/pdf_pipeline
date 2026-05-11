import re
from collections import Counter

def repetition_score(text):

    chars = Counter(text)

    top = chars.most_common(1)

    if not top:
        return 1

    return 1 - (top[0][1] / len(text))

def text_score(text):

    words = text.split()

    if not words:
        return 0

    alpha = sum(
        c.isalpha()
        for c in text
    )

    alpha_ratio = alpha / max(len(text), 1)

    valid_words = sum(
        bool(re.search(r"[A-Za-zÀ-ÿ]", w))
        for w in words
    )

    word_ratio = valid_words / len(words)

    avg_len = sum(map(len, words)) / len(words)

    size_score = min(avg_len / 5, 1)

    base_score = (
        alpha_ratio * 0.4
        + word_ratio * 0.4
        + size_score * 0.2
    )

    return (
        base_score * 0.8
        + repetition_score(text) * 0.2
    )
