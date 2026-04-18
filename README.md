# path-to

A command-line tool to find the full path to files in the current directory and subdirectories.

## 🚀 Features

- **Recursive Search**: Searches through all subdirectories
- **Exact & Partial Matching**: Finds exact matches first, then partial matches
- **Multiple Output Options**: Show first match, all matches, or just count
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Standalone Executable**: No Python installation required
- **GUI Installer**: User-friendly installation interface

## 📁 Project Structure

```
path-to/
├── src/
│   ├── path_to_final.py      # Main application (CLI + GUI)
│   ├── setup.py              # Installation configuration
│   └── build_executable.py   # Build script for executable
├── executable/
│   └── path-to.exe          # Standalone executable
├── add_to_path.bat           # PATH management script
└── README.md                 # This file
```

## 🛠️ Installation

### Option 1: Standalone Executable (Recommended)

1. **Download the executable** from `executable/` folder
2. **Run the PATH manager**: `add_to_path.bat`
3. **Choose option 1** to add to PATH
4. **Restart command prompt** for changes to take effect

### Option 2: Python Installation

1. **Install from source**:
   ```bash
   pip install .
   ```

2. **Or install with GUI**:
   ```bash
   python src/path_to_final.py --installer
   ```

### Option 3: Build Your Own

1. **Build executable**:
   ```bash
   python src/build_executable.py
   ```

2. **Executable created in**: `executable/path-to.exe`

## 📖 Usage

### Command Line

```bash
# Find a specific file
path-to <filename>

# Search in specific directory
path-to <filename> -d <directory>

# Show all matches
path-to <filename> --all

# Show count only
path-to <filename> --count

# Get help
path-to --help

# Launch GUI installer
path-to --installer
```

### Examples

```bash
# Find setup.py in current directory
path-to setup.py

# Find all Python files
path-to .py --all

# Count README files
path-to README --count

# Search in specific folder
path-to config.json -d /path/to/project
```

## 🎮 GUI Installer

Run `path-to --installer` to launch the graphical installer with:

- **Installation Status**: Shows if path-to is installed
- **Progress Tracking**: Real-time installation progress
- **Console Log**: Detailed installation output
- **Smart Buttons**: Install/Uninstall/Test based on current state
- **Information Panel**: Usage instructions and features

## 🔧 PATH Management

The `add_to_path.bat` script provides easy PATH management:

### Menu Options:
1. **Install** - Adds `executable/` folder to system PATH
2. **Uninstall** - Removes `executable/` folder from PATH with confirmation
3. **Exit** - Closes the script

### Safety Features:
- **Confirmation Required**: Uninstall requires user confirmation
- **Error Handling**: Clear success/error messages
- **Administrator Notes**: Suggests admin rights if needed
- **Rollback Support**: Easy to undo PATH changes

## 🏗️ Building from Source

### Prerequisites
- Python 3.6 or higher
- PyInstaller (automatically installed by build script)

### Build Process
```bash
# From project root
python src/build_executable.py
```

### Build Output
- **Executable**: `executable/path-to.exe`
- **Single File**: No dependencies required
- **Cross-Platform**: Works on Windows, Linux, macOS

## 🐛 Troubleshooting

### Common Issues

**"path-to is not recognized"**:
- Run `add_to_path.bat` and choose option 1
- Restart command prompt
- Verify executable exists in `executable/` folder

**"No files found"**:
- Check filename spelling
- Use `--all` flag to see all matches
- Try partial filename matching

**"Permission denied"**:
- Run as Administrator
- Check folder permissions
- Use `-d` to specify accessible directory

### GUI Issues

**"PyQt5 is not installed"**:
- This version uses Tkinter (built into Python)
- No external GUI libraries required

**Installer won't open**:
- Run as Administrator
- Check Python installation
- Try command-line installation

## 📄 License

MIT License - Feel free to use, modify, and distribute.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🌟 Star History

- **v1.0.0**: Initial release with CLI and GUI
- **Tkinter Integration**: Removed PyQt5 dependency
- **Standalone Executable**: No Python required
- **Smart PATH Management**: Install/uninstall with confirmation
- **Clean Project Structure**: Organized source and build files

## 📞 Support

For issues, questions, or feature requests, please open an issue on the GitHub repository.

---

**Made with ❤️ for developers who need quick file path access**

## Examples

```bash
# Find a specific file
path-to config.json

# Find all Python files containing "test" in the name
path-to test --all

# Search in a specific directory
path-to data.csv -d /path/to/project

# Count how many README files exist
path-to README --count
```

## Uninstallation

To uninstall the tool:

```bash
pip uninstall path-to
```

## License

MIT License
