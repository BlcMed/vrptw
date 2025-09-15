from abc import ABC, abstractmethod
from typing import Dict, Callable, List, Any
import numpy as np
from espprc.label import Label


class ESPPRC(ABC):
    """Abstract definition of an ESPPRC.
    Provides generic methods to initialize, extend, and compare labels.
    """

    def __init__(self, problem_data: Dict[str, Any]):
        self.problem_data = problem_data
        self.refs: Dict[str, Callable[[np.ndarray, int, int, Dict], np.ndarray]] = {}

    def add_ref(self, name: str, ref: Callable):
        """Register a resource extension function (REF) for a resource name."""
        self.refs[name] = ref

    def initialize_label(self, start_node: int = 0) -> Label:
        """Initialize a label at `start_node` with the lower bounds of each resource window."""
        resources = {}
        for name, (low, high) in self.problem_data["resource_windows"].items():
            resources[name] = np.array(low, dtype=float)  # lower bounds as starting point
        return Label(node=start_node, resources=resources)

    def extend_label(self, label: Label, destination: int) -> Label:
        """Create a new label by extending the given label using REFs.
        The new label will have an updated path including the destination node.
        """
        # Check if arc exists in the graph
        if "graph" in self.problem_data:
            neighbors = self.problem_data["graph"].get(label.node, [])
            if destination not in neighbors:
                # Arc does not exist
                return None

        new_resources = {}
        for name, value in label.resources.items():
            new_resources[name] = self.refs[name](value.copy(), label.node, destination, self.problem_data)
        return Label(node=destination, resources=new_resources, path=label.path)


    def dominates(
        self,
        label1: Label,
        label2: Label,
        exclude: List[str] = None
    ) -> bool:
        """Check if label1 dominates label2.
        
        Domination rule: label1[r] <= label2[r] for all r (excluding those in `exclude`).
        """
        if exclude is None:
            exclude = []

        for name, value1 in label1.resources.items():
            if name in exclude:
                continue
            value2 = label2.resources[name]
            # if any resource is strictly worse -> no domination
            if np.any(value1 > value2):
                return False

        return True

    def check_feasibility(self, label: Label) -> bool:
        """
        Generic feasibility: all resources must be within lower/upper bounds.
        Can be overridden by subclasses for problem-specific rules.
        """
        for name, resource in label.resources.items():
            lower, upper = map(np.array, self.problem_data["resource_windows"][name])
            if np.any(resource < lower) or np.any(resource > upper):
                return False
        return True
