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


def combine_signals(model_score: float, style_score: float) -> float:
    """
    Return the weighted average of the two 0–1 signals.

    Both inputs point the same way: higher means more likely AI. Your output
    should too.

    Args:
        model_score: from `detector.model_signal` — how predictable the text is.
        style_score: from `stylometry.style_signal` — the shape of the text.

    Returns:
        A float from 0.0 (confidently human) to 1.0 (confidently AI).

    The configured weights are 0.65 for the model signal and 0.35 for the
    style signal. When signals disagree, the weighted average stays between
    them; scores of 0.9 and 0.1 produce 0.62 (unsure).
    """
    if not 0.0 <= model_score <= 1.0 or not 0.0 <= style_score <= 1.0:
        raise ValueError("Signal scores must be between 0.0 and 1.0.")

    return (
        config.WEIGHT_MODEL_SIGNAL * model_score
        + config.WEIGHT_STYLE_SIGNAL * style_score
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
