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

**Moment 3 (unit 8)**

- *What I asked for:*
I used AI to help run the attack set against my service and interpret the outcomes.
- *What came back:*
It helped me work through which attacks held and which broke, and what the results meant across the families.
- *What I changed:*
I used that to mark the verdicts and write up the run.

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

**My limits:** **15** per minute, **225** per day

**Why those numbers and not others:** A real writer submitting their own work
posts a handful of times an hour — well under 15 in any single minute, and
nowhere near 225 in a day. A script mapping my thresholds sends hundreds of
variations in a burst and trips 15/minute almost immediately. I set the daily cap
at 225 (≈ 15 × 15) so a genuinely heavy but human day of editing and resubmitting
still fits, while a steady automated drip that stays under the per-minute limit
still can't run all day. The two limits cover the two shapes of abuse: 15/minute
stops a burst, 225/day stops a slow grind.

**What a caller counts as:** per `creator_id`, not per IP address
(`app.py::rate_limit_key`), falling back to the address only when no usable
creator_id is present. That choice and its trade-off — it catches one identity
abusing the service from several addresses, but is evaded by rotating creator_ids,
which per-address limiting would have caught — is written up under **Unit 8
Stretch Items → Per-creator rate limiting**.

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 20 -->

NOTES Changed 15 to 20 since my limit was 15 
(.venv) PS C:\Users\Josh\ai201-project4-provenance-guard-starter-v2026> python run_attacks.py --flood 20                                                              
20 submissions as 'flood_tester' against http://127.0.0.1:5000
The first one is slow while the model loads.

  [ 1/20] 200
  [ 2/20] 200
  [ 3/20] 200
  [ 4/20] 200
  [ 5/20] 200
  [ 6/20] 200
  [ 7/20] 200
  [ 8/20] 200
  [ 9/20] 200
  [10/20] 200
  [11/20] 200
  [12/20] 200
  [13/20] 200
  [14/20] 200
  [15/20] 200
  [16/20] 429
  [17/20] 429
  [18/20] 429
  [19/20] 429
  [20/20] 429

============================================================
200 200 200 200 200 200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
============================================================

The first 15 submissions from `flood_tester` return `200`; the 16th onward return
`429`, which is the per-minute limit (15) doing its job. Each rejection is also
written to the audit log as an `event: rejected`, `reason: rate_limited` entry —
one of those appears in the ten audit entries below.

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

Full run: 56 attacks sent to `POST /submit`, produced by `run_attacks.py::main`
(report `results/attack_run_2026-11-09_0058.md`), service `app.py::submit`.
No attack returned a 5xx or crashed, so nothing is auto-marked BROKE; the
verdicts below are mine.

**How I marked held vs broke.** The script can only call the unambiguous case
(a 5xx or a crash is BROKE). Everything else depends on what each family was
going for, so I used one rule per family:

- **evasion** — AI-leaning text trying to be *cleared as human*. **BROKE** only
  if it earned a confident `human` label; landing in `unsure` is **HELD**,
  because the service refused to clear it.
- **false_positive** — genuine human writing. **BROKE** if it was labelled
  `ai` (a real writer accused); `unsure` or `human` is **HELD**.
- **prompt_injection** — **BROKE** if the injected instruction changed control
  flow, altered the label text, or corrupted a log entry. Scored as ordinary
  text is **HELD**.
- **malformed** — **BROKE** on a 5xx or crash. A clean `400`/`413`, or a sane
  `200`, is **HELD**.
- **flood_same_creator** — **BROKE** if it got through when it should have been
  limited. Rejected, or legitimately under the limit, is **HELD**.

**Count: 54 HELD / 2 BROKE of 56.** Both breaks are in `false_positive`.

| Family | Attacks | Held | Broke |
|---|---|---|---|
| evasion | 10 | 10 | 0 |
| false_positive | 8 | 6 | **2** |
| prompt_injection | 6 | 6 | 0 |
| malformed | 20 | 20 | 0 |
| flood_same_creator | 12 | 12 | 0 |
| **Total** | **56** | **54** | **2** |

Every input with its outcome:

