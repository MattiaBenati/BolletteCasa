from src.models.water.water_data import WaterData
from src.models.water.water_calculation_result import WaterCalculationResult


class WaterCalculator:
    def calculate(self, waterData: WaterData) -> WaterCalculationResult:
        if waterData.totalAmount is None:
            raise ValueError("Total amount is missing")

        if waterData.totalConsumption is None:
            raise ValueError("Total consumption is missing")

        totalPeople = waterData.groundFloorPeople + waterData.firstFloorPeople

        if totalPeople <= 0:
            raise ValueError("Total people must be greater than 0")

        if waterData.totalConsumption <= 0:
            raise ValueError("Total consumption must be greater than 0")

        costPerPerson = waterData.totalAmount / totalPeople
        costPerUnit = waterData.totalAmount / waterData.totalConsumption
        groundFloorAmount = costPerPerson * waterData.groundFloorPeople
        firstFloorAmount = costPerPerson * waterData.firstFloorPeople

        return WaterCalculationResult(
            totalPeople=totalPeople,
            costPerPerson=costPerPerson,
            costPerUnit=costPerUnit,
            groundFloorAmount=groundFloorAmount,
            firstFloorAmount=firstFloorAmount
        )