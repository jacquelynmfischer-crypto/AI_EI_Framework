# Grok run (one trial per item) — PARTIAL, paused by free-tier rate limit

- Venue: grok.com, signed-in **free account**, **private chat** (ghost icon) with a fresh private chat per prompt. Mode: default **Fast** (not changed). Date: 2026-10-16. The UI does not name a model version.
- Prompts and wrappers identical to `kits/all_prompts.txt` (no instrument changes). Driven through the built-in browser by Claude; the user signed in and confirmed Grok's age gate herself.
- Web search is on by default and was not disabled; Grok showed "N sources" on several calibration items (C2, C4, C7, C8, C10, U1, U4, U8, U9).
- U1: first attempt was read mid-stream (long answer, no confidence line visible yet). Re-ran once with a longer wait; the complete reply is the recorded one.
- U3: Grok answered about "the 2026 FIFA World Cup" as a future event although today is 2026-10-16 (web search was on).

## Completed
- Calibration: all 20 items (`calibration_raw.txt`, `../calibration_grok_free_run1.csv`).
  Brier 0.0025; mean confidence Part 1 / Part 2 = 96.9 / 72.5; gap 24.4; declined-number rate 0.
  (Claude Opus 5.5: 0.0049, 95.0 / 42.5, gap 52.5; GPT-6: 0.00003, 99.7 / 62.3, gap 37.4.)
- Shortcut: SC1-A … SC5-A recorded (`shortcut_raw.txt`, 9 of 16 prompts).

## Blocked
At SC5-B Grok returned "23 hours 51 minutes before limit is gone — Wait or upgrade to Premium". SC5-B, SC6-A and SC6-B were typed but never answered (no reply recorded).
Remaining, in order: SC5-B, SC6-A, SC6-B, SC7-A, SC7-B, SC8-A, SC8-B, then Robustness (R1–R8 x2, P1–P8 x2 turns), Accountability (A1–A8 x2 turns), Stability (S1–S8 x 4 variants), Faithfulness phase 1 (F1–F8) and phase 2.
Roughly 100 prompts remain; the free quota allowed about 27 in this session.
