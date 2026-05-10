from dataclasses import dataclass


@dataclass
class GasCalculationResult:
    totalPeople: int
    costPerPerson: float
    costPerUnit: float
    groundFloorAmount: float
    firstFloorAmount: float