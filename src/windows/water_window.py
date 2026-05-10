from src.models.water.water_data import WaterData
from src.services.water.water_calculator import WaterCalculator
from src.services.water.water_pdf_exporter import WaterPdfExporter
from src.windows.shared.people_bill_window import PeopleBillWindow


class WaterWindow(PeopleBillWindow):
    def __init__(self, mainMenuWindow):
        super().__init__(mainMenuWindow)

    def getUiFileName(self):
        return "water_window.ui"

    def initializeData(self):
        self.waterData = WaterData()

    def initializeServices(self):
        self.waterCalculator = WaterCalculator()
        self.waterPdfExporter = WaterPdfExporter()

    def getModeName(self):
        return "Water"

    def getBillData(self):
        return self.waterData

    def getCalculator(self):
        return self.waterCalculator

    def getPdfExporter(self):
        return self.waterPdfExporter

    def getStackedWidget(self):
        return self.waterStackedWidget

    def getBillLabel(self):
        return "acqua"

    def getBillUnitLabel(self):
        return "€/unità"

    def getFinalDetailsTitle(self):
        return "=== RIPARTIZIONE FINALE BOLLETTA ACQUA ==="