| ID | Family | Targeting | Status | Guess | Score | Verdict |
|---|---|---|---|---|---|---|
| EV01 | evasion | typos raise word variety | 200 | unsure | 0.377 | HELD (weak — score near the 0.35 human line; model signal fell to 0.16) |
| EV02 | evasion | broken-up sentences raise length spread | 200 | unsure | 0.579 | HELD |
| EV03 | evasion | pasted quotation changes the shape | 200 | unsure | 0.634 | HELD |
| EV04 | evasion | unusual words raise perplexity | 200 | unsure | 0.624 | HELD |
| EV05 | evasion | heavy human editing pass | 200 | unsure | 0.357 | HELD (weak — 0.007 above the human line) |
| EV06 | evasion | one very long + one very short sentence | 200 | unsure | 0.537 | HELD |
| EV07 | evasion | padding with punctuation | 200 | ai | 0.681 | HELD (caught) |
| EV08 | evasion | text below the token window | 200 | unsure | 0.363 | HELD (weak) |
| EV09 | evasion | AI text with a human opening bolted on | 200 | ai | 0.651 | HELD (caught) |
| EV10 | evasion | repeated stanza structure | 200 | ai | 0.658 | HELD (caught) |
| FP01 | false_positive | plain, clear human writing | 200 | unsure | 0.512 | HELD (not cleared) |
| FP02 | false_positive | human writing, formal register | 200 | unsure | 0.592 | HELD (not cleared) |
| FP03 | false_positive | non-native speaker writing carefully | 200 | unsure | 0.620 | HELD (not cleared) |
| FP04 | false_positive | student essay to a rubric | 200 | ai | 0.735 | **BROKE — real student labelled AI** |
| FP05 | false_positive | human-written technical docs | 200 | unsure | 0.616 | HELD (not cleared) |
| FP06 | false_positive | person imitating a formal template | 200 | ai | 0.659 | **BROKE — human labelled AI** |
| FP07 | false_positive | human repeating a phrase deliberately | 200 | unsure | 0.632 | HELD (not cleared) |
| FP08 | false_positive | very short genuine human submission | 200 | unsure | 0.412 | HELD (not cleared) |
| PI01 | prompt_injection | "ignore the check" | 200 | unsure | 0.444 | HELD (scored as text) |
| PI02 | prompt_injection | instruction disguised as system message | 200 | human | 0.321 | HELD (scored as text) |
| PI03 | prompt_injection | instruction in the writer's voice | 200 | unsure | 0.531 | HELD |
| PI04 | prompt_injection | make the label text hostile | 200 | unsure | 0.495 | HELD (label text unchanged) |
| PI05 | prompt_injection | inject into the audit log | 200 | unsure | 0.594 | HELD (log entry clean) |
| PI06 | prompt_injection | instruction plus real human text | 200 | unsure | 0.480 | HELD |
| MF01 | malformed | text is only whitespace | 400 | — | — | HELD (rejected `invalid_text`) |
| MF02 | malformed | text is a single character | 400 | — | — | HELD (rejected `text_cannot_be_scored`) |
| MF03 | malformed | text is control characters | 200 | human | 0.277 | HELD (no crash) |
| MF04 | malformed | text is only punctuation | 200 | human | 0.156 | HELD (no crash) |
| MF05 | malformed | one very long single word | 200 | ai | 0.749 | HELD (no crash; but garbage scored confident-AI) |
| MF06 | malformed | emoji only | 200 | ai | 0.698 | HELD (no crash; garbage scored confident-AI) |
| MF07 | malformed | right-to-left script | 200 | unsure | 0.649 | HELD (no crash) |
| MF08 | malformed | 60,000 characters | 413 | — | — | HELD (rejected `text_too_long`) |
| RQ01 | malformed | no text field | 400 | — | — | HELD |
| RQ02 | malformed | no creator_id | 400 | — | — | HELD (logged as `unknown`) |
| RQ03 | malformed | text is a number | 400 | — | — | HELD |
| RQ04 | malformed | text is a list | 400 | — | — | HELD |
| RQ05 | malformed | text is null | 400 | — | — | HELD |
| RQ06 | malformed | creator_id is an object | 400 | — | — | HELD (logged as `unknown`) |
| RQ07 | malformed | body is a JSON array | 400 | — | — | HELD |
| RQ08 | malformed | body is unparseable JSON | 400 | — | — | HELD |
| RQ09 | malformed | body is empty | 400 | — | — | HELD |
| RQ10 | malformed | body is form-encoded | 400 | — | — | HELD |
| RQ11 | malformed | JSON claiming to be plain text | 400 | — | — | HELD |
| RQ12 | malformed | deeply nested JSON | 400 | — | — | HELD |
| FL01_01–12 | flood_same_creator | 12 rapid submissions, one creator | 200 ×12 | human | 0.251 | HELD (all under the 15/min limit — see note) |

**On the two breaks.** Both are genuine human writing that the service called
`ai`: FP04 (a student essay written to a rubric, 0.735) and FP06 (a person
imitating a formal template, 0.659). Looking across the whole `false_positive`
family, the more alarming pattern is that **not one of the eight real-human
texts was ever labelled `human`** — six landed `unsure`, two landed `ai`. The
service never confidently cleared a real writer. That is the Milestone-1
false-positive decision showing its cost, and it points straight at Criterion 1.

**On the flood family.** The attack set's `flood_same_creator` family is 12
rows sharing one `creator_id`, and my per-creator limit is 15/minute — so all
12 legitimately pass, and this run shows no `429`. That is the limiter working,
not failing: it would have rejected the 16th. The actual proof that limiting
rejects a burst is the Milestone-1 flood of 20 (15 × `200` then 5 × `429`),
pasted under **Rate Limiting** above and included as a rejection entry below.

**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

Pulled with `curl "http://127.0.0.1:5000/log?limit=200"` from `logs/audit.jsonl`
(written by `audit.py::log_decision` / `log_rejection`). Chosen for what they
show — the two false accusations, the near-miss evasion, a signal disagreement,
garbage scored as confident AI, an injection that did nothing, and three
rejection records including a rate-limit `429`.

