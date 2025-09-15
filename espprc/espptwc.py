from typing import Dict, Any
import numpy as np
from espprc.base import ESPPRC
from espprc.label import Label

class ESPPTWC(ESPPRC):
    """Elementary Shortest Path Problem with Time Windows and Capacity (ESPPTWC).
    
    Expects problem_data with the following structure: 
    (I will tackle this data parsing in another package)

    problem_data = {
        "num_customers": int,
        "resource_windows": {
            "reduced_cost": ([0.0], [np.inf]),
            "time": ([lower_0, ..., lower_n], [upper_0, ..., upper_n]),
            "load": ([0.0], [vehicle_capacity]),
            "is_visited": ([0.0, ..., 0.0], [1.0, ..., 1.0])
        },
        "graph": {i: [neighbors], ...},
        "reduced_costs": {(i, j): float, ...},
        "travel_times": {(i, j): float, ...},
        "demands": {i: float, ...}
    }
    """

    def __init__(self, problem_data: Dict[str, Any]):
        super().__init__(problem_data)

        # Register REFs
        self.add_ref("reduced_cost", self.ref_reduced_cost)
        self.add_ref("time", self.ref_time)
        self.add_ref("load", self.ref_load)
        self.add_ref("is_visited", self.ref_visited)

    def initialize_label(self, start_node: int = 0) -> Label:
        """
        Initialize a label at `start_node` with proper resource shapes:
        - 'time' is a scalar (1-element array)
        - other resources remain vectors as defined in resource_windows
        """
        resources = {}
        for name, (low, high) in self.problem_data["resource_windows"].items():
            if name == "time":
                # we should keep it one element for time (scalar)
                resources[name] = np.array([low[start_node]], dtype=float)
            else:
                resources[name] = np.array(low, dtype=float)
        
        return Label(node=start_node, resources=resources)


    def ref_reduced_cost(self, resource: np.ndarray, current_node: int, dest: int, problem_data: Dict) -> np.ndarray:
        """Extend reduced cost along arc (current_node, dest)."""
        return resource + problem_data["reduced_costs"][(current_node, dest)]

    def ref_time(self, resource: np.ndarray, current_node: int, dest: int, problem_data: Dict) -> np.ndarray:
        """
        Extend time resource considering travel times and destination time window.
        
        - resource: np.ndarray with 1 element (current arrival time)
        - current_node: current node index
        - dest: destination node index
        """
        travel_time = problem_data["travel_times"][(current_node, dest)]
        arrival = resource[0] + travel_time  # scalar addition

        # Wait until lower bound at destination node
        lower_bounds, _ = problem_data["resource_windows"]["time"]
        arrival = max(arrival, lower_bounds[dest])

        return np.array([arrival], dtype=float)  # still a 1-element np.ndarray


    def ref_load(self, resource: np.ndarray, current_node: int, dest: int, problem_data: Dict) -> np.ndarray:
        """Add demand of destination to current load."""
        return resource + problem_data["demands"][dest]

    def ref_visited(self, resource: np.ndarray, current_node: int, dest: int, problem_data: Dict) -> np.ndarray:
        """Mark destination as visited."""
        new_resource = resource.copy()
        new_resource[dest] = 1
        return new_resource

    def check_feasibility(self, label: Label) -> bool:
        """
        Check feasibility of a label according to resource windows.

        Rules:
        - 'time': use upper bound of the current node only
        - 'load': must be within bounds
        - 'is_visited': all elements must satisfy 0 <= value <= 1
        - 'reduced_cost': must be >= 0
        """
        node = label.node  # current node

        for name, resource in label.resources.items():
            lower_bounds, upper_bounds = self.problem_data["resource_windows"][name]
            lower = np.array(lower_bounds, dtype=float)
            upper = np.array(upper_bounds, dtype=float)

            if name == "time":
                if resource[0] < lower[node] or resource[0] > upper[node]:
                    return False
            else:
                # Scalar or vector (load, reduced_cost) checked entirely
                if np.any(resource < lower) or np.any(resource > upper):
                    return False

        return True



if __name__ == "__main__":
    from espprc.problem_data_test import problem_data_test_1
    problem_data = problem_data_test_1

    # Create ESPPTWC instance
    espptwc = ESPPTWC(problem_data)

    # Initialize label at depot node 0
    depot_label = espptwc.initialize_label(start_node=0)

    print("Initial depot label resources:")
    for r, val in depot_label.resources.items():
        print(f"{r}: {val}")
    print("Path:", depot_label.path)

    # Extend from depot to customer 1
    label1 = espptwc.extend_label(depot_label, destination=1)
    if label1:
        print("\nExtended label to customer 1:")
        for r, val in label1.resources.items():
            print(f"{r}: {val}")
        print("Path:", label1.path)
    else:
        print("\nExtension to customer 1 is infeasible")

    # Extend from depot to customer 2
    label2 = espptwc.extend_label(depot_label, destination=2)
    if label2:
        print("\nExtended label to customer 2:")
        for r, val in label2.resources.items():
            print(f"{r}: {val}")
        print("Path:", label2.path)
    else:
        print("\nExtension from depot to customer 2 is infeasible")

    # Extend from depot to customer 3 (infeasible)
    label3 = espptwc.extend_label(depot_label, destination=3)
    if label3:
        print("\nExtended depot label from depot to customer 3:")
        for r, val in label3.resources.items():
            print(f"{r}: {val}")
        print("Path:", label2.path)
    else:
        print("\n depot extension to customer 3 is infeasible")

    # Extend from label1 to customer 3
    label13 = espptwc.extend_label(label1, destination=3)
    if label13:
        print("\nExtended label1 to customer 3:")
        for r, val in label13.resources.items():
            print(f"{r}: {val}")
        print("Path:", label13.path)
    else:
        print("\nExtension to customer 3 is infeasible from label1")

    # Extend from label2 to customer 3
    label23 = espptwc.extend_label(label2, destination=3)
    if label23:
        print("\nExtended label2 to customer 3:")
        for r, val in label23.resources.items():
            print(f"{r}: {val}")
        print("Path:", label23.path)
    else:
        print("\nExtension to customer 3 is infeasible from label2")
    
    # chceck feasibility
    print(espptwc.check_feasibility(label1))
    print(espptwc.check_feasibility(label2))
    print(espptwc.check_feasibility(label13))
    print(espptwc.check_feasibility(label23))

    # check dominance
    print(espptwc.dominates(label1,label1))
    print(espptwc.dominates(label1,label2))
    print(espptwc.dominates(label2,label1))
