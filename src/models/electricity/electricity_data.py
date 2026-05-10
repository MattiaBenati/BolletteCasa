from dataclasses import dataclass
from typing import Optional


@dataclass
class ElectricityData:
    totalAmount: Optional[float] = None
    totalConsumption: Optional[float] = None
    groundFloorPeople: int = 0
    firstFloorPeople: int = 0

    boilerStartReading: Optional[float] = None
    boilerEndReading: Optional[float] = None

    controlUnitMode: Optional[str] = None
    groundFloorInitialKcal: Optional[float] = None
    groundFloorFinalKcal: Optional[float] = None
    firstFloorInitialKcal: Optional[float] = None
    firstFloorFinalKcal: Optional[float] = None