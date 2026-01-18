# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-01-18

### Added
- Multiple device selection during setup: Users can now select and configure multiple Juno devices in a single setup session
- Device filtering: Already configured devices are now excluded from the setup device list

### Changed
- Device display names in setup now show the actual device name (as set in Home Assistant) instead of combining name and manufacturer
- Updated setup flow description to indicate support for selecting one or more devices
- Improved error messaging for device selection scenarios

### Fixed
- Devices already configured by this integration are no longer shown in the setup flow
- Cleaner device name presentation in the device selection list

## [1.1.0] - 2026-01-18

### Added
- Multi-model support: Integration now discovers all Juno light devices, not just RB56SC
- Support for ABL-LIGHT-Z-201 and other Juno light models

### Changed
- Device discovery now filters only by manufacturer "Juno" instead of requiring specific model numbers
- Updated documentation to reflect multi-model support

### Technical
- Removed model-specific filtering in config_flow.py
- Cleaned up unused MODEL import

## [1.0.0] - 2026-01-18

### Added
- Initial release of Juno RB56SC Zigbee Light integration
- Light control platform with brightness and on/off support
- Sensor platform for firmware version monitoring
- Sensor platform for manufacturer and model information
- Configuration flow for device setup via Home Assistant UI
- HACS compatibility for easy installation
- Integration with ZHA (Zigbee Home Automation)
- Comprehensive documentation and README
- Spanish translations

### Features
- Enhanced light control extending ZHA functionality
- Real-time state synchronization with ZHA entities
- Device information sensors (firmware, manufacturer, model)
- User-friendly configuration flow
- Automatic device discovery from ZHA
- Support for multiple Juno RB56SC devices

### Technical
- Home Assistant 2024.1.0+ compatibility
- Proper entity and device registry integration
- Async/await pattern throughout
- Logging and error handling
- Version management support
