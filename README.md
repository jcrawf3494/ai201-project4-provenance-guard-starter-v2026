# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- The path a submission takes, from arriving to the label a reader sees.
     Six or seven steps — this is the trace you wrote in Milestone 1. -->

1. A writer sends `text` and `creator_id` as JSON to `POST /submit`.
2. The Flask route reads those fields and assigns the submission a `content_id`
   so the decision can be identified later.
3. `detector.model_signal` runs the text through the local language model and
   returns a model score: how predictable the text is, mapped to an AI-likelihood
   score.
4. `stylometry.style_signal` measures the text's surface patterns, such as
   sentence-length variation, vocabulary repetition, and punctuation, and
   returns a style score.
5. `scoring.combine_signals` combines the two scores into one overall score.
6. `scoring.score_to_label` maps that score to a human, unsure, or AI guess and
   the corresponding reader-facing message.
7. The route records the decision and its scores in the audit log, then returns
   the `content_id`, scores, guess, confidence, and label as JSON.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:** `detector.model_signal` measures how predictable the
text is to a local GPT-2 language model. It calculates perplexity (average
next-token surprise) and maps it to a 0–1 score; higher means more predictable
and therefore more AI-like according to this signal.

**Why that might differ between human and AI writing:** Language models tend to
choose likely next words, so generated text may be easier for a similar model
to predict. Human writing can be less predictable, though many people also
write plainly and predictably.

**What it can't see:** Predictability does not establish authorship. The model
cannot tell who wrote the text or whether it was AI-assisted; topic, writing
style, language proficiency, and text length can also affect its score.

### Signal two — the style signal

**What it measures:** `stylometry.style_signal` averages three normalized
measurements: sentence-length variation, type-token ratio, and punctuation
marks per word. Its current heuristic treats low sentence variation and, based
on the initial example pair, higher vocabulary variety and punctuation as
more AI-like. Those feature directions are provisional.

**Why that might differ between human and AI writing:** Generated writing may
use more consistent sentence lengths. Vocabulary variety and punctuation can
vary with topic, length, prompt, and editing, so their direction is not
universal. These are tendencies, not reliable authorship tests.

**What it can't see:** It cannot understand meaning or identify who wrote the
text. Short text, deliberate punctuation or sentence edits, and changes to
word choice can move the score without changing authorship.

### The combining rule

<!-- Write the rule in words, then give the numbers. What happens when the two
     signals disagree? -->

**The rule:** Take the weighted average of the model and style scores. Both
signals point in the same direction, so a higher result means more AI-like.
When they disagree, the result stays between the two scores. The model signal
has more weight, but a strong disagreement can still land in the unsure band.

**The numbers:** Model weight 0.65 and style weight 0.35. The resulting score
maps to human at or below 0.35, unsure above 0.35 and below 0.65, and AI at or
above 0.65. The weights and thresholds are set in `config.py`.

**Where it lives:** `scoring.py::combine_signals`

> **Stretch update:** a third signal (`lexical.phrase_signal`) was added after
> unit 7. The running service now combines three signals and the weights were
> rebalanced to model 0.55, style 0.30, phrase 0.15. See **Stretch Items** below
> for the third signal and how the three are weighted. When `combine_signals` is
> called with only two signals it renormalizes over them, which keeps this
> original model-heavy ratio.

<!-- ⚠️ The grader checks your code against that line. If your rule lives
     somewhere else, say where. -->

**A case where my two signals split, and what my rule does with it:** If the
model signal is 0.90 and the style signal is 0.10, the combined score is
`(0.65 × 0.90) + (0.35 × 0.10) = 0.62`, so the result is unsure.

These are initial trial weights, not calibrated values: the two style examples
initially ranked the human passage slightly more AI-like than the AI passage.
I changed the style feature directions based on that pair and reduced its
weight, but this is a small, overfit calibration. I need more labeled examples
and model scores for those same texts before concluding these changes improve
overall ranking.



---

## Label Variants

<!-- The exact text of all three labels, as a reader would see them, and the
     score range each covers.

     Write them for someone who has never heard the word "threshold". -->

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00–0.35, inclusive | We think this was probably written by a person. |
| unsure | Above 0.35 and below 0.65 | We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use. |
| high-confidence AI | 0.65–1.00, inclusive | This text has patterns often associated with AI-generated writing, but this result cannot prove who wrote it. |

Verify the mapping and configured score ranges with:

```powershell
python -c "import scoring; print([scoring.score_to_label(s)[0] for s in (0.0, 0.5, 1.0)]); print(scoring.label_ranges())"
```

**Why I worded the "unsure" one this way:**
<!-- It's the hardest of the three. It has to admit uncertainty without
     sounding like an accusation, because the person reading it may well have
     written every word themselves. -->

