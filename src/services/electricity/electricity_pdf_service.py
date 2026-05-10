from src.services.electricity.electricity_pdf_exporter import ElectricityPdfExporter


class ElectricityPdfService:
    def export(self, calculationResult):
        exporter = ElectricityPdfExporter()
        return exporter.export(calculationResult)