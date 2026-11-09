# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1. Limit false positives for human writing

Across each of the three evaluation trials, no more than 1 of 10 windows from
the known human-authored Darwin passage in `scenarios.py` will receive the
high-confidence AI label.

**Why this target:** A false accusation can harm a real writer, so I would
rather leave some AI-written text uncertain than label a person's own writing
as AI. The test uses a known human-authored source because it is available for
repeatable evaluation; its overlapping windows are correlated, so I will not
treat the result as a general false-positive rate.

> **Revised in unit 8:** The input is now ten short, independent human-authored
> writing samples (`scenarios.OWN_WRITING`) instead of the Darwin windows. Same
> target: across each of three trials, at most 1 of the 10 receives the
> high-confidence AI label.
>
> **Why revised:** the Darwin windows overlap, so a single hard window showed up
> several times and the "10" wasn't 10 independent chances to misfire. Ten
> separate everyday passages are closer to what a real writing-site user submits
> and make the false-positive count mean what it says. The target did not move.

---

## 2. Separate clearly human and clearly AI scores

In each evaluation trial, the mean `/submit` `confidence` across the five
AI-generated sample windows in `scenarios.py` will be at least 0.20 higher
than the mean `confidence` across the five human-authored sample windows.
`confidence` is the combined score on the 0-to-1 scale.

**Why this target:** A 0.20 gap is large enough to show useful separation on
the 0-to-1 scale without demanding perfect detection. The two example groups
are fixed in `scenarios.py` and their returned `confidence` values appear in
the `run_eval.py` report.
---

## 3. Make all three labels reachable

Scores of 0.00, 0.50, and 1.00 passed to the label-mapping function will
produce, respectively, the human, unsure, and AI labels.

**Why this target:** A label category that no possible score can produce is
misleading to readers and makes the label ranges incomplete. Testing the low,
middle, and high ends checks that all three categories can be reached. Run
`python -c "import scoring; print([scoring.score_to_label(s)[0] for s in (0.0, 0.5, 1.0)])"`
and verify the output is `['human', 'unsure', 'ai']`.

---

## 4. Record valid appeals and change their status

For every valid appeal referring to an existing `content_id`, the endpoint
will return a success response, append exactly one appeal entry to the audit
log, and record the content's status as `under_review`.

**Why this target:** A writer needs confirmation that their appeal was
received, and a reviewer needs a record of it. Requiring both the status change
and the log entry makes the appeal path observable rather than just a message
to the writer.

---

## 5. Reject missing, empty, and oversized text

In each `run_eval.py` trial, missing, empty, and whitespace-only `text` will
receive HTTP 400; exactly 10,000 characters will be accepted with HTTP 200;
and 10,001 characters will receive HTTP 413. Rejected requests will create a
rejection log entry and no decision entry.

**Why this target:** Missing or empty text cannot be meaningfully scored, and
a fixed 10,000-character limit prevents unexpectedly large submissions from
consuming excessive processing time. The bad-input scenario sends the exact
boundary cases, and `run_eval.py` records the status code for each one.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
