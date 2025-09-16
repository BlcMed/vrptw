# VRPTW & Variants Solving Framework

This project addresses the **Vehicle Routing Problem with Time Windows (VRPTW)** and its variants by employing a **Dantzig–Wolfe reformulation** combined with a **column generation approach**. In this context, the **pricing problem** is formulated as an **Elementary Shortest Path Problem with Resource Constraints (ESPPRC)**, which can be efficiently solved using a **labeling algorithm**. This approach is foundational in solving VRPTW and related vehicle routing problems.

---

## Design Overview

The framework is designed to be **modular and extensible**, with a clear separation between:

1. **Problem Abstraction** – The **ESPPRC base class** provides generic methods for label initialization, extension, dominance checking, and feasibility verification.
2. **Problem-Specific Implementations** – Each variant, like **ESPPTWC**, extends the base class and defines **resource extension functions (REFs)** and feasibility rules.
3. **Label Representation** – Partial paths are encapsulated in a **Label class**, which stores the current node, resources, and full path, enabling easy manipulation and comparison.

---

## Project Structure

```
VRPPTW/
├── data/                  # Raw and processed datasets
├── data_processing/       # Modules to parse and prepare problem data
│   └── __init__.py
├── espprc/                # Core ESPPRC framework
│   ├── __init__.py
│   ├── base.py            # Abstract ESPPRC base class
│   ├── espptwc.py         # ESPPTWC problem implementation
│   ├── label.py           # Label class representing partial paths
│   └── problem_data_test.py  # Small test instance for ESPPTWC
├── .gitignore
├── LICENSE
└── README.md
```

---

## Data

The project will leverage benchmark **Solomon instances** for VRPTW problems. These datasets provide standardized **customer locations, demands, vehicle capacities, and time windows**, which are used to generate problem-specific inputs (feasible arcs, travel times, etc.) for the ESPPRC-based labeling algorithm.

* M. M. Solomon, *Algorithms for the Vehicle Routing and Scheduling Problems with Time Window Constraints*, Operations Research, 35(2), 1987.

---

## Core Components

1. **ESPPRC Base Class (`espprc/base.py`)**

   * Abstract class for ESPPRC problems.
   * Handles **generic label initialization**, **extension via REFs**, and **dominance checking**.
   * Supports numpy-based vector resources for efficiency.
   * Methods:

     * `initialize_label()` – generic label initialization at depot.
     * `extend_label(label, destination)` – extend label along an arc.
     * `dominates(label1, label2)` – compare two labels.
     * `check_feasibility(label)` – abstract, to be implemented in problem-specific subclasses.

2. **Label Class (`espprc/label.py`)**

   * Represents a partial path in the graph.
   * Stores **current node**, **resource values**, and the **full path**.
   * Fully compatible with ESPPRC extension and dominance checks.

3. **ESPPTWC (`espprc/espptwc.py`)**

   * Subclass of ESPPRC implementing **elementary shortest paths with time windows and vehicle capacity**.
   * Problem-specific REFs for:

     * `time` (scalar, waits for destination lower bound)
     * `reduced_cost`
     * `load`
     * `is_visited` (vector of visited customers)
   * Overrides:

     * `initialize_label()` – time as scalar
     * `check_feasibility()` – node-specific rules for time, global rules for other resources

4. **Problem Data (`espprc/problem_data_test.py`)**

   * Provides a **small test instance** for ESPPTWC.
   * Format includes:

     * `num_customers`, `vehicle_capacity`
     * `resource_windows` (lower/upper bounds for each resource)
     * `graph` (adjacency dictionary)
     * `reduced_costs`, `travel_times`, `demands`

---

## Next Steps

Future development will focus on:

1. **Data Processing Modules**

   * Parse Solomon datasets.
   * Construct **problem-specific data**: feasible arcs, distances, travel times, etc.

2. **Labeling Algorithm**

   * Implement the labeling algorithm.

3. **Additional ESPPRC Variants**

   * Implement other ESPPRC problems for VRPTW variants.
   * Reuse the base class to define new REFs and feasibility rules.

4. **Column Generation Approach**

   * Use the labeling algorithm to **solve ESPPTWC and other variants**.
   * Integrate with master problem formulations for vehicle routing optimization.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](./LICENSE) file for details.
