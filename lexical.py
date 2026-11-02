"""
Signal three: the phrase signal. ← STRETCH ITEM (added after unit 7's two signals)

Signal one asks how *predictable* the text is. Signal two measures its *shape*.
This one reads the text for a specific, cheap tell: the stock transition and
boilerplate phrases that assistant-style writing leans on — "it is important to
note", "furthermore", "a wide range of", "plays a crucial role", and friends.

It is deliberately different from the other two. Perplexity is a model's view of
likelihood; stylometry counts structure without reading; this one looks for
named lexical markers. A text can be predictable (high model signal) yet contain
none of these phrases, or be full of them yet structurally varied — so the three
signals can and do disagree, which is the point of having three.

    from lexical import phrase_signal
    score = phrase_signal("some text")     # 0.0 marker-free … 1.0 marker-heavy

⚠️ **Blind spot.** This signal only knows the phrases on its list. A human who
writes with transitions ("however", "for example") scores as more AI-like for
doing nothing wrong, and an AI told to avoid these phrases scores clean. Short
text has no room for markers, so it always looks human on this signal regardless
of who wrote it. Like the style signal, it measures surface, not authorship.

    python lexical.py "some text to look at"
"""

import re

# Stock phrases that assistant-style prose reaches for. Lowercased; matched as
# substrings against lowercased text so word boundaries inside them still count.
MARKER_PHRASES = [
    "it is important to note",
    "it's important to note",
    "it is worth noting",
    "it is essential",
    "it is crucial",
    "careful consideration",
    "plays a crucial role",
    "plays a vital role",
    "plays a significant role",
    "a wide range of",
    "a variety of",
    "when it comes to",
    "on the other hand",
    "as a result",
    "in conclusion",
    "to summarize",
    "in summary",
    "furthermore",
    "moreover",
    "additionally",
    "in addition",
    "consequently",
    "therefore",
    "however",
    "for instance",
    "for example",
    "overall",
    "delve into",
    "navigate the",
    "in today's world",
]

# A marker rate of this many hits per word maps to the 0.5 point. Small, because
# even marker-heavy prose only lands a few per hundred words.
_MIDPOINT_RATE = 0.012


def words(text: str) -> list[str]:
    """Lowercase word tokens, punctuation stripped. Same split as stylometry."""
    return re.findall(r"[a-z0-9']+", text.lower())


def marker_hits(text: str) -> int:
    """How many marker phrases appear, counting repeats."""
    lowered = text.lower()
    return sum(lowered.count(phrase) for phrase in MARKER_PHRASES)


def phrase_signal(text: str) -> float:
    """
    The phrase signal as a 0–1 score. Higher means more likely AI.

    Counts marker phrases, divides by the word count to get a rate that doesn't
    just reward long text, and squashes that rate onto 0–1 with
    rate / (rate + midpoint). Text with no words, or no markers, scores 0.0 —
    which this signal reads as "nothing to say", not as confidently human.

    A heuristic, not proof of authorship. The phrase list and midpoint are
    provisional and should be recalibrated against labeled text.
    """
    tokens = words(text)
    if not tokens:
        return 0.0

    rate = marker_hits(text) / len(tokens)
    score = rate / (rate + _MIDPOINT_RATE)
    return round(min(max(score, 0.0), 1.0), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "It is important to note that the system plays a crucial role. "
        "Furthermore, a wide range of factors require careful consideration. "
        "Overall, the results are, on the other hand, quite varied."
    )

    print(f"{len(words(text))} words, {marker_hits(text)} marker hits\n")
    print(f"phrase_signal   {phrase_signal(text)}   (higher = more likely AI)")
    print("\nThis is a heuristic measurement, not proof of authorship.")
