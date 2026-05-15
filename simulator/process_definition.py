# simulator/process_definition.py

# =========================================================
# BMW Manufacturing Process Definition
# =========================================================

# These are the sequential steps every vehicle order follows
ACTIVITIES = [
    "Order Created",
    "Configuration Confirmed",
    "Parts Allocated",
    "Body Shop",
    "Assembly",
    "Paint Shop",
    "Quality Check",
    "Delivery Prep",
    "Vehicle Delivered"
]

# =========================================================
# Average Duration for Each Activity
# Format:
# "Activity Name": (mean_hours, standard_deviation)
# =========================================================

ACTIVITY_DURATIONS = {

    # Customer places order
    "Order Created": (2, 1),

    # Customer confirms vehicle specs/options
    "Configuration Confirmed": (8, 3),

    # Factory allocates required parts
    "Parts Allocated": (24, 12),

    # Car body manufacturing
    "Body Shop": (18, 5),

    # Vehicle assembly line
    "Assembly": (36, 8),

    # Vehicle painting process
    "Paint Shop": (20, 6),

    # Inspection and testing
    "Quality Check": (8, 4),

    # Final cleaning and prep
    "Delivery Prep": (6, 2),

    # Vehicle reaches customer/dealer
    "Vehicle Delivered": (4, 1),
}

# =========================================================
# Additional Simulation Variables
# =========================================================

# Vehicle types
MODEL_TYPES = [
    "Sedan",
    "SUV",
    "Coupe",
    "Electric"
]

# Factory working shifts
SHIFTS = [
    "Morning",
    "Afternoon",
    "Night"
]

# Fake supplier IDs
SUPPLIERS = [
    "S101",
    "S102",
    "S103",
    "S104"
]