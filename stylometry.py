"""
Signal two: the style signal. ← BUILT IN MILESTONE 4

Signal one reads the text for meaning. This one measures it *as text* — the
shape of it, without understanding a word.

Three measures are implemented below. They describe sentence-length variation,
vocabulary repetition, and punctuation use; the final score combines their
normalized AI-like directions.

    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

These are only surface features. Generated prose may have more consistent
sentence lengths, but vocabulary variety and punctuation depend on the prompt,
topic, length, and editing. Their direction must be checked against labeled
examples rather than assumed.

⚠️ **The blind spot, which you have to name in Milestone 1.**

This signal cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — adding typos,
breaking up sentences, pasting in a quotation. That is a very cheap thing for
someone to do on purpose, and unit 8's attack set will do it to you.

Build each function on its own and call it from a terminal before you wire
anything together:

    python stylometry.py "some text to look at"
"""

import re
import statistics
import string


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — YOU BUILD THESE ─────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    Coefficient of variation in sentence word counts.

    Returns:
        A non-negative float. Zero means no measured variation; larger values
        mean sentence lengths vary more. A single sentence has zero spread.
    """
    lengths = [len(words(sentence)) for sentence in sentences(text)]
    if len(lengths) < 2:
        return 0.0

    mean_length = statistics.mean(lengths)
    if mean_length == 0:
        return 0.0
    return statistics.stdev(lengths) / mean_length


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words.

    Returns:
        A float between 0 and 1. Empty text returns zero; higher values mean
        more varied vocabulary.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    return len(set(tokens)) / len(tokens)


def punctuation_density(text: str) -> float:
    """
    Punctuation marks per word, counting ASCII punctuation characters.

    Returns:
        A non-negative float. Text with no words returns zero.
    """
    tokens = words(text)
    if not tokens:
        return 0.0
    punctuation_count = sum(
        1 for character in text if character in string.punctuation
    )
    return punctuation_count / len(tokens)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. Higher means more likely AI.

    Each measure is converted to an AI-like score and the three are averaged.
    Low sentence-length variation contributes a higher score. For the initial
    calibration pair, higher type-token ratio and punctuation density moved
    toward the known AI example, so those directions are used provisionally.
    Sentence variation is bounded with 1 / (1 + cv), and punctuation density
    with rate / (rate + 0.2). The type-token ratio is already between zero and
    one.

    This is a simple heuristic, not evidence of authorship. The directions
    should be recalibrated against a larger, varied set of labeled texts.
    """
    tokens = words(text)
    if not tokens:
        return 0.5

    spread = sentence_length_spread(text)
    spread_ai_score = 1.0 / (1.0 + spread)

    vocabulary_ai_score = type_token_ratio(text)

    punctuation_rate = punctuation_density(text)
    punctuation_ai_score = punctuation_rate / (punctuation_rate + 0.2)

    return round(
        (spread_ai_score + vocabulary_ai_score + punctuation_ai_score) / 3.0,
        4,
    )


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")
    print("\nThese are heuristic measurements, not proof of authorship.")
