import numpy as np
from typing import Dict, Callable
from abc import ABC

class ESPPRC(ABC):
    """Abstract definition of an ESPPRC."""
    def __init__(self, resources: Dict[str, np.ndarray], problem_data: Dict):
        self.resources = resources
        self.problem_data = problem_data
        self.refs: Dict[str, Callable[[np.ndarray, int, Dict], np.ndarray]] = {}

    def add_resource(self, name: str, resource: np.ndarray, ref: Callable):
        self.resources[name] = resource
        self.refs[name] = ref

    def extend(self, destination: int) -> Dict[str, np.ndarray]:
        updated = {}
        for name, resource in self.resources.items():
            updated[name] = self.refs[name](resource.copy(), destination, self.problem_data)
        return updated
