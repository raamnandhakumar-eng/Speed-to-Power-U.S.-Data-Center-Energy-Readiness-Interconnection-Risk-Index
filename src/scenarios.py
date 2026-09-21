"""Scenario definitions for Speed-to-Power."""

DEFAULT_SCENARIO = {
    "name": "300 MW phased energization",
    "full_load_mw": 300,
    "target_full_energization_year": 2029,
    "load_factor": 0.90,
    "phases": [
        {"year": 1, "mw": 50},
        {"year": 2, "mw": 125},
        {"year": 3, "mw": 225},
        {"year": 4, "mw": 300},
    ],
}

SCENARIOS = {
    "100mw": {
        "full_load_mw": 100,
        "load_factor": 0.90,
        "phases": [{"year": 1, "mw": 50}, {"year": 2, "mw": 100}],
    },
    "300mw": DEFAULT_SCENARIO,
    "500mw": {
        "full_load_mw": 500,
        "load_factor": 0.90,
        "phases": [
            {"year": 1, "mw": 75},
            {"year": 2, "mw": 200},
            {"year": 3, "mw": 350},
            {"year": 4, "mw": 500},
        ],
    },
}