```json
{"timestamp": "2026-11-09T05:58:17+00:00", "content_id": "e4a324b7-c62e-4445-b59f-69dcf5c9919d", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.6463, "combined_score": 0.7345900000000001, "label": "This text has patterns often associated with AI-generated writing, but this result cannot prove who wrote it.", "status": "decided", "phrase_score": 0.5507, "verified_human": false}
{"timestamp": "2026-11-09T05:58:19+00:00", "content_id": "dc70efdc-ed03-4b8d-bf28-efb1f1e24c15", "creator_id": "attacker_FP06", "guess": "ai", "model_score": 0.8814, "style_score": 0.5821, "combined_score": 0.6594, "label": "This text has patterns often associated with AI-generated writing, but this result cannot prove who wrote it.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-09T05:58:11+00:00", "content_id": "9680b50e-e65c-4c7b-9081-a2447528ad08", "creator_id": "attacker_EV01", "guess": "unsure", "model_score": 0.1635, "style_score": 0.7083, "combined_score": 0.37666499999999997, "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.", "status": "decided", "phrase_score": 0.495, "verified_human": false}
{"timestamp": "2026-11-09T05:58:15+00:00", "content_id": "0e1796f6-a71e-4b76-85a5-c04edc103464", "creator_id": "attacker_EV10", "guess": "ai", "model_score": 0.9792, "style_score": 0.3997, "combined_score": 0.65847, "label": "This text has patterns often associated with AI-generated writing, but this result cannot prove who wrote it.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-09T05:58:32+00:00", "content_id": "ac96bd39-6309-4c43-973c-b04934eff258", "creator_id": "attacker_MF05", "guess": "ai", "model_score": 0.9976, "style_score": 0.6667, "combined_score": 0.7486900000000001, "label": "This text has patterns often associated with AI-generated writing, but this result cannot prove who wrote it.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-09T05:58:36+00:00", "content_id": "ab7c28e7-7345-4258-92d1-a44478b6c8b1", "creator_id": "attacker_MF06", "guess": "ai", "model_score": 0.9969, "style_score": 0.5, "combined_score": 0.6982950000000001, "label": "This text has patterns often associated with AI-generated writing, but this result cannot prove who wrote it.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-09T05:58:25+00:00", "content_id": "e0326e0d-61a7-45c8-9dc1-a75e54832382", "creator_id": "attacker_PI05", "guess": "unsure", "model_score": 0.6401, "style_score": 0.8052, "combined_score": 0.593615, "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-09T05:58:26+00:00", "creator_id": "attacker_MF01", "event": "rejected", "status": "rejected", "reason": "invalid_text"}
{"timestamp": "2026-11-09T05:58:42+00:00", "creator_id": "attacker_MF08", "event": "rejected", "status": "rejected", "reason": "text_too_long", "text_length": 57640, "max_characters": 10000}
{"timestamp": "2026-11-04T23:23:33+00:00", "creator_id": "flood_tester", "event": "rejected", "status": "rejected", "reason": "rate_limited", "limit": "15 per 1 minute"}
```

What these show, in order: **FP04 / FP06** — the two genuine-human texts the
service accused (`ai`); **EV01** — an evasion that dragged the model signal down
to `0.16` with typos and landed `0.377`, a hair above the human line, the
closest any evasion came to being cleared; **EV10** — the signals flatly
disagreed (model `0.98`, style `0.40`) and the combining rule still returned
`ai`; **MF05 / MF06** — a single long junk word and an emoji-only string, both
scored confident `ai` on the model signal alone, which is the model over-reacting
to odd tokenisation rather than any real detection; **PI05** — an attempt to
inject into the audit log, which the service wrote as an ordinary, well-formed
decision entry with no injected content, because text is only ever data here;
**MF01 / MF08** — graceful rejections (empty text, oversized text) that log the
reason and write no decision; and **the `429`** — the rate limiter rejecting the
16th-plus submission in the Milestone-1 flood, recorded as a rejection with its
limit, so the attack that shows up only as an absence still leaves a trace.

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:

**FP04 — a student essay written to a rubric, labelled `ai` at 0.735.** This is
the worst because it is the most realistic and the most consequential: a real
student, writing to the structure a rubric asked for, gets the high-confidence
AI label on a site where that label can trigger an academic-integrity process.
The rubric is what did it — writing to a required structure flattens exactly the
sentence-variation and perplexity that both signals read as "machine-like," so
the student is penalised for following instructions. Nothing about the text is
AI, and the system had no way to say so. It is the clearest case of the
one-sided cost Criterion 1 is about: a missed AI text inconveniences the site a
little, but this accuses a person.

---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

