"""
Turning two numbers into one, and one number into something a person can read.
Milestone 4 combines the signals; Milestone 5 maps scores to reader-facing labels.

`combine_signals` is where your false-positive decision from Milestone 1
actually gets made. Everything above it — the labels, the appeal path — is
downstream of a number this function produced.

`score_to_label` is where you stop writing for a machine and start writing for
a person. A score of 0.62 means nothing to a writer.

⚠️ Your README's **Signals and Scoring** section has to name the file and
function holding your combining rule. The grader checks your code against what
you claim, so that line should read `scoring.py::combine_signals`.
"""

import config


def combine_signals(
    model_score: float,
    style_score: float,
    phrase_score: float | None = None,
) -> float:
    """
    Return the weighted average of the signals, all on the 0–1 scale.

    Every input points the same way: higher means more likely AI. The output
    does too.

    Args:
        model_score: from `detector.model_signal` — how predictable the text is.
        style_score: from `stylometry.style_signal` — the shape of the text.
        phrase_score: from `lexical.phrase_signal` — stock-phrase density. This
            is the STRETCH third signal; pass None to score on the two required
            signals alone.

    Returns:
        A float from 0.0 (confidently human) to 1.0 (confidently AI).

    The configured weights are 0.55 (model), 0.30 (style), and 0.15 (phrase),
    which sum to 1.0. When `phrase_score` is None the two weights are
    renormalized over themselves, which reproduces the original model-heavy
    two-signal rule (≈0.65 / 0.35). A weighted average always lands between its
    inputs, so disagreeing signals pull toward the unsure band.
    """
    scores = [model_score, style_score]
    if phrase_score is not None:
        scores.append(phrase_score)
    if any(not 0.0 <= s <= 1.0 for s in scores):
        raise ValueError("Signal scores must be between 0.0 and 1.0.")

    if phrase_score is None:
        total = config.WEIGHT_MODEL_SIGNAL + config.WEIGHT_STYLE_SIGNAL
        return (
            config.WEIGHT_MODEL_SIGNAL * model_score
            + config.WEIGHT_STYLE_SIGNAL * style_score
        ) / total

    return (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
        + config.WEIGHT_PHRASE_SIGNAL * phrase_score
    )


def score_to_label(score: float) -> tuple[str, str]:
    """
    Turn a score into a guess and the text a reader actually sees.

    Returns:
        (guess, label_text) — where `guess` is a short machine-readable string
        like "ai" / "human" / "unsure", and `label_text` is the full sentence
        shown to a person.

    Scores at or below HUMAN_THRESHOLD are human; scores at or above
    AI_THRESHOLD are AI; scores between them are unsure.
    """
    if not 0.0 <= score <= 1.0:
        raise ValueError("Score must be between 0.0 and 1.0.")

    if score >= config.AI_THRESHOLD:
        return (
            "ai",
            "This text has patterns often associated with AI-generated writing, "
            "but this result cannot prove who wrote it.",
        )
    if score <= config.HUMAN_THRESHOLD:
        return "human", "We think this was probably written by a person."
    return (
        "unsure",
        "We can't reliably tell whether this was written by a person or by AI. "
        "This result is uncertain, not proof of AI use.",
    )


def label_ranges() -> list[tuple[str, str]]:
    """
    The score range each label covers. Your README needs these beside the
    label text — given to you so the numbers can't drift apart from config.py.
    """
    return [
        ("high-confidence human", f"0.00 – {config.HUMAN_THRESHOLD:.2f} (inclusive)"),
        (
            "unsure",
            f"above {config.HUMAN_THRESHOLD:.2f} and below {config.AI_THRESHOLD:.2f}",
        ),
        ("high-confidence AI", f"{config.AI_THRESHOLD:.2f} – 1.00 (inclusive)"),
    ]
