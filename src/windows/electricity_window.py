from src.models.electricity.electricity_data import ElectricityData
from src.services.electricity.electricity_calculation_service import ElectricityCalculationService
from src.services.electricity.electricity_pdf_service import ElectricityPdfService
from src.services.electricity.electricity_result_formatter import ElectricityResultFormatter
from src.windows.shared.abstract_window import AbstractWindow


class ElectricityWindow(AbstractWindow):
    def __init__(self, mainMenuWindow):
        super().__init__()
        self.loadUiFile("electricity_window.ui")

        self.mainMenuWindow = mainMenuWindow
        self.initializeData()
        self.initializeServices()
        self.connectNavigationSignals()
        self.connectStepSignals()
        self.goToGeneralDataPage()

    def initializeData(self):
        self.electricityData = ElectricityData()
        self.lastResultsSummaryText = ""
        self.lastResultsDetailsText = ""
        self.lastCalculationResult = None

    def initializeServices(self):
        self.electricityCalculationService = ElectricityCalculationService()
        self.electricityPdfService = ElectricityPdfService()
        self.resultFormatter = ElectricityResultFormatter(self.formatNumber, self.formatCurrency)

    def connectNavigationSignals(self):
        self.generalDataBackButton.clicked.connect(self.goBackToMainMenu)
        self.resultsBackButton.clicked.connect(self.goBackToMainMenu)
        self.exportPdfButton.clicked.connect(self.handleExportPdf)

    def connectStepSignals(self):
        self.generalDataNextButton.clicked.connect(self.handleGeneralDataNext)
        self.boilerReadingsBackButton.clicked.connect(self.goToGeneralDataPage)
        self.boilerReadingsNextButton.clicked.connect(self.handleBoilerReadingsNext)
        self.controlUnitBackButton.clicked.connect(self.goToBoilerReadingsPage)
        self.controlUnitNextButton.clicked.connect(self.handleControlUnitNext)

    def handleGeneralDataNext(self):
        if not self.saveGeneralData():
            return

        print("Electricity general data saved:", self.electricityData)
        self.goToBoilerReadingsPage()

    def saveGeneralData(self):
        try:
            totalAmount, totalConsumption = self.readGeneralConsumptionValues()
            groundFloorPeople, firstFloorPeople = self.readPeopleValues()
            self.applyGeneralData(totalAmount, totalConsumption, groundFloorPeople, firstFloorPeople)
            return True
        except ValueError as error:
            self.showValidationError(str(error))
            return False

    def readGeneralConsumptionValues(self):
        totalAmount = self.parsePositiveFloat(
            self.totalAmountLineEdit.text(),
            "L'importo totale deve essere maggiore di 0"
        )
        totalConsumption = self.parsePositiveFloat(
            self.totalConsumptionLineEdit.text(),
            "Il consumo totale deve essere maggiore di 0"
        )
        return totalAmount, totalConsumption

    def readPeopleValues(self):
        groundFloorPeople = self.groundFloorPeopleSpinBox.value()
        firstFloorPeople = self.firstFloorPeopleSpinBox.value()

        if groundFloorPeople < 0:
            raise ValueError("Il numero di persone al piano terra non può essere negativo")

        if firstFloorPeople < 0:
            raise ValueError("Il numero di persone al primo piano non può essere negativo")

        if groundFloorPeople == 0 and firstFloorPeople == 0:
            raise ValueError("Deve esserci almeno 1 persona tra piano terra e primo piano")

        return groundFloorPeople, firstFloorPeople

    def applyGeneralData(self, totalAmount, totalConsumption, groundFloorPeople, firstFloorPeople):
        self.electricityData.totalAmount = totalAmount
        self.electricityData.totalConsumption = totalConsumption
        self.electricityData.groundFloorPeople = groundFloorPeople
        self.electricityData.firstFloorPeople = firstFloorPeople

    def goBackToMainMenu(self):
        print("Electricity: back to main menu")
        self.mainMenuWindow.show()
        self.close()

    def goToGeneralDataPage(self):
        print("Electricity: generalDataPage")
        self.electricityStackedWidget.setCurrentWidget(self.generalDataPage)

    def goToBoilerReadingsPage(self):
        print("Electricity: boilerReadingsPage")
        self.populateBoilerReadingsPage()
        self.electricityStackedWidget.setCurrentWidget(self.boilerReadingsPage)

    def goToControlUnitPage(self):
        print("Electricity: controlUnitPage")
        self.populateControlUnitPage()
        self.electricityStackedWidget.setCurrentWidget(self.controlUnitPage)

    def goToResultsPage(self):
        print("Electricity: resultsPage")
        self.electricityStackedWidget.setCurrentWidget(self.resultsPage)

    def handleBoilerReadingsNext(self):
        if not self.saveBoilerReadings():
            return

        print("Boiler readings saved:", self.electricityData)
        self.goToControlUnitPage()

    def saveBoilerReadings(self):
        try:
            startReading, endReading = self.readBoilerReadingsValues()
            self.applyBoilerReadings(startReading, endReading)
            return True
        except ValueError as error:
            self.showValidationError(str(error))
            return False

    def readBoilerReadingsValues(self):
        startReading = self.parseNonNegativeFloat(
            self.boilerStartReadingLineEdit.text(),
            "La lettura iniziale della caldaia deve essere un numero valido"
        )
        endReading = self.parseNonNegativeFloat(
            self.boilerEndReadingLineEdit.text(),
            "La lettura finale della caldaia deve essere un numero valido"
        )

        if endReading < startReading:
            raise ValueError("La lettura finale deve essere maggiore o uguale a quella iniziale")

        return startReading, endReading

    def applyBoilerReadings(self, startReading, endReading):
        self.electricityData.boilerStartReading = startReading
        self.electricityData.boilerEndReading = endReading

    def handleControlUnitNext(self):
        if not self.saveControlUnitData():
            return

        print("Control unit data saved:", self.electricityData)

        calculationResult = self.electricityCalculationService.calculate(self.electricityData)

        self.lastCalculationResult = calculationResult
        self.updateResultsPage(calculationResult)
        self.goToResultsPage()

    def saveControlUnitData(self):
        try:
            (
                controlUnitMode,
                groundFloorInitialKcal,
                groundFloorFinalKcal,
                firstFloorInitialKcal,
                firstFloorFinalKcal
            ) = self.readControlUnitValues()

            self.applyControlUnitData(
                controlUnitMode,
                groundFloorInitialKcal,
                groundFloorFinalKcal,
                firstFloorInitialKcal,
                firstFloorFinalKcal
            )
            return True
        except ValueError as error:
            self.showValidationError(str(error))
            return False

    def readControlUnitValues(self):
        controlUnitMode = self.controlUnitModeComboBox.currentText().strip()

        groundFloorInitialKcal = self.parseNonNegativeFloat(
            self.groundFloorInitialKcalLineEdit.text(),
            "Il valore iniziale kcal del piano terra deve essere un numero valido"
        )
        groundFloorFinalKcal = self.parseNonNegativeFloat(
            self.groundFloorFinalKcalLineEdit.text(),
            "Il valore finale kcal del piano terra deve essere un numero valido"
        )
        firstFloorInitialKcal = self.parseNonNegativeFloat(
            self.firstFloorInitialKcalLineEdit.text(),
            "Il valore iniziale kcal del primo piano deve essere un numero valido"
        )
        firstFloorFinalKcal = self.parseNonNegativeFloat(
            self.firstFloorFinalKcalLineEdit.text(),
            "Il valore finale kcal del primo piano deve essere un numero valido"
        )

        if groundFloorFinalKcal < groundFloorInitialKcal:
            raise ValueError("Il valore finale kcal del piano terra deve essere maggiore o uguale a quello iniziale")

        if firstFloorFinalKcal < firstFloorInitialKcal:
            raise ValueError("Il valore finale kcal del primo piano deve essere maggiore o uguale a quello iniziale")

        return (
            controlUnitMode,
            groundFloorInitialKcal,
            groundFloorFinalKcal,
            firstFloorInitialKcal,
            firstFloorFinalKcal
        )

    def applyControlUnitData(
        self,
        controlUnitMode,
        groundFloorInitialKcal,
        groundFloorFinalKcal,
        firstFloorInitialKcal,
        firstFloorFinalKcal
    ):
        self.electricityData.controlUnitMode = controlUnitMode
        self.electricityData.groundFloorInitialKcal = groundFloorInitialKcal
        self.electricityData.groundFloorFinalKcal = groundFloorFinalKcal
        self.electricityData.firstFloorInitialKcal = firstFloorInitialKcal
        self.electricityData.firstFloorFinalKcal = firstFloorFinalKcal

    def updateResultsPage(self, calculationResult):
        summaryText = self.resultFormatter.buildSummaryText(calculationResult)
        detailsText = self.resultFormatter.buildDetailsText(calculationResult)

        self.lastResultsSummaryText = summaryText
        self.lastResultsDetailsText = detailsText

        self.resultsSummaryLabel.setText(summaryText)
        self.resultsDetailsPlainTextEdit.setPlainText(detailsText)

    def populateGeneralDataPage(self):
        self.setLineEditValue(self.totalAmountLineEdit, self.electricityData.totalAmount)
        self.setLineEditValue(self.totalConsumptionLineEdit, self.electricityData.totalConsumption)
        self.groundFloorPeopleSpinBox.setValue(self.electricityData.groundFloorPeople)
        self.firstFloorPeopleSpinBox.setValue(self.electricityData.firstFloorPeople)

    def populateBoilerReadingsPage(self):
        self.setLineEditValue(self.boilerStartReadingLineEdit, self.electricityData.boilerStartReading)
        self.setLineEditValue(self.boilerEndReadingLineEdit, self.electricityData.boilerEndReading)

    def populateControlUnitPage(self):
        self.setComboBoxValue(self.controlUnitModeComboBox, self.electricityData.controlUnitMode)
        self.setLineEditValue(self.groundFloorInitialKcalLineEdit, self.electricityData.groundFloorInitialKcal)
        self.setLineEditValue(self.groundFloorFinalKcalLineEdit, self.electricityData.groundFloorFinalKcal)
        self.setLineEditValue(self.firstFloorInitialKcalLineEdit, self.electricityData.firstFloorInitialKcal)
        self.setLineEditValue(self.firstFloorFinalKcalLineEdit, self.electricityData.firstFloorFinalKcal)

    def handleExportPdf(self):
        print("Export PDF button clicked")

        if self.lastCalculationResult is None:
            self.showWarningMessage(
                "Esportazione PDF",
                "Genera prima i risultati prima di esportare il PDF"
            )
            return

        try:
            outputPath = self.electricityPdfService.export(self.lastCalculationResult)

            self.showInfoMessage(
                "Esportazione completata",
                f"PDF salvato correttamente sul Desktop:\n{outputPath}"
            )

        except Exception as error:
            self.showCriticalMessage(
                "Errore di esportazione",
                f"Impossibile esportare il PDF:\n{error}"
            )