# BolletteCasa

Desktop utility bill calculation application developed in Python with PyQt6, Qt Designer interfaces, PDF export, and PyInstaller packaging support.

![Python](https://img.shields.io/badge/Python-Programming-blue)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green)
![Qt Designer](https://img.shields.io/badge/UI-Qt%20Designer-lightgrey)
![ReportLab](https://img.shields.io/badge/PDF-ReportLab-orange)
![PyInstaller](https://img.shields.io/badge/Packaging-PyInstaller-yellow)
![Desktop App](https://img.shields.io/badge/Application-Desktop%20App-informational)

## Demo

https://github.com/user-attachments/assets/48dadf6c-de9e-490a-9236-6c9dbe8dbc86

## What is it?

BolletteCasa is a desktop application designed to calculate and split household utility bills between two apartments: ground floor and first floor.

The software supports three bill types: electricity, gas, and water.

Each module guides the user through the required input data, validates the inserted values, calculates the amount due for each floor, displays a detailed calculation summary, and allows the result to be exported as a PDF file.

The project is organized into separate modules for data models, calculation services, PDF export services, graphical windows, shared window logic, application paths, UI files, and assets.

## Features

- Desktop graphical user interface
- Main menu with electricity, gas, and water modules
- Electricity bill calculation
- Gas bill calculation
- Water bill calculation
- Split calculation between ground floor and first floor
- Input validation for amounts, consumption values, readings, people count, and control unit values
- Electricity calculation based on total consumption, boiler consumption, and control unit data
- Heating and cooling mode support for electricity calculation
- Gas and water split based on the number of people per floor
- Detailed result summary
- Detailed calculation explanation
- PDF export for electricity results
- PDF export for gas results
- PDF export for water results
- Automatic PDF saving on the Desktop
- Timestamped PDF file names
- Custom application icon
- Qt Designer `.ui` files for interface layout
- PyInstaller `.spec` file for executable generation
- Modular Python source code organization

## Key Technical Aspects

- PyQt6-based desktop interface
- Qt Designer `.ui` files loaded dynamically at runtime
- Shared abstract window for common UI behavior
- Shared base window for gas and water bill workflows
- Separate window class for the more complex electricity workflow
- Dataclass-based data models for bill input and calculation results
- Service-based architecture for calculations and PDF export
- ReportLab-based PDF generation
- Automatic Desktop output path resolution
- Input normalization with comma-to-dot decimal conversion
- Separation between UI logic, calculation logic, data models, and export logic
- Resource path management for UI files and assets
- PyInstaller configuration for packaging the application as a desktop executable

## Technology Stack

- Python
- PyQt6
- Qt Designer
- Qt `.ui` files
- ReportLab
- PyInstaller
- dataclasses
- pathlib
- CMake is not used in this project
- PyCharm or another Python-compatible IDE

## Requirements

- Python 3.10 or later
- PyQt6
- ReportLab
- PyInstaller, only if building the executable
- Windows operating system recommended for the packaged executable

## Quick Start

### Clone the repository

```bash
git clone https://github.com/MattiaBenati/BolletteCasa.git
cd BolletteCasa
```

### Install dependencies

Install the required Python packages:

```bash
pip install PyQt6 reportlab
```

Install PyInstaller only if you want to generate the executable:

```bash
pip install pyinstaller
```

### Run the application

Run the application from the project root:

```bash
python -m src.main
```

### Build the executable

Build the executable using the existing PyInstaller specification file:

```bash
pyinstaller BolletteCasa.spec
```

The generated executable will be created inside the `dist/` directory.

## Usage

1. Start the application
2. Choose one of the available bill types from the main menu
3. Insert the required bill data
4. Continue through the guided steps
5. Review the calculated result
6. Export the result as a PDF file if needed
7. Return to the main menu to calculate another bill type

## Bill Modules

### Electricity

The electricity module manages a multi-step calculation workflow.

The user inserts the total amount, total electricity consumption, people count for each floor, boiler meter readings, control unit mode, and kcal values for both floors.

The software calculates boiler consumption, direct ground floor consumption, cost per kWh, boiler cost distribution, and the final amount due for each floor.

### Gas

The gas module calculates the bill split between the two floors based on the total amount and the number of people living on each floor.

The software also calculates the cost per person and the cost per consumption unit.

### Water

The water module follows the same people-based calculation structure used for gas.

The software calculates the amount due for each floor, the cost per person, and the cost per consumption unit.

## Controls

| Control | Action |
| --- | --- |
| `Electricity` | Open the electricity bill calculation module |
| `Gas` | Open the gas bill calculation module |
| `Water` | Open the water bill calculation module |
| `Next` | Continue to the next step |
| `Back` | Return to the previous screen or main menu |
| `Export PDF` | Export the calculated result as a PDF file |

## Project Structure

```text
BolletteCasa/
├── BolletteCasa.spec
└── src/
    ├── assets/
    │   ├── logo.ico
    │   └── logo.png
    ├── config/
    │   └── app_paths.py
    ├── models/
    │   ├── electricity/
    │   │   └── electricity_data.py
    │   ├── gas/
    │   │   ├── gas_calculation_result.py
    │   │   └── gas_data.py
    │   └── water/
    │       ├── water_calculation_result.py
    │       └── water_data.py
    ├── services/
    │   ├── electricity/
    │   │   ├── electricity_calculation_service.py
    │   │   ├── electricity_calculator.py
    │   │   ├── electricity_pdf_exporter.py
    │   │   ├── electricity_pdf_service.py
    │   │   └── electricity_result_formatter.py
    │   ├── gas/
    │   │   ├── gas_calculator.py
    │   │   └── gas_pdf_exporter.py
    │   └── water/
    │       ├── water_calculator.py
    │       └── water_pdf_exporter.py
    ├── ui/
    │   ├── electricity_window.ui
    │   ├── gas_window.ui
    │   ├── main_menu.ui
    │   └── water_window.ui
    ├── windows/
    │   ├── shared/
    │   │   ├── abstract_window.py
    │   │   └── people_bill_window.py
    │   ├── electricity_window.py
    │   ├── gas_window.py
    │   ├── home_window.py
    │   └── water_window.py
    └── main.py
```

## Architecture Overview

The project follows a modular Python structure with a clear separation between user interface, data models, calculation services, PDF export logic, and shared window behavior.

- `src/main.py`: starts the PyQt6 application and opens the home window
- `src/config/app_paths.py`: defines project paths for UI files and assets
- `src/windows/home_window.py`: manages the main menu and opens the selected bill module
- `src/windows/electricity_window.py`: manages the electricity workflow, validation, calculation, result display, and PDF export
- `src/windows/gas_window.py`: manages the gas calculation window using the shared people-based bill workflow
- `src/windows/water_window.py`: manages the water calculation window using the shared people-based bill workflow
- `src/windows/shared/abstract_window.py`: provides common window behavior, UI loading, icon handling, formatting, parsing, and message dialogs
- `src/windows/shared/people_bill_window.py`: provides shared behavior for bill modules based on people count
- `src/models/`: contains dataclasses used to store input data and calculation results
- `src/services/electricity/`: contains electricity calculation, result formatting, and PDF export logic
- `src/services/gas/`: contains gas calculation and PDF export logic
- `src/services/water/`: contains water calculation and PDF export logic
- `src/ui/`: contains Qt Designer `.ui` files
- `src/assets/`: contains the application logo and icon files
- `BolletteCasa.spec`: defines the PyInstaller build configuration for packaging the software as a desktop executable

## Output

The software displays a graphical desktop interface built with PyQt6.

During execution, it shows guided input screens, validation messages, result summaries, detailed calculation explanations, and PDF export confirmation messages.

The exported PDF files are saved on the Desktop with timestamped file names:

- `bolletta_elettricita_YYYYMMDD_HHMMSS.pdf`
- `bolletta_gas_YYYYMMDD_HHMMSS.pdf`
- `bolletta_acqua_YYYYMMDD_HHMMSS.pdf`

Each PDF contains the calculated amount for the ground floor and first floor, the input values used, the calculation steps, and the final verification.

https://github.com/user-attachments/assets/e3175bbd-e76b-4a48-81d1-e22e38fe3e1f