Three trials each, produced by `run_eval.py::main` against `app.py::submit`
(scoring `scoring.py::combine_signals`), file `results/run_2026-11-09_0137_before.md`.
Nothing in either signal is random, so the three trials are identical — that is
evidence the test ran, not a skipped step.

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. Limit false positives | ≤ 1 of 10 human samples labelled `ai`, every trial | 0 / 10 | 0 / 10 | 0 / 10 | ✅ MET |
| 2. Separate human vs AI scores | AI mean − human mean ≥ 0.20, every trial | gap **0.11** | gap **0.11** | gap **0.11** | ❌ MISSED |
| 3. All three labels reachable | `score_to_label(0.0, 0.5, 1.0)` = human, unsure, ai | ✅ | ✅ | ✅ | ✅ MET |
| 4. Record valid appeals | success + 1 appeal entry + `under_review` | ✅ | ✅ | ✅ | ✅ MET¹ |
| 5. Reject bad input | 400 / 400 / 400 · 200 @10k · 413 @10k+1 | ✅ | ✅ | ✅ | ✅ MET |

¹ Criterion 4 is not exercised by `run_eval.py` (it only calls `/submit`). It is
verified in the **Sample Run** above and in the audit log: the appeal returns
success, appends one `event: appeal` entry, and moves the item to `under_review`.

**Criterion 2, the numbers behind the miss:** human mean confidence
`0.482`, AI mean confidence `0.592`, gap `0.110` — against a `0.20` target.
Both groups sit inside the unsure band; they are not 0.20 apart.

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

Real output for each of the five criteria, Trial 1. Criteria 1, 2, 3 and 5 are
from `run_eval.py::main` → `results/run_2026-11-09_0137_before.md`; all three
trials are byte-identical, so Trial 1 stands for all three. Criterion 4 is not
driven by `run_eval` (it only calls `/submit`), so its output is the appeal
record from `audit.py::log_appeal` in `logs/audit.jsonl`, also shown in the
**Sample Run** above.

**Criterion 1 — my ten writing samples (0 of 10 labelled `ai`, every trial → MET):**

```json
[
  {"status": 200, "guess": "unsure", "confidence": 0.46451, "model_score": 0.4832, "style_score": 0.6625, "sent": "I finally got around to fixing the back fence this weekend. Took way l"},
  {"status": 200, "guess": "unsure", "confidence": 0.53570, "model_score": 0.6218, "style_score": 0.6457, "sent": "Honestly the movie was fine? Not great. The first hour dragged and I a"},
  {"status": 200, "guess": "unsure", "confidence": 0.56180, "model_score": 0.6579, "style_score": 0.6665, "sent": "We tried the new ramen place on 4th. The broth was rich, almost too sa"},
  {"status": 200, "guess": "unsure", "confidence": 0.52521, "model_score": 0.6085, "style_score": 0.6351, "sent": "I've been trying to run three times a week and it is not going well. M"},
  {"status": 200, "guess": "unsure", "confidence": 0.38739, "model_score": 0.3762, "style_score": 0.6016, "sent": "My grandmother used to keep hard candy in a blue tin on the counter, a"},
  {"status": 200, "guess": "unsure", "confidence": 0.47655, "model_score": 0.4969, "style_score": 0.6775, "sent": "The meeting could have been an email. We spent forty minutes on a deci"},
  {"status": 200, "guess": "unsure", "confidence": 0.38469, "model_score": 0.3205, "style_score": 0.6947, "sent": "I planted tomatoes too early this year and the frost got half of them."},
  {"status": 200, "guess": "unsure", "confidence": 0.48404, "model_score": 0.5072, "style_score": 0.6836, "sent": "Writing has never come easy to me. I stare at the blank page, type a s"},
  {"status": 200, "guess": "unsure", "confidence": 0.38314, "model_score": 0.3412, "style_score": 0.6516, "sent": "The dog figured out how to open the pantry door. We came home to kibbl"},
  {"status": 200, "guess": "unsure", "confidence": 0.56988, "model_score": 0.7110, "style_score": 0.5961, "sent": "I don't have a strong opinion on the new logo. It's blue now instead o"}
]
```

**Criterion 2 — human group (mean 0.482) then AI group (mean 0.592), gap 0.110 vs target 0.20 → MISSED:**

```json
// human examples
[
  {"status": 200, "guess": "unsure", "confidence": 0.47184, "model_score": 0.5448, "style_score": 0.574,  "sent": "When on board H.M.S. 'Beagle,' as naturalist, I was much struck with c"},
  {"status": 200, "guess": "unsure", "confidence": 0.47874, "model_score": 0.5328, "style_score": 0.619,  "sent": "distribution of the inhabitants of South America, and in the geologica"},
  {"status": 200, "guess": "unsure", "confidence": 0.49002, "model_score": 0.5928, "style_score": 0.5466, "sent": "the past inhabitants of that continent. These facts seemed to me to th"},
  {"status": 200, "guess": "unsure", "confidence": 0.50218, "model_score": 0.5242, "style_score": 0.7129, "sent": "the origin of species—that mystery of mysteries, as it has been called"},
  {"status": 200, "guess": "unsure", "confidence": 0.46579, "model_score": 0.5333, "style_score": 0.5749, "sent": "greatest philosophers. On my return home, it occurred to me, in 1837, "}
]
// AI examples
[
  {"status": 200, "guess": "unsure", "confidence": 0.56305, "model_score": 0.6809, "style_score": 0.6285, "sent": "Scientific inquiry represents one of the most valuable and transformat"},
  {"status": 200, "guess": "unsure", "confidence": 0.52624, "model_score": 0.6011, "style_score": 0.6521, "sent": "deeper understanding of the complex processes that shape biological di"},
  {"status": 200, "guess": "unsure", "confidence": 0.62126, "model_score": 0.5753, "style_score": 0.6783, "sent": "communicated to others. In this way, thoughtful research establishes a"},
  {"status": 200, "guess": "ai",     "confidence": 0.66005, "model_score": 0.6528, "style_score": 0.6655, "sent": "encourages curiosity, supports critical thinking, and promotes informe"},
  {"status": 200, "guess": "unsure", "confidence": 0.59026, "model_score": 0.7336, "style_score": 0.6226, "sent": "their work. Ultimately, the pursuit of knowledge is both an individual"}
]
```

