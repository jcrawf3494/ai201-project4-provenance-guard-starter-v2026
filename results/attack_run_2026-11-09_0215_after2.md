# Attack run — after2

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-09 02:15
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
| EV01 | evasion | signal two: typos raise word variety | 200 | `ba11ec39-6069-40c9-9569-2278d26b4c65` | human | 0.303 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `8095ebd7-d538-43f3-b47c-2418b304e171` | unsure | 0.514 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `4e3c6a62-ac0c-4e7f-9d87-aca2eae04bde` | unsure | 0.566 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `b2c90643-db0b-4495-83f3-2eec3584e551` | unsure | 0.549 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `d495c22f-f248-4eea-b63e-a09180ed224f` | human | 0.304 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `67d89b42-6112-4d6e-97b3-5ca8caf2eed7` | unsure | 0.487 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `449f78ed-6f9c-410f-bdc1-395b3f7224c2` | unsure | 0.627 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `42dd20f6-85cd-4957-9e01-362ed86317d0` | human | 0.263 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `21b8bd4a-08fc-4f74-9225-c74b2f97a3e3` | unsure | 0.581 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `5e6f059c-f19b-426d-90f3-6bc2369cb042` | unsure | 0.694 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `93f3ad0a-aaac-41d0-976f-4658becb52ab` | unsure | 0.470 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `b37ff97d-aef6-4a8e-bf86-d6ddd1c41859` | unsure | 0.550 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `78e0b084-7afb-4dd8-9084-dddb6d8751de` | unsure | 0.575 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c9825f0c-21d9-4529-a83e-3439ff371c4d` | unsure | 0.673 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `e8569508-1780-4a3c-95eb-9efbacb7a06b` | unsure | 0.599 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `cabde7a7-a719-43cd-9b68-8ff29275ad29` | unsure | 0.613 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `efc3d938-7de8-4bd7-8b56-1584dc92dc4c` | unsure | 0.640 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `aca6ee6b-3d35-4db4-a4cd-1277a50f5dfc` | human | 0.312 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `029ff0bb-d667-4867-837a-6dae29d13c6e` | unsure | 0.357 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `6a10cdf6-5dea-4ecd-8969-2a8e30e87d34` | human | 0.230 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c5ab4673-050b-448d-a681-4448448f62fd` | unsure | 0.449 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `03ca47a8-a9de-435f-b228-7b3c03a10a1d` | unsure | 0.423 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `1c1e63df-275d-49ba-a421-2ab8f67cf01d` | unsure | 0.500 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c44a0048-290f-4196-b575-08fb4f23a265` | unsure | 0.438 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 200 | `0e204a8f-1b09-4352-b883-d1747bfa2f7c` | human | 0.177 |  |
| MF04 | malformed | text is only punctuation | 200 | `d447018a-f68b-47dd-b18e-9928d569c15a` | human | 0.156 |  |
| MF05 | malformed | text is a very long single word | 200 | `a634ebfa-a8ea-4d96-a742-5c91be281aaf` | unsure | 0.649 |  |
| MF06 | malformed | text is emoji only | 200 | `3578ba17-c647-432c-aeee-42ee9f537ed7` | unsure | 0.698 |  |
| MF07 | malformed | text is right-to-left script | 200 | `b78c6307-46ff-466b-a008-55d68630d072` | unsure | 0.649 |  |
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
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `5993c1ea-46fc-4518-8a7d-0f4c24fdde02` | human | 0.152 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `97d4086e-3bb9-4a40-94ea-9c5b7eef6c54` | human | 0.152 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `617cc39a-605e-41a5-8ce9-3238d7080c09` | human | 0.152 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `63f5c955-b481-4330-a8d3-63298567f9f7` | human | 0.152 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `8d2fccbe-59fa-4a7d-b716-9deaee175993` | human | 0.152 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `3e303e62-f4b3-41f5-b94a-febebee74a1d` | human | 0.152 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `1f999eef-9933-4ef2-9cc0-0e0ee5d5ff72` | human | 0.152 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c465bbb1-df42-491a-98c0-bc90a4608164` | human | 0.152 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `f8629a05-0b03-464b-aee6-e580d7ad1fd7` | human | 0.152 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c2e16093-4b29-4bc2-b086-caa3e2cfb191` | human | 0.152 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 200 | `0c160aa6-d44e-426d-989c-a42a23802092` | human | 0.152 |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 200 | `e23d177d-948f-4744-9fab-757e97b3a94e` | human | 0.152 |  |

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
  "content_id": "ba11ec39-6069-40c9-9569-2278d26b4c65",
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
  "content_id": "8095ebd7-d538-43f3-b47c-2418b304e171",
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
  "content_id": "4e3c6a62-ac0c-4e7f-9d87-aca2eae04bde",
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
  "content_id": "b2c90643-db0b-4495-83f3-2eec3584e551",
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
  "content_id": "d495c22f-f248-4eea-b63e-a09180ed224f",
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
  "content_id": "67d89b42-6112-4d6e-97b3-5ca8caf2eed7",
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
  "content_id": "449f78ed-6f9c-410f-bdc1-395b3f7224c2",
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
  "content_id": "42dd20f6-85cd-4957-9e01-362ed86317d0",
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
  "content_id": "21b8bd4a-08fc-4f74-9225-c74b2f97a3e3",
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
  "content_id": "5e6f059c-f19b-426d-90f3-6bc2369cb042",
  "creator_id": "attacker_EV10",
  "guess": "unsure",
  "confidence": 0.69438,
  "model_score": 0.9792,
  "style_score": 0.5194,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
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
  "content_id": "93f3ad0a-aaac-41d0-976f-4658becb52ab",
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
  "content_id": "b37ff97d-aef6-4a8e-bf86-d6ddd1c41859",
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
  "content_id": "78e0b084-7afb-4dd8-9084-dddb6d8751de",
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
  "content_id": "c9825f0c-21d9-4529-a83e-3439ff371c4d",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.6728200000000001,
  "model_score": 0.8329,
  "style_score": 0.4404,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
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
  "content_id": "e8569508-1780-4a3c-95eb-9efbacb7a06b",
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
  "content_id": "cabde7a7-a719-43cd-9b68-8ff29275ad29",
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
  "content_id": "efc3d938-7de8-4bd7-8b56-1584dc92dc4c",
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
  "content_id": "aca6ee6b-3d35-4db4-a4cd-1277a50f5dfc",
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
  "content_id": "029ff0bb-d667-4867-837a-6dae29d13c6e",
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
  "content_id": "6a10cdf6-5dea-4ecd-8969-2a8e30e87d34",
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
  "content_id": "c5ab4673-050b-448d-a681-4448448f62fd",
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
  "content_id": "03ca47a8-a9de-435f-b228-7b3c03a10a1d",
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
  "content_id": "1c1e63df-275d-49ba-a421-2ab8f67cf01d",
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
  "content_id": "c44a0048-290f-4196-b575-08fb4f23a265",
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
  "content_id": "0e204a8f-1b09-4352-b883-d1747bfa2f7c",
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
  "content_id": "d447018a-f68b-47dd-b18e-9928d569c15a",
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
  "content_id": "a634ebfa-a8ea-4d96-a742-5c91be281aaf",
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
  "content_id": "3578ba17-c647-432c-aeee-42ee9f537ed7",
  "creator_id": "attacker_MF06",
  "guess": "unsure",
  "confidence": 0.6982950000000001,
  "model_score": 0.9969,
  "style_score": 0.5,
  "label": "We can't reliably tell whether this was written by a person or by AI. This result is uncertain, not proof of AI use.",
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
  "content_id": "b78c6307-46ff-466b-a008-55d68630d072",
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
  "content_id": "5993c1ea-46fc-4518-8a7d-0f4c24fdde02",
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
  "content_id": "97d4086e-3bb9-4a40-94ea-9c5b7eef6c54",
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
  "content_id": "617cc39a-605e-41a5-8ce9-3238d7080c09",
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
  "content_id": "63f5c955-b481-4330-a8d3-63298567f9f7",
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
  "content_id": "8d2fccbe-59fa-4a7d-b716-9deaee175993",
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
  "content_id": "3e303e62-f4b3-41f5-b94a-febebee74a1d",
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
  "content_id": "1f999eef-9933-4ef2-9cc0-0e0ee5d5ff72",
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
  "content_id": "c465bbb1-df42-491a-98c0-bc90a4608164",
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
  "content_id": "f8629a05-0b03-464b-aee6-e580d7ad1fd7",
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
  "content_id": "c2e16093-4b29-4bc2-b086-caa3e2cfb191",
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
  "content_id": "0c160aa6-d44e-426d-989c-a42a23802092",
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
  "content_id": "e23d177d-948f-4744-9fab-757e97b3a94e",
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
