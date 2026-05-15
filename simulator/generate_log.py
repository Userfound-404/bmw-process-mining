# simulator/generate_log.py

import pandas as pd
import numpy as np
from pathlib import Path

from datetime import datetime, timedelta

from simulator.process_definition import *


# =========================================================
# Generate BMW Manufacturing Event Log
# =========================================================

def generate_log(n_orders=5000, seed=42):

    # Reproducible randomness
    np.random.seed(seed)

    rows = []

    # Simulation start date
    start_date = datetime(2023, 1, 1)

    # =====================================================
    # Generate Orders
    # =====================================================

    for i in range(n_orders):

        # Unique order ID
        case_id = f"CAR{i:06d}"

        # Random metadata
        model = np.random.choice(MODEL_TYPES)
        supplier = np.random.choice(SUPPLIERS)
        priority = np.random.choice(["High", "Normal", "Low"])

        # Random starting timestamp
        timestamp = start_date + timedelta(
            hours=np.random.uniform(0, 8760)
        )

        # Copy the base process
        activities = list(ACTIVITIES)

        # =================================================
        # Rework Logic
        # =================================================

        # 15% chance quality inspection fails
        if np.random.rand() < 0.15:

            qc_idx = activities.index("Quality Check")

            # Add rework cycle
            activities.insert(qc_idx + 1, "Rework")
            activities.insert(qc_idx + 2, "Quality Check")

        # =================================================
        # Process Activities
        # =================================================

        for act in activities:

            shift = np.random.choice(SHIFTS)

            # Default duration if activity missing
            mean, std = ACTIVITY_DURATIONS.get(act, (10, 3))

            # =============================================
            # Supplier Delay Logic
            # =============================================

            # Supplier S103 is problematic
            if act == "Parts Allocated" and supplier == "S103":
                mean *= 1.8

            # =============================================
            # Generate Random Duration
            # =============================================

            duration = max(
                0.5,
                np.random.normal(mean, std)
            )

            # =============================================
            # Save Event
            # =============================================

            rows.append({

                "case_id": case_id,

                "activity": act,

                "timestamp": timestamp,

                "resource": f"Station_{np.random.randint(1,6)}",

                "shift": shift,

                "model_type": model,

                "supplier_id": supplier,

                "priority": priority,

                "duration_h": round(duration, 2),
            })

            # Move process time forward
            timestamp += timedelta(hours=duration)

    # =====================================================
    # Create DataFrame
    # =====================================================

    df = pd.DataFrame(rows)

    # Save CSV
    df.to_csv("data/event_log.csv", index=False)

    print(f"Generated {len(df)} events for {n_orders} orders.")

    return df


# =========================================================
# Run Script
# =========================================================

if __name__ == "__main__":
    generate_log()