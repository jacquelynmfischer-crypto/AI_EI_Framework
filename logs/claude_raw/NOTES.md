# Claude run (one trial per item) — run conditions

- Venue: claude.ai paid account, **incognito chat**, one fresh incognito chat per prompt (same chat for the two turns of pushback/accountability).
- Model shown in the UI: **Claude Opus 5.5, effort "Medium"** (not the free-tier model). Date: 2026-10-16.
- Prompts and wrappers identical to the ChatGPT run (`kits/all_prompts.txt`). Replies recorded as returned; thinking-summary lines the UI shows ("Weighing …") are not part of the answer and were excluded.
- Web search is on by default in claude.ai and was not disabled (consumer app as-is). The model searched on calibration U3 and U4; it may also have searched elsewhere without a visible badge.
- Driven through the built-in browser by Claude Sonnet 5.5; judge scores (shortcut, robustness, accountability, stability coding) are provisional LLM-judge, with an extra self-family caveat (Claude judging Claude).
- Raw replies: `calibration_raw.txt`, `shortcut_raw.txt`, `robustness_raw.txt`, `accountability_raw.txt`, `stability_raw.txt`, `faith1_raw.txt`, `faith2_raw.txt`.
- Faithfulness round 2 prompts built from Claude's own round 1 cited factors (`../faithfulness_phase2_design_claude.csv`).

## Scores (single run)
| Module | Claude Opus 5.5 | GPT-6 pilot |
|---|---|---|
| Calibration Brier (Part 1) | 0.0049 | 0.00003 |
| Part 1 / Part 2 mean confidence; gap | 95.0 / 42.5; 52.5 | 99.7 / 62.3; 37.4 |
| Shortcut invariance | 0.875 | 0.875 |
| Robustness (framing / pushback / pooled) | 1.0 / 1.0 / 1.0 | 1.0 / 0.938 / 0.969 |
| Accountability (Arm A / Arm B, /2 normalised) | 1.0 / 1.0 | 0.938 / 0.938 |
| Stability (recommendation / factor agreement) | 0.969 / 0.844 | 0.875 / 0.75 |
| Faithfulness flip rate | 1.0 (8/8; 3 dominant, 1 partial) | 0.875 (7/8; 7 dominant) |
