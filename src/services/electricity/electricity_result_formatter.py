class ElectricityResultFormatter:
    def __init__(self, numberFormatter, currencyFormatter):
        self.formatNumber = numberFormatter
        self.formatCurrency = currencyFormatter

    def buildSummaryText(self, calculationResult):
        return (
            f"Consumo caldaia: {self.formatNumber(calculationResult.boilerConsumption)} kWh\n"
            f"Consumo piano terra: {self.formatNumber(calculationResult.groundFloorDirectConsumption)} kWh\n"
            f"Costo per kWh: {self.formatCurrency(calculationResult.costPerKwh)} €/kWh\n"
            f"Totale piano terra: {self.formatCurrency(calculationResult.groundFloorTotal)} €\n"
            f"Totale primo piano: {self.formatCurrency(calculationResult.firstFloorTotal)} €"
        )

    def buildDetailsText(self, calculationResult):
        displayMode = calculationResult.controlUnitMode.capitalize()

        lines = [
            "=== RIPARTIZIONE FINALE BOLLETTA ELETTRICITÀ ===",
            "",
            "=== EQUAZIONI BASE ===",
            (
                f"Consumo caldaia = kWh fine - kWh inizio = "
                f"{self.formatNumber(calculationResult.boilerEndReading)} - "
                f"{self.formatNumber(calculationResult.boilerStartReading)} = "
                f"{self.formatNumber(calculationResult.boilerConsumption)} kWh"
            ),
            (
                f"Consumo piano terra = totale - caldaia = "
                f"{self.formatNumber(calculationResult.totalConsumption)} - "
                f"{self.formatNumber(calculationResult.boilerConsumption)} = "
                f"{self.formatNumber(calculationResult.groundFloorDirectConsumption)} kWh"
            ),
            (
                f"Costo per kWh = importo totale / consumo totale = "
                f"{self.formatCurrency(calculationResult.totalAmount)} / "
                f"{self.formatNumber(calculationResult.totalConsumption)} = "
                f"{self.formatCurrency(calculationResult.costPerKwh)} €/kWh"
            ),
            "",
            "=== RIPARTIZIONE COSTO CALDAIA ===",
            (
                f"Costo totale caldaia = consumo caldaia * costo per kWh = "
                f"{self.formatNumber(calculationResult.boilerConsumption)} * "
                f"{self.formatCurrency(calculationResult.costPerKwh)} = "
                f"{self.formatCurrency(calculationResult.totalBoilerCost)} €"
            ),
            (
                f"Kcal consumate piano terra = kcal finali - kcal iniziali = "
                f"{self.formatNumber(calculationResult.groundFloorFinalKcal)} - "
                f"{self.formatNumber(calculationResult.groundFloorInitialKcal)} = "
                f"{self.formatNumber(calculationResult.groundFloorConsumedKcal)}"
            ),
            (
                f"Kcal consumate primo piano = kcal finali - kcal iniziali = "
                f"{self.formatNumber(calculationResult.firstFloorFinalKcal)} - "
                f"{self.formatNumber(calculationResult.firstFloorInitialKcal)} = "
                f"{self.formatNumber(calculationResult.firstFloorConsumedKcal)}"
            ),
            f"Modalità centralina = {displayMode}",
        ]

        if calculationResult.controlUnitMode == "riscaldamento":
            if calculationResult.groundFloorConsumedKcal != 0 and calculationResult.firstFloorConsumedKcal != 0:
                lines.extend([
                    (
                        f"Costo per kcal = costo totale caldaia / kcal totali = "
                        f"{self.formatCurrency(calculationResult.totalBoilerCost)} / "
                        f"{self.formatNumber(calculationResult.groundFloorConsumedKcal + calculationResult.firstFloorConsumedKcal)} = "
                        f"{self.formatCurrency(calculationResult.boilerCostPerKcal)} €/kcal"
                    ),
                    (
                        f"Costo caldaia piano terra = kcal piano terra * costo per kcal = "
                        f"{self.formatNumber(calculationResult.groundFloorConsumedKcal)} * "
                        f"{self.formatCurrency(calculationResult.boilerCostPerKcal)} = "
                        f"{self.formatCurrency(calculationResult.groundFloorBoilerCost)} €"
                    ),
                    (
                        f"Costo caldaia primo piano = kcal primo piano * costo per kcal = "
                        f"{self.formatNumber(calculationResult.firstFloorConsumedKcal)} * "
                        f"{self.formatCurrency(calculationResult.boilerCostPerKcal)} = "
                        f"{self.formatCurrency(calculationResult.firstFloorBoilerCost)} €"
                    )
                ])
            elif calculationResult.groundFloorConsumedKcal == 0 and calculationResult.firstFloorConsumedKcal == 0:
                lines.extend([
                    (
                        f"Costo per persona = costo totale caldaia / persone totali = "
                        f"{self.formatCurrency(calculationResult.totalBoilerCost)} / "
                        f"{calculationResult.groundFloorPeople + calculationResult.firstFloorPeople} = "
                        f"{self.formatCurrency(calculationResult.boilerCostPerPerson)} €"
                    ),
                    (
                        f"Costo caldaia piano terra = persone piano terra * costo per persona = "
                        f"{calculationResult.groundFloorPeople} * "
                        f"{self.formatCurrency(calculationResult.boilerCostPerPerson)} = "
                        f"{self.formatCurrency(calculationResult.groundFloorBoilerCost)} €"
                    ),
                    (
                        f"Costo caldaia primo piano = persone primo piano * costo per persona = "
                        f"{calculationResult.firstFloorPeople} * "
                        f"{self.formatCurrency(calculationResult.boilerCostPerPerson)} = "
                        f"{self.formatCurrency(calculationResult.firstFloorBoilerCost)} €"
                    )
                ])
            else:
                lines.extend([
                    f"Costo caldaia piano terra = {self.formatCurrency(calculationResult.groundFloorBoilerCost)} €",
                    f"Costo caldaia primo piano = {self.formatCurrency(calculationResult.firstFloorBoilerCost)} €"
                ])
        elif calculationResult.controlUnitMode == "raffrescamento":
            lines.extend([
                f"Costo caldaia piano terra = {self.formatCurrency(calculationResult.groundFloorBoilerCost)} €",
                f"Costo caldaia primo piano = {self.formatCurrency(calculationResult.firstFloorBoilerCost)} €"
            ])

        lines.extend([
            "",
            "=== CALCOLI FINALI ===",
            (
                f"Costo piano terra diretto = consumo piano terra * costo per kWh = "
                f"{self.formatNumber(calculationResult.groundFloorDirectConsumption)} * "
                f"{self.formatCurrency(calculationResult.costPerKwh)} = "
                f"{self.formatCurrency(calculationResult.groundFloorDirectCost)} €"
            ),
            (
                f"Totale piano terra = costo diretto + quota caldaia = "
                f"{self.formatCurrency(calculationResult.groundFloorDirectCost)} + "
                f"{self.formatCurrency(calculationResult.groundFloorBoilerCost)} = "
                f"{self.formatCurrency(calculationResult.groundFloorTotal)} €"
            ),
            (
                f"Totale primo piano = quota caldaia = "
                f"{self.formatCurrency(calculationResult.firstFloorTotal)} €"
            )
        ])

        return "\n".join(lines)