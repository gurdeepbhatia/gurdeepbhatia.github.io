# Building Chart Preparation Utility as Windows EXE

This guide explains how to build the Chart Preparation Utility as a standalone Windows executable.

## Prerequisites

### System Requirements
- **Windows Operating System** (Windows 10 or later recommended)
- **Python 3.8 or later** installed
- All dependencies from `requirements.txt`

### Why Windows?

PyInstaller bundles platform-specific dependencies. **Building on Mac or Linux will not produce a working Windows executable.** You must build on Windows or use a Windows VM.

## Installation

### 1. Install Python Dependencies

Open Command Prompt or PowerShell in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- openpyxl (Excel file generation)
- PyInstaller (executable builder)
- pywin32 (Windows-specific functionality)

## Building the Executable

### Option 1: Using the Build Script (Recommended)

Simply run:

```bash
python build.py
```

The script will:
- Clean old build directories
- Run PyInstaller with the correct configuration
- Report success or failure
- Show the location of the generated exe

### Option 2: Manual Build

If you prefer to build manually:

```bash
pyinstaller ChartPreparation.spec --clean
```

## Output

After a successful build:

- **Executable location:** `dist/ChartPreparation.exe`
- **File size:** Approximately 50-100 MB
- **Contents:** Includes Python interpreter, Flask, all dependencies, templates, static files, and CSV symbol files

## Testing the Executable

1. Navigate to the `dist` folder
2. Double-click `ChartPreparation.exe`
3. A console window should appear with startup messages
4. Your default browser should automatically open to the application
5. Test both Daily Chart and Index Chart functionality
6. Close the browser - the server should shutdown automatically after 5 seconds
7. Check the version number displayed in the bottom-right corner

### Test Checklist

- [ ] Exe runs without errors
- [ ] Browser opens automatically
- [ ] Console shows "Version 1" in startup messages
- [ ] Version "1" displayed in web UI
- [ ] Upload Daily CSV (e.g., sec_bhavdata_full*.csv)
- [ ] Generate Daily Chart Excel file
- [ ] Upload Index CSV (e.g., MW-All-Indices*.csv)
- [ ] Generate Index Chart Excel file
- [ ] Verify Excel files created in Downloads folder
- [ ] Close browser and verify server shuts down
- [ ] Check Windows file properties - verify version metadata

## Distributing to Users

### What to Distribute

Only the executable file:
- `dist/ChartPreparation.exe` (rename if needed, but not required)

### Installation Instructions for End Users

Send these instructions to your users:

```
Chart Preparation Utility - Quick Start

1. Download ChartPreparation.exe
2. Save it to any folder (e.g., Desktop or Documents)
3. Double-click the exe to run
4. The application will open in your browser automatically
5. Upload your CSV file and generate charts
6. Excel files will be saved to your Downloads folder
7. Close the browser when done - the server will stop automatically

No installation required. No dependencies needed.
```

### Security Note

Windows Defender or antivirus software may flag the exe as suspicious (false positive). This is common with PyInstaller executables. Users may need to:
- Add an exception in Windows Defender
- Click "More Info" → "Run Anyway" when SmartScreen warning appears

## Updating to a New Version

### For Developers

1. Make your code changes
2. Update the version number in `config.py`:
   ```python
   VERSION = "2"  # Change from "1" to "2"
   ```
3. Update version metadata in `file_version_info.txt`:
   - Update `filevers=(2, 0, 0, 0)`
   - Update `prodvers=(2, 0, 0, 0)`
   - Update `FileVersion` and `ProductVersion` strings
4. Rebuild: `python build.py`
5. Test the new executable
6. Distribute `ChartPreparation.exe` to users

### For End Users

Simply:
1. Download the new `ChartPreparation.exe`
2. Delete the old exe
3. Use the new exe

The filename stays the same: `ChartPreparation.exe`

## Troubleshooting

### Build Fails with "PyInstaller not found"

```bash
pip install pyinstaller
```

### Build Fails with Import Errors

Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### Exe Fails to Run on Target Machine

**Check:**
- Is it Windows 10 or later?
- Are you running the exe that was built on Windows?
- Try running from Command Prompt to see error messages:
  ```
  cd path\to\exe
  ChartPreparation.exe
  ```

### Browser Doesn't Open Automatically

The exe still works. Manually open your browser and go to:
```
http://127.0.0.1:5000
```

### Server Doesn't Shutdown When Browser Closes

Press `Ctrl+C` in the console window to manually stop the server.

### Version Number Not Showing

Check the browser console (F12) for JavaScript errors. The version is fetched from `/api/version` endpoint.

### Large File Size (100+ MB)

This is normal. The exe includes:
- Python interpreter
- Flask web framework
- openpyxl library
- All templates and static files
- CSV symbol files

You can reduce size by:
- Using UPX compression (already enabled in spec file)
- Excluding unnecessary modules (requires spec file customization)

## Advanced Configuration

### Changing the Icon

1. Create or download a `.ico` file
2. Edit `ChartPreparation.spec`:
   ```python
   exe = EXE(
       ...
       icon='path/to/your/icon.ico',
       ...
   )
   ```
3. Rebuild

### Hiding the Console Window

Edit `ChartPreparation.spec`:

```python
exe = EXE(
    ...
    console=False,  # Change from True to False
    ...
)
```

**Note:** This removes the console window entirely. Users won't see startup messages or be able to force-quit with Ctrl+C.

### Including Additional Files

Edit `ChartPreparation.spec` and add to the `datas` list:

```python
datas=[
    ('templates', 'templates'),
    ('static', 'static'),
    ('StockSymbols.csv', '.'),
    ('NiftySymbols.csv', '.'),
    ('config.py', '.'),
    ('your_new_file.txt', '.'),  # Add this line
],
```

## Build Environment

### Recommended Setup

For consistent builds:
- Use a clean Windows virtual machine
- Install only Python and required dependencies
- Build in a fresh environment each time

### GitHub Actions (Optional)

You can automate Windows builds using GitHub Actions:
1. Create `.github/workflows/build.yml`
2. Use `windows-latest` runner
3. Install dependencies and run build script
4. Upload artifact

Example workflow available in the GitHub Actions documentation.

## Support

For issues specific to:
- **Application functionality:** Contact the developer
- **PyInstaller issues:** See https://pyinstaller.org/
- **Windows compatibility:** Ensure building on Windows 10+

## Version History

- **Version 1** (Initial Release)
  - Daily Chart generation from stock CSV
  - Index Chart generation from indices CSV
  - Auto-browser opening
  - Automatic server shutdown on browser close
  - Version display in UI and metadata
