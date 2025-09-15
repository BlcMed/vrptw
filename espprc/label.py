from typing import Dict, Optional, List
import numpy as np


class Label:
    def __init__(self, node: int, resources: Dict[str, np.ndarray],
                 path: Optional[List[int]] = None):
        """
        Represents a partial path (label) ending at `node`.
        
        node: last node of the partial path
        resources: dict {resource_name: np.ndarray}
        path: full list of nodes visited so far, including the current node
        """
        self.node = node
        self.resources = {k: v.copy() for k, v in resources.items()}  # copy for mutability
        if path is None:
            self.path = [node]
        else:
            self.path = path.copy()
            if node != path[-1]:
                self.path.append(node)
