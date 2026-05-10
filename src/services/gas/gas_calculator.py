from src.models.gas.gas_data import GasData
from src.models.gas.gas_calculation_result import GasCalculationResult


class GasCalculator:
    def calculate(self, gasData: GasData) -> GasCalculationResult:
        if gasData.totalAmount is None:
            raise ValueError("Total amount is missing")

        if gasData.totalConsumption is None:
            raise ValueError("Total consumption is missing")

        totalPeople = gasData.groundFloorPeople + gasData.firstFloorPeople

        if totalPeople <= 0:
            raise ValueError("Total people must be greater than 0")

        if gasData.totalConsumption <= 0:
            raise ValueError("Total consumption must be greater than 0")

        costPerPerson = gasData.totalAmount / totalPeople
        costPerUnit = gasData.totalAmount / gasData.totalConsumption
        groundFloorAmount = costPerPerson * gasData.groundFloorPeople
        firstFloorAmount = costPerPerson * gasData.firstFloorPeople

        return GasCalculationResult(
            totalPeople=totalPeople,
            costPerPerson=costPerPerson,
            costPerUnit=costPerUnit,
            groundFloorAmount=groundFloorAmount,
            firstFloorAmount=firstFloorAmount
        )