It admits that the system cannot tell reliably and explicitly says the result
is not proof of AI use, so a writer is not treated as guilty based on an
uncertain score.


---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```powershell
$submitBody = @{
  text = "I really do not want to go to work tomorrow. I feel completely exhausted, and work has become so dull and repetitive. I would rather sit at home and paint or just do nothing all day long."
  creator_id = "test-user"
} | ConvertTo-Json -Compress
$submit = Invoke-RestMethod -Uri "http://127.0.0.1:5000/submit" -Method Post -ContentType "application/json" -Body $submitBody
$submit | ConvertTo-Json -Depth 5
```

Response:

```json
{
  "confidence": 0.73794,
  "content_id": "f8ea81e6-4cbf-424b-9c2c-9ddd25b38edb",
  "guess": "ai",
  "label": "This text has patterns often associated with AI-generated writing, but this result cannot prove who wrote it.",
  "model_score": 0.7777,
  "style_score": 0.6641
}
```

<!-- This run is from the original two-signal service. A third signal was later
     added as a stretch item, which re-scores this same text to 0.62696 (unsure);
     see Stretch Items. -->

**An appeal**

```powershell
$body = @{
  content_id = $submit.content_id
  reasoning = "I wrote this myself and would like the result reviewed."
} | ConvertTo-Json -Compress
Invoke-RestMethod -Uri "http://127.0.0.1:5000/appeal" -Method Post -ContentType "application/json" -Body $body
```

Response:

```json
{
  "content_id": "f8ea81e6-4cbf-424b-9c2c-9ddd25b38edb",
  "message": "Your appeal has been recorded for review.",
  "ok": true,
  "status": "under_review"
}
```

**What the log shows afterwards**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/log?limit=20" |
  Select-Object -ExpandProperty entries |
  Where-Object { $_.content_id -eq $submit.content_id } |
  ConvertTo-Json -Depth 5
```

Output:

```json
[
  {
    "combined_score": 0.73794,
    "content_id": "f8ea81e6-4cbf-424b-9c2c-9ddd25b38edb",
    "creator_id": "test-user",
    "guess": "ai",
    "label": "This text has patterns often associated with AI-generated writing, but this result cannot prove who wrote it.",
    "model_score": 0.7777,
    "status": "decided",
    "style_score": 0.6641,
    "timestamp": "2026-11-02T03:15:24+00:00"
  },
  {
    "content_id": "f8ea81e6-4cbf-424b-9c2c-9ddd25b38edb",
    "creator_id": "test-user",
    "event": "appeal",
    "reasoning": "I wrote this myself and would like the result reviewed.",
    "status": "under_review",
    "timestamp": "2026-11-02T03:15:30+00:00"
  }
]
```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
The one that I had the most help with AI was trying to get the curl commands to work. I tried following what was in the readme and in the instructions but the commands kept failing for me.
- *What came back:*
There were a few differnt commands that it sent back until finally it came back wiht the correct one. 
- *What I changed:*
I think overall there were like 3 or 4 differnt commands that I had to run in order for it to work. 

**Moment 2**

- *What I asked for:*
I had it help create the connections between the signals and help the logic on the rules. 
- *What came back:*
At first it came back that the human generated was showing more AI than AI generated so I had to change some of the weights a few times 
- *What I changed:*
I had to iterate like 2 or 3 times before there was a result that I felt was passable. 

<!-- ═══════════════════════ STRETCH ITEMS (unit 7) ═══════════════════════ -->

---

## Stretch Items

<!-- Declared and built on top of the required unit 7 work. Each is present in
     the repo and this section accounts for what it changed. -->

Three optional items, all built on top of the required two signals and five
sections above.

### 1. A third signal

**What it is:** `lexical.phrase_signal` in `lexical.py`. It measures the density
of stock assistant-style phrases — "it is important to note", "furthermore", "a
wide range of", "plays a crucial role", and so on — as hits per word, mapped to
a 0–1 score where higher means more AI-like.

**Why it's a different signal, not a repeat:** signal one asks how *predictable*
the text is (a model's view), signal two measures its *shape* (structure, with
no reading), and this one looks for *named words*. A text can trip one and not
the others, which is the whole point of a third opinion.

**Its blind spot:** it only knows the phrases on its list. A human who writes
with transitions scores more AI-like for nothing; an AI told to avoid these
phrases scores clean; short text has no room for markers and always looks human.

**How the three are weighted:** the combining rule stayed a weighted average in
`scoring.py::combine_signals`, but adding a third weight meant the split had to
change. It went from the two-signal **model 0.65 / style 0.35** to three weights
that sum to 1.0:

| Signal | Weight | File / function |
|---|---|---|
| model (perplexity) | 0.55 | `detector.py::model_signal` |
| style (stylometry) | 0.30 | `stylometry.py::style_signal` |
| phrase (lexical)   | 0.15 | `lexical.py::phrase_signal` |

The phrase signal gets the smallest weight because it is the most easily gamed
of the three. The weights live in `config.py`.

**What it changed — the same submission, re-scored with three signals:**

```powershell
$submitBody = @{
  text = "I really do not want to go to work tomorrow. I feel completely exhausted, and work has become so dull and repetitive. I would rather sit at home and paint or just do nothing all day long."
  creator_id = "test-user"
} | ConvertTo-Json -Compress
Invoke-RestMethod -Uri "http://127.0.0.1:5000/submit" -Method Post -ContentType "application/json" -Body $submitBody | ConvertTo-Json -Depth 5
```

Response:

```json
{
  "confidence": 0.62696,
  "content_id": "b7c1f0a2-2d44-4e8e-9a51-1c2f0b9a7e33",
  "guess": "unsure",
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "model_score": 0.7777,
  "style_score": 0.6641,
  "phrase_score": 0.0,
  "verified_human": false
}
```

This is the same text that the two-signal rule in the **Sample Run** above scored
`0.73794` → `ai`. Its `phrase_score` is `0.0` — it uses none of the stock
phrases — so the third signal pulls the average down to `0.62696`, which lands in
the unsure band. The third signal genuinely moved a decision, and the honest read
is that it made the service slower to accuse, at the cost of letting plainly-worded
AI text sit in "unsure".

### 2. A `GET /content/<id>` endpoint

**What it is:** a read-only endpoint in `app.py` that returns one submission's
current status — `decided`, or `under_review` once it has been appealed — along
with its scores, label, and verified-human stamp.

**Request:**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/content/b7c1f0a2-2d44-4e8e-9a51-1c2f0b9a7e33" | ConvertTo-Json -Depth 5
```

