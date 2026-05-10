from dataclasses import dataclass


@dataclass
class WaterCalculationResult:
    totalPeople: int
    costPerPerson: float
    costPerUnit: float
    groundFloorAmount: float
    firstFloorAmount: float