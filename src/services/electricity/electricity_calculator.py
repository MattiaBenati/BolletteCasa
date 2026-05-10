from dataclasses import dataclass
from src.models.electricity.electricity_data import ElectricityData


@dataclass
class ElectricityCalculationResult:
    totalAmount: float
    totalConsumption: float
    groundFloorPeople: int
    firstFloorPeople: int
    boilerStartReading: float
    boilerEndReading: float
    controlUnitMode: str
    groundFloorInitialKcal: float
    groundFloorFinalKcal: float
    firstFloorInitialKcal: float
    firstFloorFinalKcal: float

    boilerConsumption: float
    groundFloorDirectConsumption: float
    costPerKwh: float
    totalBoilerCost: float
    groundFloorConsumedKcal: float
    firstFloorConsumedKcal: float
    boilerCostPerKcal: float
    boilerCostPerPerson: float
    groundFloorBoilerCost: float
    firstFloorBoilerCost: float
    groundFloorDirectCost: float
    groundFloorTotal: float
    firstFloorTotal: float


class ElectricityCalculator:
    def __init__(self, electricityData: ElectricityData):
        self.electricityData = electricityData

    def calculate(self) -> ElectricityCalculationResult:
        totalAmount = self.electricityData.totalAmount
        totalConsumption = self.electricityData.totalConsumption
        groundFloorPeople = self.electricityData.groundFloorPeople
        firstFloorPeople = self.electricityData.firstFloorPeople
        boilerStartReading = self.electricityData.boilerStartReading
        boilerEndReading = self.electricityData.boilerEndReading
        controlUnitMode = (self.electricityData.controlUnitMode or "").strip().lower()
        groundFloorInitialKcal = self.electricityData.groundFloorInitialKcal
        groundFloorFinalKcal = self.electricityData.groundFloorFinalKcal
        firstFloorInitialKcal = self.electricityData.firstFloorInitialKcal
        firstFloorFinalKcal = self.electricityData.firstFloorFinalKcal

        boilerConsumption = boilerEndReading - boilerStartReading
        groundFloorDirectConsumption = totalConsumption - boilerConsumption
        costPerKwh = totalAmount / totalConsumption
        totalBoilerCost = boilerConsumption * costPerKwh

        groundFloorConsumedKcal = groundFloorFinalKcal - groundFloorInitialKcal
        firstFloorConsumedKcal = firstFloorFinalKcal - firstFloorInitialKcal

        boilerCostPerKcal = 0.0
        boilerCostPerPerson = 0.0
        groundFloorBoilerCost = 0.0
        firstFloorBoilerCost = 0.0

        if controlUnitMode == "riscaldamento":
            if groundFloorConsumedKcal != 0 and firstFloorConsumedKcal != 0:
                boilerCostPerKcal = totalBoilerCost / (groundFloorConsumedKcal + firstFloorConsumedKcal)
                groundFloorBoilerCost = groundFloorConsumedKcal * boilerCostPerKcal
                firstFloorBoilerCost = firstFloorConsumedKcal * boilerCostPerKcal
            elif groundFloorConsumedKcal == 0 and firstFloorConsumedKcal == 0:
                totalPeople = groundFloorPeople + firstFloorPeople
                boilerCostPerPerson = totalBoilerCost / totalPeople
                groundFloorBoilerCost = groundFloorPeople * boilerCostPerPerson
                firstFloorBoilerCost = firstFloorPeople * boilerCostPerPerson
            else:
                if groundFloorConsumedKcal != 0:
                    groundFloorBoilerCost = totalBoilerCost
                    firstFloorBoilerCost = 0.0
                else:
                    groundFloorBoilerCost = 0.0
                    firstFloorBoilerCost = totalBoilerCost

        elif controlUnitMode == "raffrescamento":
            groundFloorBoilerCost = 0.0
            firstFloorBoilerCost = totalBoilerCost

        groundFloorDirectCost = groundFloorDirectConsumption * costPerKwh
        groundFloorTotal = groundFloorDirectCost + groundFloorBoilerCost
        firstFloorTotal = firstFloorBoilerCost

        return ElectricityCalculationResult(
            totalAmount=totalAmount,
            totalConsumption=totalConsumption,
            groundFloorPeople=groundFloorPeople,
            firstFloorPeople=firstFloorPeople,
            boilerStartReading=boilerStartReading,
            boilerEndReading=boilerEndReading,
            controlUnitMode=controlUnitMode,
            groundFloorInitialKcal=groundFloorInitialKcal,
            groundFloorFinalKcal=groundFloorFinalKcal,
            firstFloorInitialKcal=firstFloorInitialKcal,
            firstFloorFinalKcal=firstFloorFinalKcal,
            boilerConsumption=boilerConsumption,
            groundFloorDirectConsumption=groundFloorDirectConsumption,
            costPerKwh=costPerKwh,
            totalBoilerCost=totalBoilerCost,
            groundFloorConsumedKcal=groundFloorConsumedKcal,
            firstFloorConsumedKcal=firstFloorConsumedKcal,
            boilerCostPerKcal=boilerCostPerKcal,
            boilerCostPerPerson=boilerCostPerPerson,
            groundFloorBoilerCost=groundFloorBoilerCost,
            firstFloorBoilerCost=firstFloorBoilerCost,
            groundFloorDirectCost=groundFloorDirectCost,
            groundFloorTotal=groundFloorTotal,
            firstFloorTotal=firstFloorTotal
        )