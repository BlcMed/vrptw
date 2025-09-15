import numpy as np

problem_data_test_1 = {
    "num_customers": 3,

    # Resource windows
    "resource_windows": {
        "reduced_cost": ([0.0], [np.inf]),
        "time": (
            [0.0, 10.0, 0.0, 0.0],  # lower bounds for depot + 3 customers
            [100.0, 50.0, 40.0, 0.0]  # upper bounds
        ),
        "load": ([0.0], [15.0]),
        "is_visited": ([0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0])
    },

    # ---- Graph structure ----
    "graph": {
        0: [1, 2],  # depot can go to customer 1 or 2
        1: [3],     # customer 1 can go to 3
        2: [3],     # customer 2 can go to 3
        3: []       # customer 3 is last (can be depot itself)
    },

    # Arc data
    "reduced_costs": {
        (0, 1): 2.0,
        (0, 2): 3.0,
        (1, 3): 4.0,
        (2, 3): 1.0
    },
    "travel_times": {
        (0, 1): 5.0,
        (0, 2): 4.0,
        (1, 3): 6.0,
        (2, 3): 3.0
    },

    # Node-specific data
    "demands": {
        1: 4.0,
        2: 6.0,
        3: 5.0
    }
}