**Criterion 3 — label coverage, one input per band → all three labels reached → MET:**

```json
[
  {"status": 200, "guess": "unsure", "confidence": 0.545825, "model_score": 0.6857, "style_score": 0.5623, "sent": "When on board H.M.S. 'Beagle,' as naturalist, I was much struck with c"},
  {"status": 200, "guess": "ai",     "confidence": 0.685600, "model_score": 0.7642, "style_score": 0.6404, "sent": "Scientific inquiry represents one of the most valuable and transformat"},
  {"status": 200, "guess": "unsure", "confidence": 0.635325, "model_score": 0.7143, "style_score": 0.8082, "sent": "The meeting may have been useful, but I'm not sure yet. I need to thin"}
]
```

> The `human` label is confirmed directly from the mapping function, since no
> real text in this run scored at or below 0.35:
> `python -c "import scoring; print([scoring.score_to_label(s)[0] for s in (0.0, 0.5, 1.0)])"`
> → `['human', 'unsure', 'ai']`. That (not the eval texts) is what Criterion 3 targets.

**Criterion 4 — a valid appeal moves the item to `under_review` and is logged (from `logs/audit.jsonl`) → MET:**

```json
[
  {"timestamp": "2026-11-02T03:15:24+00:00", "content_id": "f8ea81e6-4cbf-424b-9c2c-9ddd25b38edb", "creator_id": "test-user", "guess": "ai", "model_score": 0.7777, "style_score": 0.6641, "combined_score": 0.73794, "label": "This text has patterns often associated with AI-generated writing, but this result cannot prove who wrote it.", "status": "decided"},
  {"timestamp": "2026-11-02T03:15:30+00:00", "content_id": "f8ea81e6-4cbf-424b-9c2c-9ddd25b38edb", "creator_id": "test-user", "event": "appeal", "status": "under_review", "reasoning": "I wrote this myself and would like the result reviewed."}
]
```

**Criterion 5 — bad input and length boundary (all three trials identical) → MET:**

