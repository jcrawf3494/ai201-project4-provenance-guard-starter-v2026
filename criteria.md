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

Across each of the three evaluation trials, no more than 1 of 10 pieces of
human-written text will receive the high-confidence AI label.

**Why this target:** A false accusation can harm a real writer, so I would
rather leave some AI-written text uncertain than label a person's own writing
as AI. Testing 10 examples per trial makes the limit concrete.

---

## 2. Separate clearly human and clearly AI scores

In each evaluation trial, the mean combined score for the clearly AI-written
examples will be at least 0.20 higher than the mean combined score for the
clearly human-written examples.

**Why this target:** A 0.20 gap is large enough to show useful separation on
the 0-to-1 scale, without demanding perfect detection or that every individual
example score in the expected order.
---

## 3. Make all three labels reachable

Scores of 0.00, 0.50, and 1.00 passed to the label-mapping function will
produce, respectively, the human, unsure, and AI labels.

**Why this target:** A label category that no possible score can produce is
misleading to readers and makes the label ranges incomplete. Testing the low,
middle, and high ends checks that all three categories can be reached.

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

Requests with missing or whitespace-only `text` will receive HTTP 400;
requests with more than 10,000 characters of text will receive HTTP 413.
None of these requests will create a decision entry in the audit log.

**Why this target:** Missing or empty text cannot be meaningfully scored, and
a fixed 10,000-character limit prevents unexpectedly large submissions from
consuming excessive processing time. Explicit status codes and checking the
log make each outcome verifiable.

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
