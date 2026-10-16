"""
Calibration scoring for AI EI.

Computes Brier score and a reliability diagram per model from a logged
calibration CSV (see logs/calibration_template.csv for the expected format).

Usage:
    python calibration_scoring.py ../logs/calibration.csv

Requires: pandas, numpy, matplotlib
"""

import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


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

    print("Brier score by model (lower = better calibrated):\n")
    print(brier_score(df).sort_values().to_string())

    for model in df["model"].unique():
        out_path = f"reliability_{model.replace(' ', '_')}.png"
        reliability_diagram(df, model, out_path=out_path)
        print(f"\nSaved reliability diagram for {model} -> {out_path}")


if __name__ == "__main__":
    main()
