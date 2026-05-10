from src.services.electricity.electricity_calculator import ElectricityCalculator


class ElectricityCalculationService:
    def calculate(self, electricityData):
        calculator = ElectricityCalculator(electricityData)
        return calculator.calculate()