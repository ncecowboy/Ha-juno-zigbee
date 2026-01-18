# Juno RB56SC Zigbee Light Integration for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)
[![GitHub release](https://img.shields.io/github/release/ncecowboy/Ha-juno-zigbee.svg)](https://github.com/ncecowboy/Ha-juno-zigbee/releases)
[![License](https://img.shields.io/github/license/ncecowboy/Ha-juno-zigbee.svg)](LICENSE)

A Home Assistant custom integration for advanced management of Juno RB56SC Zigbee lights. This integration extends the functionality provided by Home Assistant's native Zigbee Home Automation (ZHA) integration by adding device settings management, firmware monitoring, and enhanced control capabilities.

## Features

- **Advanced Light Control**: Enhanced control over Juno RB56SC light brightness and on/off states
- **Settings Management**: Configure and manage device-specific settings
- **Firmware Monitoring**: Track firmware versions and device information
- **Device Attributes**: Access detailed device information including manufacturer, model, and firmware version
- **Seamless ZHA Integration**: Works alongside Home Assistant's ZHA integration without conflicts

## Requirements

- Home Assistant 2024.1.0 or later
- Zigbee Home Automation (ZHA) integration installed and configured
- Juno RB56SC Zigbee light(s) paired with ZHA

## Installation

### HACS Installation (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on **Integrations**
3. Click the three dots menu in the top right corner
4. Select **Custom repositories**
5. Add this repository URL: `https://github.com/ncecowboy/Ha-juno-zigbee`
6. Select category: **Integration**
7. Click **Add**
8. Find "Juno RB56SC Zigbee Light" in the integration list
9. Click **Download**
10. Restart Home Assistant

### Manual Installation

1. Download the [latest release](https://github.com/ncecowboy/Ha-juno-zigbee/releases) from GitHub
2. Extract the downloaded file
3. Copy the `custom_components/juno_rb56sc` folder to your Home Assistant `config/custom_components/` directory
   - If the `custom_components` directory doesn't exist, create it in your config folder
4. Restart Home Assistant

## Configuration

1. Ensure your Juno RB56SC device is already paired with ZHA:
   - Go to **Settings** → **Devices & Services** → **Zigbee Home Automation**
   - Pair your Juno RB56SC light if not already done

2. Add the Juno RB56SC integration:
   - Go to **Settings** → **Devices & Services**
   - Click **Add Integration**
   - Search for "Juno RB56SC"
   - Select your Juno RB56SC device from the list
   - Click **Submit**

3. The integration will create additional entities for your device:
   - Light control entity (enhanced)
   - Firmware version sensor
   - Manufacturer sensor
   - Model sensor

## Usage

### Light Control

The integration creates an enhanced light entity that provides:
- On/Off control
- Brightness adjustment (0-255)
- State synchronization with ZHA

Example automation:
```yaml
automation:
  - alias: "Set Juno Light to 50% at sunset"
    trigger:
      - platform: sun
        event: sunset
    action:
      - service: light.turn_on
        target:
          entity_id: light.juno_rb56sc_light
        data:
          brightness: 128
```

### Sensors

The integration provides several diagnostic sensors:

- **Firmware Version**: Shows the current firmware version installed on the device
- **Manufacturer**: Displays the device manufacturer
- **Model**: Shows the device model number

These can be used in automations or displayed on dashboards to monitor device information.

## Version Management

This integration follows [Semantic Versioning](https://semver.org/):
- **Major version** (X.0.0): Breaking changes
- **Minor version** (0.X.0): New features, backward compatible
- **Patch version** (0.0.X): Bug fixes, backward compatible

Current version: **1.0.0**

## Troubleshooting

### No devices found during setup

**Problem**: The integration reports "No Juno RB56SC devices found"

**Solution**: 
1. Ensure your device is paired with ZHA first
2. Verify the device manufacturer and model in the device registry
3. Check that the device name contains "Juno" and model contains "RB56SC"

### Light control not working

**Problem**: Light doesn't respond to commands

**Solution**:
1. Check that the underlying ZHA light entity is working
2. Verify the device is online in the ZHA integration
3. Try reloading the Juno RB56SC integration
4. Check Home Assistant logs for error messages

### State not updating

**Problem**: Light state doesn't reflect actual device state

**Solution**:
1. The integration syncs state from ZHA every 30 seconds
2. Manually refresh by reloading the integration
3. Check ZHA integration for device connectivity issues

## Development

### Project Structure

```
custom_components/juno_rb56sc/
├── __init__.py          # Integration initialization
├── config_flow.py       # Configuration UI
├── const.py            # Constants and configuration
├── light.py            # Light platform
├── sensor.py           # Sensor platform
├── strings.json        # UI strings and translations
└── manifest.json       # Integration metadata
```

### Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

### Reporting Issues

Please report issues on the [GitHub issue tracker](https://github.com/ncecowboy/Ha-juno-zigbee/issues).

Include:
- Home Assistant version
- Integration version
- Device model and firmware version
- Relevant log entries
- Steps to reproduce

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Home Assistant community
- ZHA integration developers
- HACS for making custom integration distribution easy

## Support

For support:
- Check the [documentation](https://github.com/ncecowboy/Ha-juno-zigbee)
- Review [existing issues](https://github.com/ncecowboy/Ha-juno-zigbee/issues)
- Create a [new issue](https://github.com/ncecowboy/Ha-juno-zigbee/issues/new) if needed
