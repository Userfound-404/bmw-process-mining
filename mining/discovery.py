# mining/discovery.py

import pm4py

from mining.load_event_log import load_event_log


# =========================================================
# Process Discovery
# =========================================================

def discover_process(log):

    # =====================================================
    # Directly-Follows Graph (DFG)
    # =====================================================

    dfg, start_activities, end_activities = (
        pm4py.discover_directly_follows_graph(log)
    )

    # =====================================================
    # Performance DFG
    # =====================================================

    performance_dfg, _, _ = (
        pm4py.discover_performance_dfg(log)
    )

    # =====================================================
    # Save Process Map Image
    # =====================================================

    pm4py.save_vis_dfg(
        dfg,
        start_activities,
        end_activities,
        "data/process_map.png"
    )

    print("Process map saved to data/process_map.png")

    return dfg, performance_dfg


# =========================================================
# Run Script
# =========================================================

if __name__ == "__main__":

    # Load data
    df, log = load_event_log()

    # Discover process
    dfg, perf = discover_process(log)

    # =====================================================
    # Show Slowest Transitions
    # =====================================================

    

    # Extract mean performance safely
    clean_perf = {}

    for (a, b), metrics in perf.items():
        if isinstance(metrics, dict):
            # PM4Py returns dict like {"mean": ..., "median": ...}
            clean_perf[(a, b)] = metrics.get("mean", 0)
        else:
            clean_perf[(a, b)] = metrics


    # Sort by time (descending)
    sorted_perf = sorted(
        clean_perf.items(),
        key=lambda x: x[1],
        reverse=True
    )   


    print("\nTop 5 Slowest Transitions:\n")

    for (a, b), seconds in sorted_perf[:5]:
        print(f"{a} → {b}: {seconds/3600:.1f}h avg")