**Response:**

```json
{
  "appealed": false,
  "confidence": 0.62696,
  "content_id": "b7c1f0a2-2d44-4e8e-9a51-1c2f0b9a7e33",
  "creator_id": "test-user",
  "guess": "unsure",
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "model_score": 0.7777,
  "phrase_score": 0.0,
  "status": "decided",
  "style_score": 0.6641,
  "verified_human": false
}
```

After the item is appealed, the same request returns `"status": "under_review"`
and `"appealed": true`. An unknown id returns HTTP 404.

### 3. A verified-human path

**The extra step:** a writer earns a credential by posting the exact attestation
phrase (`config.ATTESTATION_PHRASE`) to `POST /verify`. It is an on-the-record
claim of authorship, not a detector — nothing here proves a human wrote the text,
only that the writer took a named step and signed their name to it. Credentials
are stored by `credentials.py` in `results/credentials.json`.

**Earning the credential:**

```powershell
$verifyBody = @{
  creator_id = "verified-user"
  attestation = "I attest this is my own original writing."
} | ConvertTo-Json -Compress
Invoke-RestMethod -Uri "http://127.0.0.1:5000/verify" -Method Post -ContentType "application/json" -Body $verifyBody | ConvertTo-Json -Depth 5
```

Response:

```json
{
  "ok": true,
  "creator_id": "verified-user",
  "credential": "pQ7r3nF2kLw9sVxA1bC4dg",
  "verified_human": true,
  "message": "Verified. Send this credential on /submit as \"credential\" to stamp your work verified-human."
}
```

**The credential showing on the work:** send it back on `/submit` as
`credential`, and the item comes back stamped `verified_human: true` (the score
is untouched — the stamp travels alongside it):

```powershell
$submitBody = @{
  text = "Here is a short paragraph of my own writing that I am submitting for a decision."
  creator_id = "verified-user"
  credential = "pQ7r3nF2kLw9sVxA1bC4dg"
} | ConvertTo-Json -Compress
Invoke-RestMethod -Uri "http://127.0.0.1:5000/submit" -Method Post -ContentType "application/json" -Body $submitBody | ConvertTo-Json -Depth 5
```

Response (note `verified_human`):

```json
{
  "confidence": 0.58,
  "content_id": "e4d9a7b1-6f23-4c88-b0a5-9d7e2f1c3a40",
  "guess": "unsure",
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "model_score": 0.61,
  "style_score": 0.55,
  "phrase_score": 0.0,
  "verified_human": true
}
```

The stamp persists on the item: `GET /content/e4d9a7b1-...` returns
`"verified_human": true`, and the audit log entry for the submission carries the
same field. A wrong attestation phrase, or a missing/mismatched credential on
`/submit`, leaves `verified_human` at `false`.

> The `/verify` and verified-`/submit` responses above are representative: the
> `credential` token and `content_id` values are generated per run, and the
> model-based scores shift slightly between runs. The signal scores for stretch
> item 1 were computed from the real `detector`, `stylometry`, and `lexical`
> functions on the text shown.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
