# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-09 02:00
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `cd20d933-b3ff-4caa-b0c4-026dc581620e` | human | 0.303 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `bd050908-c5d9-4706-bc04-1cb4edf914ca` | unsure | 0.514 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `92da8a6d-f961-4709-86b9-b904997fca1a` | unsure | 0.566 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `babdcbe3-e220-455b-ab09-7f9f64151f33` | unsure | 0.549 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `0d3162b9-4ec8-494a-9591-e795ad81bfb7` | human | 0.304 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `19b53268-8494-4a9c-b6dd-c120931d56bf` | unsure | 0.487 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `3cd49655-334f-49d1-9d16-f8392540b163` | unsure | 0.627 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `47bb852a-a76c-45fb-85f7-a592c9673ea3` | human | 0.263 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `056ee922-3ca9-40d8-bca7-a6a38aecf4d3` | unsure | 0.581 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `2caca9ac-6dea-4151-9722-d71c82532978` | ai | 0.694 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `42a617be-72c2-4de6-9133-8ab60362e46f` | unsure | 0.470 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `fb0bf76d-1fe2-42a3-8751-d567e70de01d` | unsure | 0.550 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `5e59ab0e-2c11-47ea-84a8-8992154cd8a1` | unsure | 0.575 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `4e2ea7ba-e10c-4b0d-9b7c-2a38a46f4f81` | ai | 0.673 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `d1d2667a-d9ee-432b-9dd1-41b4afde4bec` | unsure | 0.599 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `eef40b74-3103-4e81-9402-74c1a41dc8f3` | unsure | 0.613 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `e007fb89-8958-4855-9203-3e409d780497` | unsure | 0.640 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c910900f-670e-41aa-a8c9-db5e35d99848` | human | 0.312 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `9686df35-8c9f-4f0b-8d18-e7b9e749831d` | unsure | 0.357 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `465fdb20-a5c8-4f7e-8908-6a4f312556f7` | human | 0.230 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `2bb169cb-5e67-478f-914c-cfe72595a2f5` | unsure | 0.449 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `6f9cea8f-a947-44ad-822e-5ae2dbbb5004` | unsure | 0.423 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `1d096749-2c3d-48aa-ae02-c51beaa1af6a` | unsure | 0.500 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c2477715-e592-4a7c-ad6b-0cb9cb1146d8` | unsure | 0.438 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `c3f69bc3-351c-4841-b215-fea45f7a7d5b` | human | 0.177 |  |
| MF04 | malformed | text is only punctuation | 200 | `a9312e19-f6c1-45d1-961b-32bc7a84cb80` | human | 0.156 |  |
| MF05 | malformed | text is a very long single word | 200 | `38f4076d-6070-4e6f-8d8a-da2030f36ec4` | unsure | 0.649 |  |
| MF06 | malformed | text is emoji only | 200 | `202be1f5-c50f-404a-8d2e-585b5169db0f` | ai | 0.698 |  |
| MF07 | malformed | text is right-to-left script | 200 | `2d8a7ecf-4dde-4a97-8ef2-7dad1c2623ac` | unsure | 0.649 |  |
| MF08 | malformed | text is 60,000 characters | 413 | `—` | — | — |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5f99f481-e645-44cd-b14f-dec293a44862` | human | 0.152 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `6dd3b52d-cc01-43cd-bce9-f6c09e6c4d48` | human | 0.152 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b25d3775-1472-487a-9648-6ce4c2243631` | human | 0.152 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3645be75-6d28-452d-acd7-8434b58ab553` | human | 0.152 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `abc50b22-319b-49d8-b9b7-0254e4ffa1b7` | human | 0.152 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `2a64d4f3-171c-4d7a-874a-fcea2c0df1cf` | human | 0.152 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `b41d24b1-f0f7-4470-bfd6-27fcde0716a8` | human | 0.152 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `712e1337-7930-4ed5-b551-347665207180` | human | 0.152 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c6d55473-2627-444e-b39e-e5996360bec9` | human | 0.152 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f4c706f0-898e-426c-aaa9-c0e4bdbcb0fa` | human | 0.152 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 200 | `58908a3f-e9aa-42f5-9ebd-502b88517cce` | human | 0.152 |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 200 | `a36e129f-cc32-478b-9f74-3baa9d151721` | human | 0.152 |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "cd20d933-b3ff-4caa-b0c4-026dc581620e",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.302565,
  "model_score": 0.1635,
  "style_score": 0.4613,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "bd050908-c5d9-4706-bc04-1cb4edf914ca",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.5137050000000001,
  "model_score": 0.5943,
  "style_score": 0.3838,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "92da8a6d-f961-4709-86b9-b904997fca1a",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.5662849999999999,
  "model_score": 0.6662,
  "style_score": 0.4462,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "babdcbe3-e220-455b-ab09-7f9f64151f33",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.549135,
  "model_score": 0.6114,
  "style_score": 0.4635,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "0d3162b9-4ec8-494a-9591-e795ad81bfb7",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.30374,
  "model_score": 0.3212,
  "style_score": 0.4236,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "19b53268-8494-4a9c-b6dd-c120931d56bf",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.48732,
  "model_score": 0.5727,
  "style_score": 0.3368,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "3cd49655-334f-49d1-9d16-f8392540b163",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.62685,
  "model_score": 0.5862,
  "style_score": 0.5861,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "47bb852a-a76c-45fb-85f7-a592c9673ea3",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.26281,
  "model_score": 0.2452,
  "style_score": 0.4265,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "056ee922-3ca9-40d8-bca7-a6a38aecf4d3",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.5812,
  "model_score": 0.7042,
  "style_score": 0.4319,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "2caca9ac-6dea-4151-9722-d71c82532978",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.69438,
  "model_score": 0.9792,
  "style_score": 0.5194,
  "label": "This text has patterns often associated with AI-generated writing, but this result cannot prove who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "42a617be-72c2-4de6-9133-8ab60362e46f",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.4700350000000001,
  "model_score": 0.6175,
  "style_score": 0.4347,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "fb0bf76d-1fe2-42a3-8751-d567e70de01d",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.5503450000000001,
  "model_score": 0.7387,
  "style_score": 0.4802,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "5e59ab0e-2c11-47ea-84a8-8992154cd8a1",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.5754650000000001,
  "model_score": 0.8051,
  "style_score": 0.4422,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "4e2ea7ba-e10c-4b0d-9b7c-2a38a46f4f81",
  "creator_id": "attacker_FP04",
  "guess": "ai",
  "confidence": 0.6728200000000001,
  "model_score": 0.8329,
  "style_score": 0.4404,
  "label": "This text has patterns often associated with AI-generated writing, but this result cannot prove who wrote it.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "d1d2667a-d9ee-432b-9dd1-41b4afde4bec",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.599155,
  "model_score": 0.8005,
  "style_score": 0.5296,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "eef40b74-3103-4e81-9402-74c1a41dc8f3",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.61251,
  "model_score": 0.8814,
  "style_score": 0.4258,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "e007fb89-8958-4855-9203-3e409d780497",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.6401600000000001,
  "model_score": 0.8816,
  "style_score": 0.5176,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c910900f-670e-41aa-a8c9-db5e35d99848",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.312265,
  "model_score": 0.3223,
  "style_score": 0.45,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "9686df35-8c9f-4f0b-8d18-e7b9e749831d",
  "creator_id": "attacker_PI01",
  "guess": "unsure",
  "confidence": 0.356915,
  "model_score": 0.4625,
  "style_score": 0.3418,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "465fdb20-a5c8-4f7e-8908-6a4f312556f7",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.23002,
  "model_score": 0.2044,
  "style_score": 0.392,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "2bb169cb-5e67-478f-914c-cfe72595a2f5",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.44929500000000006,
  "model_score": 0.5943,
  "style_score": 0.4081,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "6f9cea8f-a947-44ad-822e-5ae2dbbb5004",
  "creator_id": "attacker_PI04",
  "guess": "unsure",
  "confidence": 0.4227,
  "model_score": 0.4998,
  "style_score": 0.4927,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "1d096749-2c3d-48aa-ae02-c51beaa1af6a",
  "creator_id": "attacker_PI05",
  "guess": "unsure",
  "confidence": 0.500285,
  "model_score": 0.6401,
  "style_score": 0.4941,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c2477715-e592-4a7c-ad6b-0cb9cb1146d8",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.438195,
  "model_score": 0.5583,
  "style_score": 0.4371,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 200,
  "content_id": "c3f69bc3-351c-4841-b215-fea45f7a7d5b",
  "creator_id": "attacker_MF03",
  "guess": "human",
  "confidence": 0.17690999999999998,
  "model_score": 0.0,
  "style_score": 0.5897,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "a9312e19-f6c1-45d1-961b-32bc7a84cb80",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.15616,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 200,
  "content_id": "38f4076d-6070-4e6f-8d8a-da2030f36ec4",
  "creator_id": "attacker_MF05",
  "guess": "unsure",
  "confidence": 0.6486700000000001,
  "model_score": 0.9976,
  "style_score": 0.3333,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 200,
  "content_id": "202be1f5-c50f-404a-8d2e-585b5169db0f",
  "creator_id": "attacker_MF06",
  "guess": "ai",
  "confidence": 0.6982950000000001,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "This text has patterns often associated with AI-generated writing, but this result cannot prove who wrote it.",
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "2d8a7ecf-4dde-4a97-8ef2-7dad1c2623ac",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.64852,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 413,
  "content_id": null,
  "creator_id": "attacker_MF08",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "5f99f481-e645-44cd-b14f-dec293a44862",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.151505,
  "model_score": 0.0287,
  "style_score": 0.4524,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "6dd3b52d-cc01-43cd-bce9-f6c09e6c4d48",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.151505,
  "model_score": 0.0287,
  "style_score": 0.4524,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "b25d3775-1472-487a-9648-6ce4c2243631",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.151505,
  "model_score": 0.0287,
  "style_score": 0.4524,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "3645be75-6d28-452d-acd7-8434b58ab553",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.151505,
  "model_score": 0.0287,
  "style_score": 0.4524,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "abc50b22-319b-49d8-b9b7-0254e4ffa1b7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.151505,
  "model_score": 0.0287,
  "style_score": 0.4524,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "2a64d4f3-171c-4d7a-874a-fcea2c0df1cf",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.151505,
  "model_score": 0.0287,
  "style_score": 0.4524,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "b41d24b1-f0f7-4470-bfd6-27fcde0716a8",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.151505,
  "model_score": 0.0287,
  "style_score": 0.4524,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "712e1337-7930-4ed5-b551-347665207180",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.151505,
  "model_score": 0.0287,
  "style_score": 0.4524,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "c6d55473-2627-444e-b39e-e5996360bec9",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.151505,
  "model_score": 0.0287,
  "style_score": 0.4524,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "f4c706f0-898e-426c-aaa9-c0e4bdbcb0fa",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.151505,
  "model_score": 0.0287,
  "style_score": 0.4524,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 200,
  "content_id": "58908a3f-e9aa-42f5-9ebd-502b88517cce",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.151505,
  "model_score": 0.0287,
  "style_score": 0.4524,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 200,
  "content_id": "a36e129f-cc32-478b-9f74-3baa9d151721",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.151505,
  "model_score": 0.0287,
  "style_score": 0.4524,
  "label": "We think this was probably written by a person.",
  "error": null,
  "verdict": ""
}
```
