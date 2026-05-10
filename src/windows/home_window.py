from src.windows.shared.abstract_window import AbstractWindow
from src.windows.electricity_window import ElectricityWindow
from src.windows.gas_window import GasWindow
from src.windows.water_window import WaterWindow


class HomeWindow(AbstractWindow):
    def __init__(self):
        super().__init__()
        self.loadUiFile("main_menu.ui")

        self.initializeWindowReferences()
        self.connectSignals()

    def initializeWindowReferences(self):
        self.electricityWindow = None
        self.gasWindow = None
        self.waterWindow = None

    def connectSignals(self):
        self.openElectricityWindowButton.clicked.connect(self.openElectricityWindow)
        self.openGasWindowButton.clicked.connect(self.openGasWindow)
        self.openWaterWindowButton.clicked.connect(self.openWaterWindow)

    def openWindow(self, windowClass, attributeName, logMessage):
        print(logMessage)
        windowInstance = windowClass(self)
        setattr(self, attributeName, windowInstance)
        windowInstance.show()
        self.hide()

    def openElectricityWindow(self):
        self.openWindow(ElectricityWindow, "electricityWindow", "Opening electricity window")

    def openGasWindow(self):
        self.openWindow(GasWindow, "gasWindow", "Opening gas window")

    def openWaterWindow(self):
        self.openWindow(WaterWindow, "waterWindow", "Opening water window")