# mining/load_event_log.py

import pandas as pd
import pm4py


# =========================================================
# Load and Format Event Log for PM4Py
# =========================================================

def load_event_log(csv_path="data/event_log.csv"):

    # Read CSV
    df = pd.read_csv(
        csv_path,
        parse_dates=["timestamp"]
    )

    # Tell PM4Py column meanings
    df = pm4py.format_dataframe(
        df,
        case_id="case_id",
        activity_key="activity",
        timestamp_key="timestamp"
    )

    # Convert dataframe into PM4Py event log
    log = pm4py.convert_to_event_log(df)

    return df, log