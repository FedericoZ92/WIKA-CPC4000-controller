# WIKA CPC4000 Cycle UI

This project provides a graphical user interface (GUI) for automating pressure cycling tests on the WIKA CPC4000 pressure controller via serial communication.

## Features
- Automatically detects available COM ports and pre-fills the serial port field
- Allows user to configure test parameters:
  - Serial port (COM)
  - Baudrate
  - Number of cycles
  - Hold time per cycle
  - Target pressure A
  - Target pressure B
- Runs a pressure cycling test, alternating between two target pressures for a specified number of cycles
- Displays error messages for connection issues or invalid input

## Requirements
- Python 3.x
- pyserial
- Tkinter (usually included with Python)

## Usage
1. Install dependencies:
   ```bash
   pip install pyserial
   ```
2. Run the UI script:
   ```bash
   python wika-cpc4000-cycle-UI.py
   ```
3. Configure the test parameters in the GUI and click "Avvia Test" to start.

## Files
- `wika-cpc4000-cycle-UI.py`: Main GUI application

## Notes
- The application will attempt to detect the first available COM port automatically, but you can change it in the UI.
- Ensure the CPC4000 device is connected and powered on before starting the test.

## License

## Generating an Executable

To create a standalone executable for Windows using PyInstaller:

**Important:** Always activate your virtual environment before generating the executable. This ensures the correct dependencies are included.

1. Activate your virtual environment:
   ```powershell
   .\.venv\Scripts\activate
   ```
2. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
3. Generate the executable:
   ```bash
   pyinstaller --onefile wika-cpc4000-cycle-UI.py
   ```
4. The executable will be created in the `dist` folder. You can distribute this `.exe` file to users who do not have Python installed.
This project is provided as-is for educational and automation purposes.
