from src.models.gas.gas_data import GasData
from src.services.gas.gas_calculator import GasCalculator
from src.services.gas.gas_pdf_exporter import GasPdfExporter
from src.windows.shared.people_bill_window import PeopleBillWindow


class GasWindow(PeopleBillWindow):
    def __init__(self, mainMenuWindow):
        super().__init__(mainMenuWindow)

    def getUiFileName(self):
        return "gas_window.ui"

    def initializeData(self):
        self.gasData = GasData()

    def initializeServices(self):
        self.gasCalculator = GasCalculator()
        self.gasPdfExporter = GasPdfExporter()

    def getModeName(self):
        return "Gas"

    def getBillData(self):
        return self.gasData

    def getCalculator(self):
        return self.gasCalculator

    def getPdfExporter(self):
        return self.gasPdfExporter

    def getStackedWidget(self):
        return self.gasStackedWidget

    def getBillLabel(self):
        return "gas"

    def getBillUnitLabel(self):
        return "€/unità"

    def getFinalDetailsTitle(self):
        return "=== RIPARTIZIONE FINALE BOLLETTA GAS ==="