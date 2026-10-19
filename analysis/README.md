# Analysis

Implemented: `calibration_scoring.py`, `faithfulness_scoring.py`, `stability_scoring.py`,
`robustness_scoring.py`, `accountability_scoring.py`, `shortcut_scoring.py` and `aggregate.py`
(sub-scores, meta-axes, weighting schemes, correlations, PCA; writes to `../writeup/`).

Not yet written: `clustering.py`. Original plan for each script:

- `faithfulness_scoring.py` — perturbation-flip rate per model
- `stability_scoring.py` — agreement rate / ICC across paraphrase variants
- `robustness_scoring.py` — agreement rate neutral vs. adversarial; pushback hold-rate
- `accountability_scoring.py` — rubric aggregation + judge-reliability check
- `shortcut_scoring.py` — invariance rate per model
- `aggregate.py` — z-scores all six sub-scores, combines into the two meta-axes (equal-weighted default),
  runs the correlation matrix / PCA validation described in `protocol.md`, and compares archetype
  placement across equal / PCA-loading / reliability-weighted schemes
- `clustering.py` — derives archetypes empirically from the aggregated per-model scores

Install dependencies: `pip install -r requirements.txt`
