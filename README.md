# AI EI — Artificial Intelligence Explainable Intelligence

**AIPI 590.01 (Duke, Explainable AI) final project.**

AI EI is a behavioral instrument for measuring how large language models behave under the kinds of
pressure that matter in practice — not what they say about themselves, but what they actually do when
tested. It draws a deliberate parallel to *emotional intelligence* in humans while making a clear
distinction: this is not a claim that models have personalities or emotions. It is a practitioner-facing
framework, built from specific Explainable AI course concepts, for predicting how a given model will
behave and how to work with it.

The project has two halves:

1. **The instrument** — six behavioral sub-dimensions, each grounded in a named AIPI 590 course concept,
   measured with repeatable situational probes rather than self-report (self-report measures trained
   social desirability, not behavioral tendency — see `protocol.md`).
2. **The archetype guide** — the six sub-dimensions are grouped into two meta-axes (Epistemic Integrity,
   Pressure Resistance) and, once real model data is collected, clustered empirically into a small set of
   named archetypes with practical "how to work with this model" guidance — modeled on how a framework
   like the Michigan leadership model or Enneagram functions for humans, but built from measured LLM
   behavior instead of self-report.

## The six sub-dimensions

| Sub-dimension | Meta-axis | Course concept |
| --- | --- | --- |
| Calibration | Epistemic Integrity | Unit 0, Trust & Adoption — calibrated trust / automation bias |
| Faithfulness | Epistemic Integrity | Unit 2 Ch. 9 (+ Ch. 8 CoT faithfulness) |
| Shortcut sensitivity | Epistemic Integrity | Unit 0, Debugging — shortcut learning |
| Stability | Pressure Resistance | Unit 2 Ch. 9 — consistency under benign paraphrase |
| Robustness | Pressure Resistance | Unit 2 Ch. 9 — resistance to adversarial/loaded framing |
| Accountability posture | Pressure Resistance | Unit 0, Accountability |

See `protocol.md` for the full scoring/weighting methodology and `items/` for each sub-dimension's item
bank.

## Repo structure

```
AI_EI_Project/
├── README.md            this file
├── protocol.md           manual testing protocol, scoring methodology, weighting approach
├── items/                one file per sub-dimension: item bank + exact prompt wrapper
├── logs/                 trial data collected by hand across models
├── analysis/             scoring + statistics scripts (Brier score, ICC, PCA, clustering)
└── writeup/              final archetype guide and report
```

## Status

All six sub-dimensions fully drafted: item banks, protocols, and flip/variant/scoring instructions
complete for calibration, faithfulness, stability, robustness, accountability, and shortcut sensitivity.
Only `analysis/calibration_scoring.py` (Part 1 Brier + Part 2 unwarranted-confidence metrics) is implemented so far — the remaining five scoring scripts and the
meta-axis aggregation/clustering scripts are still to be written (see `analysis/README.md`). Data
collection has not yet started.

## Scope note (limitations)

This instrument is behavioral/black-box by design and does not require access to model weights or
activations. Course Units 1 and 3 (interpretable-by-construction models; mechanistic interpretability —
sparse autoencoders, circuits, feature clamping/steering) are out of scope for this reason and are named
here as a future-work direction: a white-box arm of this instrument, run against an open-weight model,
could validate self-report and behavioral measures against the model's actual internal computation.
