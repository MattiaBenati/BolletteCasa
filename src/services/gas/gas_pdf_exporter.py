from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak

from src.models.gas.gas_data import GasData
from src.models.gas.gas_calculation_result import GasCalculationResult


class GasPdfExporter:
    def export(self, gasData: GasData, calculationResult: GasCalculationResult):
        desktopPath = Path.home() / "Desktop"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        outputPath = desktopPath / f"bolletta_gas_{timestamp}.pdf"

        document = SimpleDocTemplate(
            str(outputPath),
            pagesize=A4,
            leftMargin=42,
            rightMargin=42,
            topMargin=42,
            bottomMargin=42
        )

        styles = self.buildStyles()
        story = []

        story.append(self.buildFloorPage(
            styles=styles,
            pageTitle="Bolletta gas : piano terra",
            totalLabel="TOTALE DA PAGARE",
            totalValue=f"{self.formatCurrency(calculationResult.groundFloorAmount)} €",
            dataLines=self.buildGroundFloorDataLines(gasData, calculationResult),
            calculationLines=self.buildGroundFloorCalculationLines(gasData, calculationResult),
            finalVerificationLines=self.buildGroundFloorFinalVerificationLines(gasData, calculationResult)
        ))

        story.append(PageBreak())

        story.append(self.buildFloorPage(
            styles=styles,
            pageTitle="Bolletta gas : primo piano",
            totalLabel="TOTALE DA PAGARE",
            totalValue=f"{self.formatCurrency(calculationResult.firstFloorAmount)} €",
            dataLines=self.buildFirstFloorDataLines(gasData, calculationResult),
            calculationLines=self.buildFirstFloorCalculationLines(gasData, calculationResult),
            finalVerificationLines=self.buildFirstFloorFinalVerificationLines(gasData, calculationResult)
        ))

        flattenedStory = []
        for pagePart in story:
            if isinstance(pagePart, list):
                flattenedStory.extend(pagePart)
            else:
                flattenedStory.append(pagePart)

        document.build(flattenedStory)
        return str(outputPath)

    def buildFloorPage(
        self,
        styles,
        pageTitle,
        totalLabel,
        totalValue,
        dataLines,
        calculationLines,
        finalVerificationLines
    ):
        story = []

        story.append(Paragraph(escape(pageTitle), styles["mainTitle"]))
        story.append(Spacer(1, 16))

        story.append(Paragraph(escape(totalLabel), styles["totalLabel"]))
        story.append(Spacer(1, 4))
        story.append(Paragraph(escape(totalValue), styles["totalValue"]))
        story.append(Spacer(1, 10))

        self.appendDivider(story, styles)
        self.appendSection(story, styles, "DATI UTILIZZATI", dataLines)
        self.appendDivider(story, styles)
        self.appendSection(story, styles, "CALCOLI", calculationLines)
        self.appendDivider(story, styles)
        self.appendSection(story, styles, "VERIFICA FINALE", finalVerificationLines)

        return story

    def appendSection(self, story, styles, sectionTitle, lines):
        story.append(Paragraph(escape(sectionTitle), styles["sectionTitle"]))
        story.append(Spacer(1, 8))

        for line in lines:
            if not line:
                story.append(Spacer(1, 6))
                continue

            story.append(Paragraph(escape(line), styles["bodyLine"]))
            story.append(Spacer(1, 5))

        story.append(Spacer(1, 10))

    def appendDivider(self, story, styles):
        story.append(Paragraph("_" * 110, styles["divider"]))
        story.append(Spacer(1, 10))

    def buildGroundFloorDataLines(self, gasData: GasData, result: GasCalculationResult):
        return [
            f"Importo totale gas: {self.formatCurrency(gasData.totalAmount)} €",
            f"Consumo totale gas: {self.formatNumber(gasData.totalConsumption)}",
            f"Numero persone piano terra: {gasData.groundFloorPeople}",
            f"Numero persone primo piano: {gasData.firstFloorPeople}",
            f"Numero persone totali: {result.totalPeople}"
        ]

    def buildFirstFloorDataLines(self, gasData: GasData, result: GasCalculationResult):
        return [
            f"Importo totale gas: {self.formatCurrency(gasData.totalAmount)} €",
            f"Consumo totale gas: {self.formatNumber(gasData.totalConsumption)}",
            f"Numero persone piano terra: {gasData.groundFloorPeople}",
            f"Numero persone primo piano: {gasData.firstFloorPeople}",
            f"Numero persone totali: {result.totalPeople}"
        ]

    def buildGroundFloorCalculationLines(self, gasData: GasData, result: GasCalculationResult):
        return [
            (
                f"Persone totali = persone piano terra + persone primo piano = "
                f"{gasData.groundFloorPeople} + {gasData.firstFloorPeople} = {result.totalPeople}"
            ),
            (
                f"Costo per persona = importo totale gas / persone totali = "
                f"{self.formatCurrency(gasData.totalAmount)} / {result.totalPeople} = "
                f"{self.formatCurrency(result.costPerPerson)} €"
            ),
            (
                f"Costo per unità = importo totale gas / consumo totale gas = "
                f"{self.formatCurrency(gasData.totalAmount)} / {self.formatNumber(gasData.totalConsumption)} = "
                f"{self.formatCurrency(result.costPerUnit)} €/unità"
            ),
            (
                f"Quota piano terra = persone piano terra * costo per persona = "
                f"{gasData.groundFloorPeople} * {self.formatCurrency(result.costPerPerson)} = "
                f"{self.formatCurrency(result.groundFloorAmount)} €"
            )
        ]

    def buildFirstFloorCalculationLines(self, gasData: GasData, result: GasCalculationResult):
        return [
            (
                f"Persone totali = persone piano terra + persone primo piano = "
                f"{gasData.groundFloorPeople} + {gasData.firstFloorPeople} = {result.totalPeople}"
            ),
            (
                f"Costo per persona = importo totale gas / persone totali = "
                f"{self.formatCurrency(gasData.totalAmount)} / {result.totalPeople} = "
                f"{self.formatCurrency(result.costPerPerson)} €"
            ),
            (
                f"Costo per unità = importo totale gas / consumo totale gas = "
                f"{self.formatCurrency(gasData.totalAmount)} / {self.formatNumber(gasData.totalConsumption)} = "
                f"{self.formatCurrency(result.costPerUnit)} €/unità"
            ),
            (
                f"Quota primo piano = persone primo piano * costo per persona = "
                f"{gasData.firstFloorPeople} * {self.formatCurrency(result.costPerPerson)} = "
                f"{self.formatCurrency(result.firstFloorAmount)} €"
            )
        ]

    def buildGroundFloorFinalVerificationLines(self, gasData: GasData, result: GasCalculationResult):
        return [
            (
                f"Totale piano terra = quota piano terra = "
                f"{self.formatCurrency(result.groundFloorAmount)} €"
            )
        ]

    def buildFirstFloorFinalVerificationLines(self, gasData: GasData, result: GasCalculationResult):
        return [
            (
                f"Totale primo piano = quota primo piano = "
                f"{self.formatCurrency(result.firstFloorAmount)} €"
            )
        ]

    def buildStyles(self):
        sampleStyles = getSampleStyleSheet()

        return {
            "mainTitle": ParagraphStyle(
                "mainTitle",
                parent=sampleStyles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=20,
                leading=24,
                textColor=HexColor("#111827"),
                alignment=TA_CENTER
            ),
            "totalLabel": ParagraphStyle(
                "totalLabel",
                parent=sampleStyles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=12,
                leading=15,
                textColor=HexColor("#374151"),
                alignment=TA_CENTER
            ),
            "totalValue": ParagraphStyle(
                "totalValue",
                parent=sampleStyles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=24,
                leading=28,
                textColor=HexColor("#111827"),
                alignment=TA_CENTER
            ),
            "sectionTitle": ParagraphStyle(
                "sectionTitle",
                parent=sampleStyles["Normal"],
                fontName="Helvetica-Bold",
                fontSize=13,
                leading=16,
                textColor=HexColor("#111827"),
                alignment=TA_LEFT
            ),
            "bodyLine": ParagraphStyle(
                "bodyLine",
                parent=sampleStyles["Normal"],
                fontName="Helvetica",
                fontSize=10.5,
                leading=14,
                textColor=HexColor("#111827"),
                alignment=TA_LEFT
            ),
            "divider": ParagraphStyle(
                "divider",
                parent=sampleStyles["Normal"],
                fontName="Helvetica",
                fontSize=6,
                leading=6,
                textColor=HexColor("#9CA3AF"),
                alignment=TA_CENTER
            )
        }

    def formatNumber(self, value):
        return f"{value:.2f}"

    def formatCurrency(self, value):
        return f"{value:.2f}"