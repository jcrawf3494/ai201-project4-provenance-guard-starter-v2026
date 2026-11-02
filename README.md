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

**What it measures:**

**Why that might differ between human and AI writing:**

**What it can't see:**

### Signal two — the style signal

**What it measures:** `stylometry.style_signal` averages three normalized
measurements: sentence-length variation, type-token ratio, and punctuation
marks per word. For the initial human/AI example pair, low sentence variation
and higher vocabulary variety and punctuation point toward AI-like; those
directions are provisional and must be checked against more labeled examples.

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

```bash
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```powershell
$body = @{
  content_id = "94900b5b-d5a5-4b38-8794-bb67955e7f07"
  reasoning = "I wrote this myself and would like the result reviewed."
} | ConvertTo-Json -Compress
Invoke-RestMethod -Uri "http://127.0.0.1:5000/appeal" -Method Post -ContentType "application/json" -Body $body
```

Expected response:

```text
{
  "content_id": "94900b5b-d5a5-4b38-8794-bb67955e7f07",
  "message": "Your appeal has been recorded for review.",
  "ok": true,
  "status": "under_review"
}
```

**What the log shows afterwards**

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5000/log?limit=3" | ConvertTo-Json -Depth 5
```

After running these commands, paste the actual response and the matching
`event: "appeal"` log entry here. The appeal appends an `under_review` event;
the original decision remains in the append-only log.

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
