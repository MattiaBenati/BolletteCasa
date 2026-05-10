from src.windows.shared.abstract_window import AbstractWindow


class PeopleBillWindow(AbstractWindow):
    def __init__(self, mainMenuWindow):
        super().__init__()
        self.loadUiFile(self.getUiFileName())

        self.mainMenuWindow = mainMenuWindow
        self.initializeState()
        self.initializeData()
        self.initializeServices()
        self.goToGeneralDataPage()
        self.connectCommonSignals()

    def initializeState(self):
        self.lastResultsSummaryText = ""
        self.lastResultsDetailsText = ""

    def connectCommonSignals(self):
        self.generalDataBackButton.clicked.connect(self.goBackToMainMenu)
        self.resultsBackButton.clicked.connect(self.goBackToMainMenu)
        self.generalDataNextButton.clicked.connect(self.handleGeneralDataNext)
        self.exportPdfButton.clicked.connect(self.handleExportPdf)

    def handleGeneralDataNext(self):
        if not self.saveGeneralData():
            return

        print(f"{self.getModeName()} general data saved:", self.getBillData())
        self.updateResultsPage()
        self.goToResultsPage()

    def handleExportPdf(self):
        try:
            calculationResult = self.getCalculator().calculate(self.getBillData())
            exportedFilePath = self.getPdfExporter().export(self.getBillData(), calculationResult)
            self.showInfoMessage(
                "PDF esportato",
                f"PDF salvato con successo:\n{exportedFilePath}"
            )
        except Exception as error:
            self.showCriticalMessage(
                "Errore di esportazione",
                f"Impossibile esportare il PDF:\n{str(error)}"
            )

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
        billData = self.getBillData()
        billData.totalAmount = totalAmount
        billData.totalConsumption = totalConsumption
        billData.groundFloorPeople = groundFloorPeople
        billData.firstFloorPeople = firstFloorPeople

    def goBackToMainMenu(self):
        print(f"{self.getModeName()}: back to main menu")
        self.mainMenuWindow.show()
        self.close()

    def goToGeneralDataPage(self):
        print(f"{self.getModeName()}: generalDataPage")
        self.populateGeneralDataPage()
        self.getStackedWidget().setCurrentWidget(self.generalDataPage)

    def goToResultsPage(self):
        print(f"{self.getModeName()}: resultsPage")
        self.getStackedWidget().setCurrentWidget(self.resultsPage)

    def populateGeneralDataPage(self):
        billData = self.getBillData()

        self.setLineEditValue(self.totalAmountLineEdit, billData.totalAmount)
        self.setLineEditValue(self.totalConsumptionLineEdit, billData.totalConsumption)
        self.groundFloorPeopleSpinBox.setValue(billData.groundFloorPeople)
        self.firstFloorPeopleSpinBox.setValue(billData.firstFloorPeople)

    def updateResultsPage(self):
        calculationResult = self.getCalculator().calculate(self.getBillData())
        summaryText = self.buildResultsSummaryText(calculationResult)
        detailsText = self.buildResultsDetailsText(calculationResult)

        self.lastResultsSummaryText = summaryText
        self.lastResultsDetailsText = detailsText

        self.resultsSummaryLabel.setText(summaryText)
        self.resultsDetailsPlainTextEdit.setPlainText(detailsText)

    def buildResultsSummaryText(self, calculationResult):
        billData = self.getBillData()

        return (
            f"Importo totale: {self.formatCurrency(billData.totalAmount)} €\n"
            f"Persone totali: {calculationResult.totalPeople}\n"
            f"Quota piano terra: {self.formatCurrency(calculationResult.groundFloorAmount)} €\n"
            f"Quota primo piano: {self.formatCurrency(calculationResult.firstFloorAmount)} €"
        )

    def buildResultsDetailsText(self, calculationResult):
        billData = self.getBillData()
        billLabel = self.getBillLabel()
        billUnitLabel = self.getBillUnitLabel()
        finalTitle = self.getFinalDetailsTitle()

        detailsLines = [
            finalTitle,
            "",
            "=== EQUAZIONI BASE ===",
            (
                f"Persone totali = persone piano terra + persone primo piano = "
                f"{billData.groundFloorPeople} + {billData.firstFloorPeople} = {calculationResult.totalPeople}"
            ),
            (
                f"Costo per persona = importo totale {billLabel} / persone totali = "
                f"{self.formatCurrency(billData.totalAmount)} / {calculationResult.totalPeople} = "
                f"{self.formatCurrency(calculationResult.costPerPerson)} €"
            ),
            "",
            "=== CALCOLI FINALI ===",
            (
                f"Quota piano terra = costo per persona * persone piano terra = "
                f"{self.formatCurrency(calculationResult.costPerPerson)} * {billData.groundFloorPeople} = "
                f"{self.formatCurrency(calculationResult.groundFloorAmount)} €"
            ),
            (
                f"Quota primo piano = costo per persona * persone primo piano = "
                f"{self.formatCurrency(calculationResult.costPerPerson)} * {billData.firstFloorPeople} = "
                f"{self.formatCurrency(calculationResult.firstFloorAmount)} €"
            ),
            "",
            "=== INFORMAZIONI AGGIUNTIVE ===",
            (
                f"Consumo totale {billLabel} = {self.formatNumber(billData.totalConsumption)}"
            ),
            (
                f"Costo per unità = importo totale {billLabel} / consumo totale {billLabel} = "
                f"{self.formatCurrency(billData.totalAmount)} / "
                f"{self.formatNumber(billData.totalConsumption)} = "
                f"{self.formatCurrency(calculationResult.costPerUnit)} {billUnitLabel}"
            )
        ]

        return "\n".join(detailsLines)

    def getUiFileName(self):
        raise NotImplementedError

    def initializeData(self):
        raise NotImplementedError

    def initializeServices(self):
        raise NotImplementedError

    def getModeName(self):
        raise NotImplementedError

    def getBillData(self):
        raise NotImplementedError

    def getCalculator(self):
        raise NotImplementedError

    def getPdfExporter(self):
        raise NotImplementedError

    def getStackedWidget(self):
        raise NotImplementedError

    def getBillLabel(self):
        raise NotImplementedError

    def getBillUnitLabel(self):
        raise NotImplementedError

    def getFinalDetailsTitle(self):
        raise NotImplementedError