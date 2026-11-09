"""
Inputs for run_eval.py.

The human and AI examples are overlapping windows from the human-authored
Darwin excerpt and AI-generated passage used during calibration. The windows
make the evaluation repeatable but are correlated, not an independent dataset.
"""


def _windows(text: str, count: int, width: int) -> list[str]:
    tokens = text.split()
    if len(tokens) <= width:
        return [text]
    last_start = len(tokens) - width
    starts = [round(last_start * i / (count - 1)) for i in range(count)]
    return [" ".join(tokens[start:start + width]) for start in starts]


HUMAN_SOURCE = (
    "When on board H.M.S. 'Beagle,' as naturalist, I was much struck with certain "
    "facts in the distribution of the inhabitants of South America, and in the "
    "geological relations of the present to the past inhabitants of that continent. "
    "These facts seemed to me to throw some light on the origin of species—that "
    "mystery of mysteries, as it has been called by one of our greatest philosophers. "
    "On my return home, it occurred to me, in 1837, that something might perhaps be "
    "made out on this question by patiently accumulating and reflecting on all sorts "
    "of facts which could possibly have any bearing on it. After five years' work I "
    "allowed myself to speculate on the subject, and drew up some short notes; these "
    "I enlarged in 1844 into a sketch of the conclusions, which then seemed to me "
    "probable: from that period to the present day I have steadily pursued the same "
    "object. I hope that I may be excused for entering on these personal details, as "
    "I give them to show that I have not been hasty in coming to a decision."
)

AI_SOURCE = (
    "Scientific inquiry represents one of the most valuable and transformative "
    "pursuits in human history. By carefully observing the natural world, documenting "
    "meaningful patterns, and evaluating evidence in a systematic manner, researchers "
    "can develop a deeper understanding of the complex processes that shape biological "
    "diversity. This process is not simply about collecting isolated facts; rather, "
    "it involves transforming observations into coherent explanations that can be "
    "evaluated, refined, and communicated to others. In this way, thoughtful research "
    "establishes a foundation for continued discovery and intellectual progress. "
    "Moreover, the importance of scientific investigation extends beyond the "
    "immediate acquisition of knowledge. A rigorous approach encourages curiosity, "
    "supports critical thinking, and promotes informed decisions in an increasingly "
    "interconnected world. When scientists acknowledge uncertainty, consider "
    "alternative explanations, and remain open to revising their conclusions, they "
    "strengthen the overall reliability of their work. Ultimately, the pursuit of "
    "knowledge is both an individual responsibility and a collective endeavor. By "
    "embracing evidence-based reasoning and sustained collaboration, society can "
    "continue to expand its understanding of nature while building a more informed "
    "and resilient future."
)

HUMAN_EXAMPLES = _windows(HUMAN_SOURCE, count=10, width=40)
AI_EXAMPLES = _windows(AI_SOURCE, count=5, width=40)

# Ten short first-person human-style passages for the false-positive criterion.
# Everyday writing — varied sentence length, specific detail, the odd aside —
# the kind of thing a real writing-site user submits.
OWN_WRITING = [
    "I finally got around to fixing the back fence this weekend. Took way longer "
    "than it should have because I kept running out to the hardware store for "
    "one more bracket. By Sunday night my hands were wrecked but the gate "
    "actually closes now, which it hasn't done since we moved in.",

    "Honestly the movie was fine? Not great. The first hour dragged and I almost "
    "fell asleep, but the ending pulled it together enough that I didn't regret "
    "going. My sister loved it, so maybe it's just me.",

    "We tried the new ramen place on 4th. The broth was rich, almost too salty "
    "for me, but the noodles had a good chew and the egg was perfect. I'd go "
    "back, probably on a cold day when I actually want something that heavy.",

    "I've been trying to run three times a week and it is not going well. Monday "
    "I managed two miles. Wednesday it rained so I skipped it and told myself I'd "
    "double up Friday, which, of course, I did not. Next week.",

    "My grandmother used to keep hard candy in a blue tin on the counter, and "
    "every time I smell butterscotch I'm eight years old again in her kitchen "
    "waiting for the kettle. Funny how a smell does that and a photograph "
    "doesn't.",

    "The meeting could have been an email. We spent forty minutes on a decision "
    "that three people had already made in the hallway beforehand. I did get a "
    "free coffee out of it, so there's that.",

    "I planted tomatoes too early this year and the frost got half of them. The "
    "survivors are doing okay, a little leggy, leaning toward the window like "
    "they're trying to escape. I'll stake them this weekend if I remember.",

    "Writing has never come easy to me. I stare at the blank page, type a "
    "sentence, delete it, type it again slightly different. Eventually something "
    "sticks and I can build off it, but those first few minutes are miserable "
    "every single time.",

    "The dog figured out how to open the pantry door. We came home to kibble "
    "everywhere and one very guilty-looking retriever who would not make eye "
    "contact. We've since added a latch. He is already studying the latch.",

    "I don't have a strong opinion on the new logo. It's blue now instead of "
    "green. People online are furious about it, which feels like a lot of energy "
    "to spend on a logo, but then again I spent ten minutes reading the comments, "
    "so who am I to judge.",
]
MAX_LENGTH_TEXT = "word " * 1999 + "word!"
OVER_MAX_LENGTH_TEXT = "word " * 1999 + "word!!"

SCENARIOS = [
    {
        "name": "human-authored writing samples",
        "criterion": 1,
        "texts": OWN_WRITING,
    },
    {
        "name": "human examples for score spread",
        "criterion": 2,
        "texts": HUMAN_EXAMPLES[:5],
    },
    {
        "name": "AI-generated examples for score spread",
        "criterion": 2,
        "texts": AI_EXAMPLES,
    },
    {
        "name": "label coverage examples",
        "criterion": 3,
        "texts": [
            HUMAN_SOURCE,
            AI_SOURCE,
            "The meeting may have been useful, but I'm not sure yet. "
            "I need to think about what we discussed before deciding.",
        ],
    },
    {
        "name": "bad input and length boundary",
        "criterion": 5,
        "bodies": [
            {"creator_id": "eval_missing_text"},
            {"text": "", "creator_id": "eval_empty_text"},
            {"text": "   ", "creator_id": "eval_whitespace_text"},
            {"text": MAX_LENGTH_TEXT, "creator_id": "eval_max_length"},
            {"text": OVER_MAX_LENGTH_TEXT, "creator_id": "eval_over_max_length"},
        ],
    },
]


def validate() -> list[str]:
    """Validate scenario definitions before run_eval sends requests."""
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")
        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                "bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(f"scenario {i}, body {j} is not a dict")
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not isinstance(text, str) or not text.strip():
                problems.append(f"scenario {i}, text {j} is empty or not a string")
    return problems
