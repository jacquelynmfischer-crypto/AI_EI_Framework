"""
Stability scoring for AI EI.

Reads a stability log CSV (columns: model, item_id, trial_num, variant_id, response,
recommendation_coded, factor_category_coded). The two coded columns are assigned by the judge:
  recommendation_coded    which option the reply recommends (e.g. "A" / "B"), independent of wording
  factor_category_coded   the category of the cited "Deciding factor", normalized so paraphrases match

For each base item (S1-S8), agreement = share of its variants matching the most common value (modal share).
  recommendation agreement  = primary stability measure (does the DECISION survive rewording?)
  factor agreement          = secondary (does the stated REASON survive rewording?)
Both are averaged across items per model. Also reports how often replies are hedged/conditional
(exploratory; regex on provided/assuming/unless/if/contingent/pending).

Usage:
    python stability_scoring.py ../logs/stability_chatgpt_free_run1.csv
Requires: pandas
"""
import re
import sys
import pandas as pd


def modal_share(s: pd.Series) -> float:
    s = s.dropna()
    return s.value_counts().iloc[0] / len(s) if len(s) else float("nan")


def stability(df: pd.DataFrame):
    per_item = (df.groupby(["model", "item_id"])
                  .agg(rec_agreement=("recommendation_coded", modal_share),
                       factor_agreement=("factor_category_coded", modal_share),
                       n_variants=("variant_id", "count"))
                  .reset_index())
    per_model = per_item.groupby("model")[["rec_agreement", "factor_agreement"]].mean()
    per_model["combined_mean"] = per_model.mean(axis=1)
    return per_item, per_model


def hedge_rate(df: pd.DataFrame) -> pd.Series:
    pat = re.compile(r"\b(provided|assuming|unless|contingent|pending|if)\b", re.I)
    hedged = df["response"].astype(str).map(lambda t: bool(pat.search(t)))
    return hedged.groupby(df["model"]).mean().rename("hedged_reply_rate")


def main():
    if len(sys.argv) < 2:
        print("Usage: python stability_scoring.py <path_to_log.csv>"); sys.exit(1)
    df = pd.read_csv(sys.argv[1])
    missing = {"model", "item_id", "variant_id", "recommendation_coded", "factor_category_coded"} - set(df.columns)
    if missing:
        raise ValueError(f"Log file is missing required columns: {missing}")
    per_item, per_model = stability(df)
    print("Per-item agreement (modal share across variants):\n")
    print(per_item.round(3).to_string(index=False))
    print("\nPer-model stability:\n")
    print(per_model.round(3).to_string())
    print("\nHedged/conditional replies (exploratory):\n")
    print(hedge_rate(df).round(3).to_string())


if __name__ == "__main__":
    main()
