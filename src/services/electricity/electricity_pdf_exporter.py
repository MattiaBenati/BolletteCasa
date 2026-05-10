from datetime import datetime
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, PageBreak


class ElectricityPdfExporter:
    def export(self, calculationResult):
        desktopPath = Path.home() / "Desktop"
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        outputPath = desktopPath / f"bolletta_elettricita_{timestamp}.pdf"

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

        self.appendFloorPage(
            story,
            styles,
            pageTitle="Bolletta elettricità : piano terra",
            totalLabel="TOTALE DA PAGARE",
            totalValue=f"{self.formatCurrency(calculationResult.groundFloorTotal)} €",
            exportDate=self.buildExportDate(),
            dataLines=self.buildGroundFloorDataLines(calculationResult),
            calculationLines=self.buildGroundFloorCalculationLines(calculationResult),
            finalVerificationLines=self.buildGroundFloorFinalVerificationLines(calculationResult)
        )

        story.append(PageBreak())

        self.appendFloorPage(
            story,
            styles,
            pageTitle="Bolletta elettricità : primo piano",
            totalLabel="TOTALE DA PAGARE",
            totalValue=f"{self.formatCurrency(calculationResult.firstFloorTotal)} €",
            exportDate=self.buildExportDate(),
            dataLines=self.buildFirstFloorDataLines(calculationResult),
            calculationLines=self.buildFirstFloorCalculationLines(calculationResult),
            finalVerificationLines=self.buildFirstFloorFinalVerificationLines(calculationResult)
        )

        document.build(story)
        return str(outputPath)

    def appendFloorPage(
        self,
        story,
        styles,
        pageTitle,
        totalLabel,
        totalValue,
        exportDate,
        dataLines,
        calculationLines,
        finalVerificationLines
    ):
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

    def buildExportDate(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M")

    def buildGroundFloorDataLines(self, result):
        lines = [
            f"Importo totale energia: {self.formatCurrency(result.totalAmount)} €",
            f"Consumo totale energia: {self.formatNumber(result.totalConsumption)} kWh",
            f"Lettura caldaia inizio primo mese: {self.formatNumber(result.boilerStartReading)} kWh",
            f"Lettura caldaia fine secondo mese: {self.formatNumber(result.boilerEndReading)} kWh",
            f"Modalità centralina: {result.controlUnitMode.capitalize()}"
        ]

        if result.controlUnitMode == "riscaldamento":
            lines.extend([
                f"Kcal iniziali piano terra: {self.formatNumber(result.groundFloorInitialKcal)}",
                f"Kcal finali piano terra: {self.formatNumber(result.groundFloorFinalKcal)}",
                f"Kcal iniziali primo piano: {self.formatNumber(result.firstFloorInitialKcal)}",
                f"Kcal finali primo piano: {self.formatNumber(result.firstFloorFinalKcal)}"
            ])

        return lines

    def buildFirstFloorDataLines(self, result):
        lines = [
            f"Importo totale energia: {self.formatCurrency(result.totalAmount)} €",
            f"Consumo totale energia: {self.formatNumber(result.totalConsumption)} kWh",
            f"Lettura caldaia inizio primo mese: {self.formatNumber(result.boilerStartReading)} kWh",
            f"Lettura caldaia fine secondo mese: {self.formatNumber(result.boilerEndReading)} kWh",
            f"Modalità centralina: {result.controlUnitMode.capitalize()}"
        ]

        if result.controlUnitMode == "riscaldamento":
            lines.extend([
                f"Kcal iniziali piano terra: {self.formatNumber(result.groundFloorInitialKcal)}",
                f"Kcal finali piano terra: {self.formatNumber(result.groundFloorFinalKcal)}",
                f"Kcal iniziali primo piano: {self.formatNumber(result.firstFloorInitialKcal)}",
                f"Kcal finali primo piano: {self.formatNumber(result.firstFloorFinalKcal)}"
            ])

        return lines

    def buildGroundFloorCalculationLines(self, result):
        lines = [
            (
                f"Consumo caldaia = lettura finale caldaia - lettura iniziale caldaia = "
                f"{self.formatNumber(result.boilerEndReading)} - {self.formatNumber(result.boilerStartReading)} = "
                f"{self.formatNumber(result.boilerConsumption)} kWh"
            ),
            (
                f"Consumo piano terra diretto = consumo totale energia - consumo caldaia = "
                f"{self.formatNumber(result.totalConsumption)} - {self.formatNumber(result.boilerConsumption)} = "
                f"{self.formatNumber(result.groundFloorDirectConsumption)} kWh"
            ),
            (
                f"Costo per kWh = importo totale energia / consumo totale energia = "
                f"{self.formatCurrency(result.totalAmount)} / {self.formatNumber(result.totalConsumption)} = "
                f"{self.formatCurrency(result.costPerKwh)} €/kWh"
            ),
            (
                f"Costo diretto piano terra = consumo piano terra diretto * costo per kWh = "
                f"{self.formatNumber(result.groundFloorDirectConsumption)} * {self.formatCurrency(result.costPerKwh)} = "
                f"{self.formatCurrency(result.groundFloorDirectCost)} €"
            )
        ]

        if result.controlUnitMode == "riscaldamento":
            lines.extend(self.buildHeatingGroundFloorLines(result))
        elif result.controlUnitMode == "raffrescamento":
            lines.extend(self.buildCoolingGroundFloorLines(result))

        return lines

    def buildFirstFloorCalculationLines(self, result):
        lines = [
            (
                f"Consumo caldaia = lettura finale caldaia - lettura iniziale caldaia = "
                f"{self.formatNumber(result.boilerEndReading)} - {self.formatNumber(result.boilerStartReading)} = "
                f"{self.formatNumber(result.boilerConsumption)} kWh"
            ),
            (
                f"Costo per kWh = importo totale energia / consumo totale energia = "
                f"{self.formatCurrency(result.totalAmount)} / {self.formatNumber(result.totalConsumption)} = "
                f"{self.formatCurrency(result.costPerKwh)} €/kWh"
            ),
            (
                f"Costo totale caldaia = consumo caldaia * costo per kWh = "
                f"{self.formatNumber(result.boilerConsumption)} * {self.formatCurrency(result.costPerKwh)} = "
                f"{self.formatCurrency(result.totalBoilerCost)} €"
            )
        ]

        if result.controlUnitMode == "riscaldamento":
            lines.extend(self.buildHeatingFirstFloorLines(result))
        elif result.controlUnitMode == "raffrescamento":
            lines.extend(self.buildCoolingFirstFloorLines(result))

        return lines

    def buildHeatingGroundFloorLines(self, result):
        lines = [
            (
                f"Kcal consumate piano terra = kcal finali piano terra - kcal iniziali piano terra = "
                f"{self.formatNumber(result.groundFloorFinalKcal)} - {self.formatNumber(result.groundFloorInitialKcal)} = "
                f"{self.formatNumber(result.groundFloorConsumedKcal)}"
            ),
            (
                f"Kcal consumate primo piano = kcal finali primo piano - kcal iniziali primo piano = "
                f"{self.formatNumber(result.firstFloorFinalKcal)} - {self.formatNumber(result.firstFloorInitialKcal)} = "
                f"{self.formatNumber(result.firstFloorConsumedKcal)}"
            ),
            (
                f"Costo totale caldaia = consumo caldaia * costo per kWh = "
                f"{self.formatNumber(result.boilerConsumption)} * {self.formatCurrency(result.costPerKwh)} = "
                f"{self.formatCurrency(result.totalBoilerCost)} €"
            )
        ]

        if result.groundFloorConsumedKcal != 0 and result.firstFloorConsumedKcal != 0:
            lines.extend([
                (
                    f"Costo per kcal = costo totale caldaia / (kcal consumate piano terra + kcal consumate primo piano) = "
                    f"{self.formatCurrency(result.totalBoilerCost)} / "
                    f"({self.formatNumber(result.groundFloorConsumedKcal)} + {self.formatNumber(result.firstFloorConsumedKcal)}) = "
                    f"{self.formatCurrency(result.boilerCostPerKcal)} €/kcal"
                ),
                (
                    f"Quota caldaia piano terra = kcal consumate piano terra * costo per kcal = "
                    f"{self.formatNumber(result.groundFloorConsumedKcal)} * {self.formatCurrency(result.boilerCostPerKcal)} = "
                    f"{self.formatCurrency(result.groundFloorBoilerCost)} €"
                )
            ])
        elif result.groundFloorConsumedKcal == 0 and result.firstFloorConsumedKcal == 0:
            totalPeople = result.groundFloorPeople + result.firstFloorPeople
            lines.extend([
                (
                    f"Costo per persona = costo totale caldaia / persone totali = "
                    f"{self.formatCurrency(result.totalBoilerCost)} / {totalPeople} = "
                    f"{self.formatCurrency(result.boilerCostPerPerson)} €"
                ),
                (
                    f"Quota caldaia piano terra = persone piano terra * costo per persona = "
                    f"{result.groundFloorPeople} * {self.formatCurrency(result.boilerCostPerPerson)} = "
                    f"{self.formatCurrency(result.groundFloorBoilerCost)} €"
                )
            ])
        else:
            if result.groundFloorConsumedKcal != 0:
                lines.append(
                    f"Quota caldaia piano terra = costo totale caldaia = {self.formatCurrency(result.groundFloorBoilerCost)} €"
                )
            else:
                lines.append(
                    f"Quota caldaia piano terra = 0.00 €"
                )

        return lines

    def buildHeatingFirstFloorLines(self, result):
        lines = [
            (
                f"Kcal consumate piano terra = kcal finali piano terra - kcal iniziali piano terra = "
                f"{self.formatNumber(result.groundFloorFinalKcal)} - {self.formatNumber(result.groundFloorInitialKcal)} = "
                f"{self.formatNumber(result.groundFloorConsumedKcal)}"
            ),
            (
                f"Kcal consumate primo piano = kcal finali primo piano - kcal iniziali primo piano = "
                f"{self.formatNumber(result.firstFloorFinalKcal)} - {self.formatNumber(result.firstFloorInitialKcal)} = "
                f"{self.formatNumber(result.firstFloorConsumedKcal)}"
            )
        ]

        if result.groundFloorConsumedKcal != 0 and result.firstFloorConsumedKcal != 0:
            lines.extend([
                (
                    f"Costo per kcal = costo totale caldaia / (kcal consumate piano terra + kcal consumate primo piano) = "
                    f"{self.formatCurrency(result.totalBoilerCost)} / "
                    f"({self.formatNumber(result.groundFloorConsumedKcal)} + {self.formatNumber(result.firstFloorConsumedKcal)}) = "
                    f"{self.formatCurrency(result.boilerCostPerKcal)} €/kcal"
                ),
                (
                    f"Quota caldaia primo piano = kcal consumate primo piano * costo per kcal = "
                    f"{self.formatNumber(result.firstFloorConsumedKcal)} * {self.formatCurrency(result.boilerCostPerKcal)} = "
                    f"{self.formatCurrency(result.firstFloorBoilerCost)} €"
                )
            ])
        elif result.groundFloorConsumedKcal == 0 and result.firstFloorConsumedKcal == 0:
            totalPeople = result.groundFloorPeople + result.firstFloorPeople
            lines.extend([
                (
                    f"Costo per persona = costo totale caldaia / persone totali = "
                    f"{self.formatCurrency(result.totalBoilerCost)} / {totalPeople} = "
                    f"{self.formatCurrency(result.boilerCostPerPerson)} €"
                ),
                (
                    f"Quota caldaia primo piano = persone primo piano * costo per persona = "
                    f"{result.firstFloorPeople} * {self.formatCurrency(result.boilerCostPerPerson)} = "
                    f"{self.formatCurrency(result.firstFloorBoilerCost)} €"
                )
            ])
        else:
            if result.firstFloorConsumedKcal != 0:
                lines.append(
                    f"Quota caldaia primo piano = costo totale caldaia = {self.formatCurrency(result.firstFloorBoilerCost)} €"
                )
            else:
                lines.append(
                    f"Quota caldaia primo piano = 0.00 €"
                )

        return lines

    def buildCoolingGroundFloorLines(self, result):
        return [
            (
                f"Costo totale caldaia = consumo caldaia * costo per kWh = "
                f"{self.formatNumber(result.boilerConsumption)} * {self.formatCurrency(result.costPerKwh)} = "
                f"{self.formatCurrency(result.totalBoilerCost)} €"
            ),
            "Quota caldaia piano terra = 0.00 €"
        ]

    def buildCoolingFirstFloorLines(self, result):
        return [
            (
                f"Quota caldaia primo piano = costo totale caldaia = "
                f"{self.formatCurrency(result.totalBoilerCost)} €"
            )
        ]

    def buildGroundFloorFinalVerificationLines(self, result):
        return [
            (
                f"Totale piano terra = costo diretto piano terra + quota caldaia piano terra = "
                f"{self.formatCurrency(result.groundFloorDirectCost)} + {self.formatCurrency(result.groundFloorBoilerCost)} = "
                f"{self.formatCurrency(result.groundFloorTotal)} €"
            )
        ]

    def buildFirstFloorFinalVerificationLines(self, result):
        if result.controlUnitMode == "raffrescamento":
            return [
                (
                    f"Totale primo piano = quota caldaia primo piano = "
                    f"{self.formatCurrency(result.firstFloorTotal)} €"
                )
            ]

        return [
            (
                f"Totale primo piano = quota caldaia primo piano = "
                f"{self.formatCurrency(result.firstFloorTotal)} €"
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
            "metaLine": ParagraphStyle(
                "metaLine",
                parent=sampleStyles["Normal"],
                fontName="Helvetica",
                fontSize=10,
                leading=13,
                textColor=HexColor("#4B5563"),
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