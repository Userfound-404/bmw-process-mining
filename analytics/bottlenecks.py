# analytics/bottlenecks.py

import pandas as pd


# =========================================================
# Bottleneck + Insight Engine
# =========================================================

def compute_bottlenecks(csv_path="data/event_log.csv"):

    df = pd.read_csv(csv_path)

    # =====================================================
    # 1. Average duration per activity
    # =====================================================
    avg_activity = (
        df.groupby("activity")["duration_h"]
        .mean()
        .sort_values(ascending=False)
    )

    total_time = avg_activity.sum()

    shares = (avg_activity / total_time * 100).round(1)

    # =====================================================
    # 2. Shift performance comparison
    # =====================================================
    shift_avg = df.groupby("shift")["duration_h"].mean()

    night = shift_avg.get("Night", 0)
    morning = shift_avg.get("Morning", 1)

    shift_diff_pct = ((night - morning) / morning) * 100 if morning else 0

    # =====================================================
    # 3. Supplier bottleneck (Parts Allocated)
    # =====================================================
    parts = df[df["activity"] == "Parts Allocated"]

    supplier_avg = (
        parts.groupby("supplier_id")["duration_h"]
        .mean()
        .sort_values(ascending=False)
    )

    worst_supplier = supplier_avg.index[0]
    worst_supplier_time = supplier_avg.iloc[0]

    # =====================================================
    # 4. Model analysis (SUV vs others)
    # =====================================================
    model_avg = (
        df.groupby("model_type")["duration_h"]
        .mean()
        .sort_values(ascending=False)
    )

    worst_model = model_avg.index[0]
    worst_model_time = model_avg.iloc[0]

    # =====================================================
    # 5. Insights Generator (human readable)
    # =====================================================
    insights = []

    top_activity = avg_activity.index[0]

    insights.append(
        f"{top_activity} is the biggest bottleneck, accounting for {shares.iloc[0]:.1f}% of total process time."
    )

    if shift_diff_pct > 10:
        insights.append(
            f"Night shift is {shift_diff_pct:.1f}% slower than morning shift."
        )

    insights.append(
        f"Supplier {worst_supplier} causes the longest delays in Parts Allocated ({worst_supplier_time:.1f}h average)."
    )

    insights.append(
        f"{worst_model} vehicles take the longest time overall ({worst_model_time:.1f}h per event on average)."
    )

    return avg_activity, shares, insights


# =========================================================
# Run standalone
# =========================================================
if __name__ == "__main__":

    avg, shares, insights = compute_bottlenecks()

    print("\n=== AI INSIGHTS ===\n")

    for i in insights:
        print("•", i)

# =========================================================
# WHAT-IF SIMULATION ENGINE
# =========================================================

def what_if_simulation(
    csv_path="data/event_log.csv",
    night_shift_improvement=0.0,
    drop_supplier=None
):
    """
    Simulate process improvements and return avg lead time.
    """

    df = pd.read_csv(csv_path)

    # -----------------------------------------------------
    # 1. Improve night shift performance
    # -----------------------------------------------------
    if night_shift_improvement > 0:
        mask = df["shift"] == "Night"
        df.loc[mask, "duration_h"] *= (1 - night_shift_improvement)

    # -----------------------------------------------------
    # 2. Remove or fix bad supplier
    # -----------------------------------------------------
    if drop_supplier:
        bad_mask = df["supplier_id"] == drop_supplier

        # replace with system average (not deletion → realistic simulation)
        avg_duration = df.loc[~bad_mask, "duration_h"].mean()

        df.loc[bad_mask, "duration_h"] = avg_duration

    # -----------------------------------------------------
    # 3. Recompute lead time per order
    # -----------------------------------------------------
    new_avg = df.groupby("case_id")["duration_h"].sum().mean()

    return round(new_avg, 2)