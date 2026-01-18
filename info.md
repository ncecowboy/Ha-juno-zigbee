# Juno RB56SC Zigbee Light Integration

This integration provides advanced management capabilities for Juno RB56SC Zigbee lights in Home Assistant.

## Features

- **Settings Management**: Configure and manage device settings
- **Light Control**: Full control over brightness and on/off states
- **Firmware Monitoring**: Track firmware versions and updates
- **Device Attributes**: Access detailed device information and status

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/ncecowboy/Ha-juno-zigbee`
6. Select category: "Integration"
7. Click "Add"
8. Click "Install" on the Juno RB56SC Zigbee Light card
9. Restart Home Assistant

### Manual Installation

1. Download the latest release
2. Copy the `custom_components/juno_rb56sc` folder to your Home Assistant `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "Juno RB56SC"
4. Follow the configuration flow

## Notes

- This integration works alongside Home Assistant's Zigbee Home Automation (ZHA) integration
- Your Juno RB56SC devices must already be paired via ZHA
- This integration adds advanced settings and firmware management capabilities
