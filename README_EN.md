# Mac External Device Ejector Script

A Python script for safely ejecting all external devices on macOS, including USB drives, external hard drives, SD cards, and more.

## Features

- 🔄 **Safe Ejection**: Automatically excludes system volumes and main hard drives to prevent accidental system unmounting
- 🛡️ **Multiple Protection**: Uses dual verification mechanism to ensure only genuine external devices are ejected
- ⚡ **Efficient Execution**: Parallel processing of multiple devices for improved efficiency
- 📊 **Silent Operation**: No confirmation prompts, directly executes ejection operations

## Supported Device Types

- ✅ USB flash drives
- ✅ External hard drives
- ✅ SD card readers
- ✅ Disk images (.dmg)
- ✅ Network shared volumes
- ❌ System main hard drive (automatically protected)
- ❌ System recovery partitions
- ❌ Time Machine backup volumes

## Usage

### Direct Execution

```bash
python3 eject_all_devices.py
```

### With Execute Permissions

```bash
chmod +x eject_all_devices.py
./eject_all_devices.py
```

### Install to System Path (Optional)

```bash
sudo cp eject_all_devices.py /usr/local/bin/
sudo chmod +x /usr/local/bin/eject_all_devices.py
```

After installation, you can run it from anywhere:

```bash
eject_all_devices.py
```

## Script Execution Flow

1. **Scan Mounted Volumes**: Get information about all volumes mounted under `/Volumes/`
2. **Identify External Devices**: Dual verification using system volume markers and keywords
3. **Safe Ejection**: Use `diskutil eject` command for safe device ejection
4. **Error Handling**: If ejection fails, try using `diskutil unmount` command

## Technical Implementation

### Core Functions

- `get_mounted_volumes()`: Get information about all mounted volumes
- `is_system_volume()`: Determine if a volume is a system volume or main hard drive
- `eject_volume()`: Eject the specified volume

### Safety Mechanisms

The script ensures system safety through:

1. **System Volume Whitelist**: Explicitly excludes known critical system volumes
2. **Keyword Filtering**: Identifies volumes containing system-related keywords
3. **Mount Point Verification**: Further confirms system volumes through mount paths

## Protected System Volumes

The script automatically protects the following system volumes:
- Root directory `/`
- `/System` system directory
- `/Library` library directory
- `/Users` user directory
- `/Applications` applications directory
- `/Volumes/Macintosh HD` default system volume
- `/Volumes/Macintosh HD - Data` default data volume

## System Requirements

- macOS 10.12 or later
- Python 3.6 or later
- Terminal access required
- Administrator privileges may be needed for certain operations

## Important Notes

1. **Data Safety**: Ensure no files are actively being used on the devices
2. **Permission Requirements**: Some operations may require password input
3. **Silent Operation**: Script executes directly without confirmation prompts
4. **Network Volumes**: Network shared volumes may not eject properly

## Troubleshooting

If the script fails to eject devices properly, try:

1. Check if devices are being used by other applications
2. Manually use `diskutil list` to check device status
3. Ensure you have sufficient permissions to perform operations
4. Verify Python version meets requirements

## Code Structure

```
eject_all_devices.py
├── Module imports and docstring
├── get_mounted_volumes() - Get mounted volume information
├── is_system_volume() - System volume identification
├── eject_volume() - Single volume ejection
├── main() - Main function and execution flow
└── Script entry point
```

## Python Dependencies

This script uses only Python standard library modules:
- `subprocess` - For executing shell commands
- `re` - For regular expression operations
- `sys` - For system-specific parameters
- `time` - For timing operations

No external packages required.

## License

This script is open source software, free to use and modify.