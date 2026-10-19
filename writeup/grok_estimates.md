# Grok: estimated stability and faithfulness (not measured)

Grok's free-tier limit stopped the run before stability and faithfulness were complete. These two numbers are
**estimates, not data**. They are not in any CSV and are not used by `analysis/aggregate.py`. They exist so
Grok can be drawn on the radar and described next to the other models. Replace them with measured values.

| Dimension | Estimate | Range | Basis |
| --- | --- | --- | --- |
| Stability | 0.85 | 0.80 - 0.90 | 2 of 32 prompts measured: both S1 rewordings gave the same pick and the same deciding factor (Candidate B, technical score). Grok never hedged in any measured reply, which is the DeepSeek pattern (0.844). Claude 0.969, GPT-6 0.875. |
| Faithfulness | 0.875 | 0.75 - 1.00 | Not measured. Other models scored 1.00, 0.875, 0.875 on 8 items. Half of those items made one option dominate, so the test has little power and most models land in a narrow band. |

Measured Grok values used on the radar: calibration 0.997, shortcut 0.875, robustness 1.00 (framing 8/8,
pushback 8/8), accountability 1.00 (arm A 8/8 correct and re-confirmed, arm B 8/8 held; judge-coded).

Planned replacement: the condensed faithfulness run in `kits/grok_faithfulness_condensed.md` (4 items, 8
prompts), plus the remaining stability prompts if the quota allows.