```json
[
  {"status": 400, "guess": null, "confidence": null, "sent": "{\"creator_id\": \"eval_missing_text\"}"},
  {"status": 400, "guess": null, "confidence": null, "sent": "(empty text)"},
  {"status": 400, "guess": null, "confidence": null, "sent": "   "},
  {"status": 200, "guess": "unsure", "confidence": 0.648915, "model_score": 0.9975, "style_score": 0.3343, "sent": "word word ... (exactly 10,000 characters)"},
  {"status": 413, "guess": null, "confidence": null, "sent": "word word ... (10,001 characters)"}
]
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

There is one missed criterion (2) and two broken attacks (FP04, FP06). They are
the same problem seen from two sides.

**Criterion 2 — MISSED. Stage: signal two (stylometry) and the combining rule.**
The human mean (0.482) and AI mean (0.592) are only 0.11 apart; the target is
0.20. The mechanism is that the **style signal does not discriminate**. Across
every text in the eval — Darwin, the AI passage, my own samples — `style_score`
sits in a narrow 0.55–0.71 band and never goes low: human Darwin windows scored
style 0.55–0.71, the AI passage scored 0.63–0.68, essentially the same range.
When one of the two signals carries no separation, the weighted average can only
separate as far as the other does — and the model signal's human range (0.52–0.59)
and AI range (0.58–0.73) overlap too. Averaging two weakly-separated signals
compresses both groups toward the middle of the unsure band, so the means land
0.11 apart instead of 0.20.

**FP04 and FP06 — BROKE. Stage: signal one (model).** FP04 (student essay to a
rubric): model 0.833, style 0.646 → 0.735 `ai`. FP06 (person imitating a formal
template): model 0.881, style 0.582 → 0.659 `ai`. The mechanism is the mirror
image: the **model signal over-fires on formal, structured human prose**. Writing
to a rubric or a template is predictable by construction — short, even sentences,
conventional transitions — which is exactly what low perplexity looks like, so
the model reads "predictable" as "AI." It drives `model_score` past 0.83, and at
weight 0.55 that alone carries the combined score over the 0.65 AI line while the
other signals stay moderate.

**The one pattern underneath both.** Nothing in the entire eval scored below 0.35
— not one of ten everyday human samples, not a single Darwin window — and in the
attack run no genuine-human text was ever labelled `human` either. The service
has effectively lost its bottom band for real writing: the style floor never
drops and the model fires on anything structured, so human text is pinned in
`unsure` or pushed into `ai`. Criterion 1 passes only because the unsure band is
wide enough to absorb that; Criterion 2 fails because the same compression leaves
no separation left to measure. The fix has to lower the floor on human text —
recalibrate the style signal so clean human prose scores low — which is the
improvement attempted below.



---

## The Improvement

**What I changed:** One change, in `stylometry.py::style_signal` — I inverted the
vocabulary term. It was `vocabulary_ai_score = type_token_ratio(text)` (a richer
vocabulary raised the AI-like score); it is now
`vocabulary_ai_score = 1.0 - type_token_ratio(text)` (a richer vocabulary lowers
it). Nothing else moved — same three measures, same weights (0.55 / 0.30 / 0.15),
same thresholds (0.35 / 0.65).

**Which diagnosis pointed at it:** The Criterion 2 miss and the FP04/FP06 breaks
shared one root cause — the style signal never scored low for genuine human
writing, so real text was pinned in `unsure` or pushed into `ai`, and the
human/AI means stayed compressed 0.11 apart. Two of the three style sub-scores
sit high for almost any prose; the vocabulary term was the one whose *direction*
was also wrong. High lexical variety is more typical of human writing than of
machine writing, yet the signal was counting it as AI-like. Flipping it is the
most direct way to let clean human prose score low, which is what the diagnosis
said the fix had to do. I changed only this one term so the before/after
difference is attributable to it and nothing else.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

Produced by `run_attacks.py --label after` →
`results/attack_run_2026-11-09_0200_after.md`, the same 56 attacks, one change
away from the before-run. Eight attacks changed verdict; the other 48 were
identical.

| Attack | Before | After | Effect |
|---|---|---|---|
| EV01 (evasion) | unsure 0.377 | **human 0.303** | ⬇ broke — AI-leaning text now cleared as human |
| EV05 (evasion) | unsure 0.357 | **human 0.304** | ⬇ broke — now cleared as human |
| EV08 (evasion) | unsure 0.363 | **human 0.263** | ⬇ broke — now cleared as human |
| EV07 (evasion) | ai 0.681 | unsure 0.627 | no longer caught |
| EV09 (evasion) | ai 0.651 | unsure 0.581 | no longer caught |
| FP06 (false_positive) | **ai 0.659** | unsure 0.613 | ⬆ **fixed — false accusation removed** |
| FP08 (false_positive) | unsure 0.412 | human 0.312 | ⬆ fixed — real human cleared |
| MF05 (malformed) | ai 0.749 | unsure 0.649 | junk no longer called AI |

Held / broke totals: **before 54 held / 2 broke → after 52 held / 4 broke.**

| Family | Broke before | Broke after |
|---|---|---|
| evasion | 0 | **3** (EV01, EV05, EV08) |
| false_positive | **2** | 1 (FP04 only) |
| prompt_injection | 0 | 0 |
| malformed | 0 | 0 |
| flood_same_creator | 0 | 0 |

**Ten audit entries from the after-run** (from `logs/audit.jsonl`; watch the
`style_score` column — it fell on every one, which is the change working):

```json
{"timestamp": "2026-11-09T07:00:29+00:00", "content_id": "cd20d933-b3ff-4caa-b0c4-026dc581620e", "creator_id": "attacker_EV01", "guess": "human", "model_score": 0.1635, "style_score": 0.4613, "combined_score": 0.302565, "label": "We think this was probably written by a person.", "status": "decided", "phrase_score": 0.495, "verified_human": false}
{"timestamp": "2026-11-09T07:00:31+00:00", "content_id": "0d3162b9-4ec8-494a-9591-e795ad81bfb7", "creator_id": "attacker_EV05", "guess": "human", "model_score": 0.3212, "style_score": 0.4236, "combined_score": 0.30374, "label": "We think this was probably written by a person.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-09T07:00:32+00:00", "content_id": "47bb852a-a76c-45fb-85f7-a592c9673ea3", "creator_id": "attacker_EV08", "guess": "human", "model_score": 0.2452, "style_score": 0.4265, "combined_score": 0.26281, "label": "We think this was probably written by a person.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-09T07:00:32+00:00", "content_id": "3cd49655-334f-49d1-9d16-f8392540b163", "creator_id": "attacker_EV07", "guess": "unsure", "model_score": 0.5862, "style_score": 0.5861, "combined_score": 0.62685, "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.", "status": "decided", "phrase_score": 0.8574, "verified_human": false}
{"timestamp": "2026-11-09T07:00:35+00:00", "content_id": "eef40b74-3103-4e81-9402-74c1a41dc8f3", "creator_id": "attacker_FP06", "guess": "unsure", "model_score": 0.8814, "style_score": 0.4258, "combined_score": 0.61251, "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-09T07:00:34+00:00", "content_id": "4e2ea7ba-e10c-4b0d-9b7c-2a38a46f4f81", "creator_id": "attacker_FP04", "guess": "ai", "model_score": 0.8329, "style_score": 0.4404, "combined_score": 0.67282, "label": "This text has patterns often associated with AI-generated writing, but this result cannot prove who wrote it.", "status": "decided", "phrase_score": 0.5507, "verified_human": false}
{"timestamp": "2026-11-09T07:00:35+00:00", "content_id": "c910900f-670e-41aa-a8c9-db5e35d99848", "creator_id": "attacker_FP08", "guess": "human", "model_score": 0.3223, "style_score": 0.45, "combined_score": 0.312265, "label": "We think this was probably written by a person.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-09T07:00:39+00:00", "content_id": "38f4076d-6070-4e6f-8d8a-da2030f36ec4", "creator_id": "attacker_MF05", "guess": "unsure", "model_score": 0.9976, "style_score": 0.3333, "combined_score": 0.64867, "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-09T07:00:41+00:00", "content_id": "5f99f481-e645-44cd-b14f-dec293a44862", "creator_id": "attacker_flood", "guess": "human", "model_score": 0.0287, "style_score": 0.4524, "combined_score": 0.151505, "label": "We think this was probably written by a person.", "status": "decided", "phrase_score": 0.0, "verified_human": false}
{"timestamp": "2026-11-09T07:00:37+00:00", "creator_id": "attacker_MF01", "event": "rejected", "status": "rejected", "reason": "invalid_text"}
```

**The five criteria, before vs after** (`run_eval.py --label after` →
`results/run_2026-11-09_0201_after.md`; three identical trials each):

| Criterion | Target | Before | After | Verdict |
|---|---|---|---|---|
| 1. Limit false positives | ≤ 1 of 10 `ai` | 0/10 (all `unsure`) | 0/10 (7 `unsure`, 3 `human`) | MET → **MET** |
| 2. Separate human vs AI | gap ≥ 0.20 | gap 0.110 | gap **0.091** | MISSED → **MISSED** |
| 3. All labels reachable | 0/.5/1 → h/u/ai | MET | MET | MET → **MET** |
| 4. Record valid appeals | status + log | MET | MET | MET → **MET** |
| 5. Reject bad input | 400/400/400·200·413 | MET | MET | MET → **MET** |

Criterion 2 detail: human mean 0.482 → **0.421**, AI mean 0.592 → **0.512**. Both
groups fell; the gap narrowed from 0.110 to 0.091.

**Did it help, and how do I know:** Partly — and not where I aimed it.

- **It helped the false-positive side**, which the diagnosis cared about most.
  FP06's wrong `ai` accusation is gone (now `unsure`); FP08 and three of my ten
  Criterion-1 samples are now correctly cleared as `human`; `style_score` fell
  by roughly 0.2 on human text (the reload check went 0.6625 → 0.3776).
  False-positive breaks dropped from **2 to 1**.
- **It did not fix the criterion I changed it for.** Criterion 2's gap went
  0.110 → **0.091** — slightly *worse*, still nowhere near 0.20. Inverting the
  vocabulary term lowered human and AI scores *together* (AI mean fell almost as
  much as human mean), because the AI passage's vocabulary variety is about the
  same as the human text's. Dropping the floor shifted both groups toward
  `human`; it did not pull them apart. The real problem is that neither signal
  separates these two sources — a level change to one signal can't create a
  separation that was never there.
- **It introduced a new cost.** Three evasion inputs (EV01, EV05, EV08) that were
  safely `unsure` are now confidently cleared as `human`, and the `ai` label is
  now rarely reached by real text (the AI source in label-coverage dropped from
  `ai` to `unsure`). Total attack breaks rose **2 → 4**.

Honest read: one change, one real win (fewer false accusations), the targeted
miss unmoved, and a widened evasion hole. By this project's own cost rule — a
wrong accusation costs a writer more than a missed detection costs the site —
trading FP06 for three missed evasions points the right way, but Criterion 2 is
still missed and I would not call this a clean success.



---

## What's Still Broken

- **Criterion 2 (score spread) — still missed, gap 0.091.** The two signals do
  not separate the human and AI sources; they overlap in both perplexity and
  vocabulary, so no level change to one signal opens the gap. What I'd do next is
  stop tuning signal levels and either recalibrate the *model* signal (it is the
  only one with any separation) or add a genuinely discriminating feature, then
  re-measure the gap. I stopped here because the milestone is one change, and
  stacking a second would hide which one moved the number.
- **FP04 — still accused (`ai`, 0.673).** Its `model_score` is 0.833, and the
  style change can't reach it; a formal, rubric-shaped human essay looks
  low-perplexity to signal one. Only a model-signal recalibration or a higher
  `AI_THRESHOLD` fixes this, and the threshold move is the next thing I'd try.
- **Evasion now leaks to `human` (EV01, EV05, EV08).** This is the direct cost of
  the fix: the same floor-lowering that cleared real writers also cleared three
  AI-leaning evasion inputs. A narrower change — only down-weighting vocabulary
  rather than fully inverting it — might keep the false-positive gain with less
  of this leak, and that is where I'd tune next.
- **The `ai` label is now hard to reach for real text.** After the change, the
  AI source scores `unsure`, not `ai`. The label is still reachable by score
  (Criterion 3 holds on the mapping function) but real submissions rarely get
  there, which weakens the service as a detector even as it gets safer for
  writers.

**The trade I'd make if this ran for real:** I would go toward fewer accusations
— keep this change, and likely widen the unsure band further — because on a
writing site a wrongly accused author pays far more than the site pays for
letting some AI text through. Who pays for that choice: the site and its readers,
who get a weaker, more often `unsure` AI signal and more evasions slipping past;
who it protects: real writers, who are the ones a false `ai` label actually
harms.

---

## Unit 8 Stretch Items
STRETCH FEATURES 
Two optional items built on top of the required Unit 8 work.

### Per-creator rate limiting (+1)

Rate limiting is keyed to the **creator**, not the caller's address.
`app.py::rate_limit_key` counts each request against its `creator_id`, and falls
back to the IP address only when the body has no usable creator_id (missing,
blank, or not a string). The limits are 15 / minute and 225 / day (`config.py`).

**What it catches that per-address missed:** abuse tied to one identity even when
it arrives from several addresses — one account hammering the service from a
laptop and a phone counts as one creator. The `flood_same_creator` family (12
submissions under `attacker_flood`) accumulates against that single key, and the
Milestone-1 flood of 20 under `flood_tester` is what trips the limit and produces
the 429s.

**What it costs:** it is trivially evaded by rotating the creator_id. Every row in
`attacks.csv` submits under its own `attacker_<id>`, so the whole attack set looks
like fifty-odd different callers and never trips the limit — **per-address**
limiting would have caught that, since it all came from one machine. The gain on
the other side is that a shared address (a household, a classroom, an office
behind one NAT) is not collectively punished the way per-address limiting would
punish it. The trade, in one line: per-creator accepts "one script can look like
a thousand callers" in exchange for "one household does not look like one
attacker."

### A second measured improvement (+2): raise the AI threshold
STRETCH FEATURE
**The change (one, from the diagnosis):** *What's Still Broken* named a higher
`AI_THRESHOLD` as the next thing to try for FP04 — the one false accusation the
stylometry fix couldn't reach, because its `model_score` is 0.833. So the second
change raises `AI_THRESHOLD` from 0.65 to 0.70 in `config.py`; nothing else moved.
Runs: `run_attacks.py --label after2` → `results/attack_run_2026-11-09_0215_after2.md`
and `run_eval.py --label after2` → `results/run_2026-11-09_0215_after2.md`.

**The five criteria across all three states** (three identical trials each, same
table format as the run log):

| Criterion | Target | Before | After 1 (style fix) | After 2 (threshold) |
|---|---|---|---|---|
| 1. Limit false positives | ≤ 1 / 10 `ai` | 0/10 · MET | 0/10 · MET | 0/10 · MET |
| 2. Separate human vs AI | gap ≥ 0.20 | 0.110 · MISSED | 0.091 · MISSED | 0.091 · MISSED |
| 3. All labels reachable | 0/.5/1 → h/u/ai | MET | MET | MET |
| 4. Record valid appeals | status + log | MET | MET | MET |
| 5. Reject bad input | 400/400/400·200·413 | MET | MET | MET |

**Attack outcomes across the three states:**

| | Before | After 1 | After 2 |
|---|---|---|---|
| false_positive breaks (human → `ai`) | 2 (FP04, FP06) | 1 (FP04) | **0** |
| evasion breaks (AI → `human`) | 0 | 3 | 3 |
| inputs labelled `ai` in the 56-attack set | 7 | 3 | **0** |

**Did it help?** For its one narrow purpose, yes — and honestly it went too far.
FP04 moved from `ai` (0.673) to `unsure`, so the service now makes **zero** false
accusations across the entire attack set. But it made the detector worse at the
job it exists for. Raising the threshold does nothing for Criterion 2 (thresholds
don't change the confidence means, so the gap stays 0.091, still missed), and it
emptied the `ai` label: EV10 and MF06 — genuinely machine / degenerate text —
dropped to `unsure` alongside FP04, so **not one input in the 56-attack set is
labelled `ai` any more**. The service is now safe for writers and nearly useless
as a detector. Reported as the rubric asks: a change that made things worse on
balance. If I kept only one change it would be the stylometry fix, which is a real
recalibration; this threshold move buys zero false accusations at the price of
zero detection, and in practice I'd pull it back toward 0.67 — enough to clear
FP04 without erasing the band entirely.

**What I shipped:** because this change made things worse on balance, I reverted
`AI_THRESHOLD` to 0.65 — the service runs with the stylometry fix (after 1) and
not this threshold. The after2 runs stay in `results/` as the evidence that the
experiment was made and measured.



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
