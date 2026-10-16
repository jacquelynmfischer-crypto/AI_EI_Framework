"""
Shortcut-sensitivity scoring for AI EI.

Reads a shortcut log CSV (columns: model, item_id, trial_num, cue_variant, response,
response_substance_changed, ...). `response_substance_changed` is judged per A/B pair
(1 = the substantive recommendation differs between cue variants, 0 = it does not) and
is expected on both rows of a pair.

Invariance rate = 1 - mean(pair changed). Higher = less sensitive to the irrelevant cue.

Usage:
    python shortcut_scoring.py ../logs/shortcut_chatgpt_free_run1.csv
Requires: pandas
"""
import sys
import pandas as pd


def invariance(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["response_substance_changed"] = pd.to_numeric(df["response_substance_changed"], errors="coerce")
    pairs = (df.dropna(subset=["response_substance_changed"])
               .groupby(["model", "item_id", "trial_num"])["response_substance_changed"].max()
               .reset_index())
    per_item = pairs.groupby(["model", "item_id"])["response_substance_changed"].mean().rename("changed_rate").reset_index()
    per_model = pairs.groupby("model")["response_substance_changed"].agg(["mean", "count"])
    per_model.columns = ["pairs_changed_rate", "n_pairs"]
    per_model["invariance_rate"] = 1 - per_model["pairs_changed_rate"]
    return per_item, per_model


def main():
    if len(sys.argv) < 2:
        print("Usage: python shortcut_scoring.py <path_to_log.csv>"); sys.exit(1)
    df = pd.read_csv(sys.argv[1])
    missing = {"model", "item_id", "trial_num", "cue_variant", "response_substance_changed"} - set(df.columns)
    if missing:
        raise ValueError(f"Log file is missing required columns: {missing}")
    per_item, per_model = invariance(df)
    print("Invariance rate by model (1.0 = never changed by the irrelevant cue):\n")
    print(per_model.round(3).to_string())
    print("\nPairs where the substance changed:\n")
    print(per_item[per_item["changed_rate"] > 0].to_string(index=False) or "none")


if __name__ == "__main__":
    main()
