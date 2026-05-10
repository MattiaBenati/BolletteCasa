from dataclasses import dataclass
from typing import Optional


@dataclass
class GasData:
    totalAmount: Optional[float] = None
    totalConsumption: Optional[float] = None
    groundFloorPeople: int = 0
    firstFloorPeople: int = 0