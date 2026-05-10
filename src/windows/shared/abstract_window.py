import os
from PyQt6 import uic
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QMessageBox

from src.config.app_paths import ASSETS_DIR, UI_DIR


class AbstractWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.applyWindowIcon()

    def applyWindowIcon(self):
        self.setWindowIcon(QIcon(os.path.join(ASSETS_DIR, "logo.ico")))

    def loadUiFile(self, uiFileName):
        uic.loadUi(os.path.join(UI_DIR, uiFileName), self)
        self.applyWindowIcon()  # 🔥 fondamentale: riapplica dopo loadUi

    def parsePositiveFloat(self, rawValue, errorMessage):
        normalizedValue = rawValue.strip().replace(",", ".")

        if not normalizedValue:
            raise ValueError(errorMessage)

        try:
            parsedValue = float(normalizedValue)
        except ValueError as error:
            raise ValueError(errorMessage) from error

        if parsedValue <= 0:
            raise ValueError(errorMessage)

        return parsedValue

    def parseNonNegativeFloat(self, rawValue, errorMessage):
        normalizedValue = rawValue.strip().replace(",", ".")

        if not normalizedValue:
            raise ValueError(errorMessage)

        try:
            parsedValue = float(normalizedValue)
        except ValueError as error:
            raise ValueError(errorMessage) from error

        if parsedValue < 0:
            raise ValueError("Il valore non può essere negativo")

        return parsedValue

    def showValidationError(self, message):
        self.showWarningMessage("Errore di input", message)

    def showWarningMessage(self, title, message):
        QMessageBox.warning(self, title, message)

    def showInfoMessage(self, title, message):
        QMessageBox.information(self, title, message)

    def showCriticalMessage(self, title, message):
        QMessageBox.critical(self, title, message)

    def formatNumber(self, value):
        return f"{value:.2f}"

    def formatCurrency(self, value):
        return f"{value:.2f}"

    def formatInputNumber(self, value):
        if float(value).is_integer():
            return str(int(value))
        return str(value)

    def setLineEditValue(self, lineEdit, value):
        if value is not None:
            lineEdit.setText(self.formatInputNumber(value))
        else:
            lineEdit.clear()

    def setComboBoxValue(self, comboBox, value):
        if value:
            index = comboBox.findText(value)
            if index >= 0:
                comboBox.setCurrentIndex(index)