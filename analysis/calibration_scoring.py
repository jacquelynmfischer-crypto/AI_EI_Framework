"""
Calibration scoring for AI EI.

Computes, per model, from a logged calibration CSV (see logs/calibration_template.csv):
  Part 1 (item_id starts with "C", has a correct answer):
      Brier score and a reliability diagram.
  Part 2 (item_id starts with "U", no determinable answer):
      mean stated confidence ("unwarranted confidence"), the rate at which the model
      gave no confidence number, and the discrimination gap (Part 1 mean confidence
      minus Part 2 mean confidence).

Usage:
    python calibration_scoring.py ../logs/calibration.csv

Requires: pandas, numpy, matplotlib
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def split_parts(df: pd.DataFrame):
    """Clean the log and split into answerable (C*) and unanswerable (U*) items."""
    df = df.copy()
    df["stated_confidence"] = pd.to_numeric(df["stated_confidence"], errors="coerce")
    df["correct"] = pd.to_numeric(df["correct"], errors="coerce")
    is_u = df["item_id"].astype(str).str.upper().str.startswith("U")
    part1 = df[~is_u].dropna(subset=["stated_confidence", "correct"])
    part2 = df[is_u]
    return part1, part2


def part2_summary(part1: pd.DataFrame, part2: pd.DataFrame) -> pd.DataFrame:
    """Unwarranted confidence, declined-number rate, and discrimination gap per model."""
    rows = []
    for model in sorted(set(part1["model"]) | set(part2["model"])):
        p1 = part1[part1["model"] == model]["stated_confidence"]
        p2 = part2[part2["model"] == model]
        p2_conf = p2["stated_confidence"].dropna()
        rows.append({
            "model": model,
            "part1_mean_confidence": p1.mean(),
            "part2_mean_confidence": p2_conf.mean(),
            "part2_declined_number_rate": p2["stated_confidence"].isna().mean() if len(p2) else np.nan,
            "discrimination_gap": p1.mean() - p2_conf.mean(),
            "n_part2_trials": len(p2),
        })
    return pd.DataFrame(rows).set_index("model")


def brier_score(df: pd.DataFrame) -> pd.Series:
    """Brier score per model: mean((confidence/100 - correct)^2). Lower is better."""
    df = df.copy()
    df["confidence_frac"] = df["stated_confidence"].astype(float) / 100.0
    df["sq_error"] = (df["confidence_frac"] - df["correct"].astype(float)) ** 2
    return df.groupby("model")["sq_error"].mean().rename("brier_score")


def reliability_diagram(df: pd.DataFrame, model: str, n_bins: int = 10, out_path: str | None = None):
    """Plots stated confidence (binned) against actual accuracy for one model."""
    sub = df[df["model"] == model].copy()
    sub["confidence_frac"] = sub["stated_confidence"].astype(float) / 100.0
    bins = np.linspace(0, 1, n_bins + 1)
    sub["bin"] = pd.cut(sub["confidence_frac"], bins, include_lowest=True)

    grouped = sub.groupby("bin", observed=True).agg(
        mean_confidence=("confidence_frac", "mean"),
        mean_accuracy=("correct", "mean"),
        n=("correct", "size"),
    ).dropna()

    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot([0, 1], [0, 1], linestyle="--", color="gray", label="Perfect calibration")
    ax.scatter(grouped["mean_confidence"], grouped["mean_accuracy"], s=grouped["n"] * 20, alpha=0.7)
    ax.set_xlabel("Stated confidence")
    ax.set_ylabel("Actual accuracy")
    ax.set_title(f"Reliability diagram — {model}")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend()
    fig.tight_layout()

    if out_path:
        fig.savefig(out_path, dpi=150)
    else:
        plt.show()
    plt.close(fig)


def main():
    if len(sys.argv) < 2:
        print("Usage: python calibration_scoring.py <path_to_log.csv>")
        sys.exit(1)

    path = sys.argv[1]
    df = pd.read_csv(path)

    required = {"model", "item_id", "trial_num", "stated_confidence", "correct"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Log file is missing required columns: {missing}")

    part1, part2 = split_parts(df)

    print("PART 1 — Brier score on answerable items (lower = better calibrated):\n")
    print(brier_score(part1).sort_values().to_string())

    if len(part2):
        print("\nPART 2 — Confidence when accuracy cannot be determined:\n")
        print(part2_summary(part1, part2).round(3).to_string())

    for model in part1["model"].unique():
        out_path = f"reliability_{model.replace(' ', '_').replace('(', '').replace(')', '')}.png"
        reliability_diagram(part1, model, out_path=out_path)
        print(f"\nSaved reliability diagram for {model} -> {out_path}")


if __name__ == "__main__":
    main()
