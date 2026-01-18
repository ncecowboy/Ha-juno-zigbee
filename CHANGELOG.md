# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.2] - 2026-01-18

- Fix AttributeError when configuring multiple devices simultaneously (#8)

## [1.2.1] - 2026-01-18

### Fixed
- Fixed AttributeError when setting up multiple devices at once
  - Resolved crash that occurred when users selected multiple devices during configuration
  - The error `AttributeError: 'ConfigEntries' object has no attribute 'async_create_entry'` no longer occurs
  - Configuration flow now properly handles multi-device selection
  - Additional devices are configured through separate import flows
  - Impact: Users can now successfully configure multiple Juno devices in one setup session

### Technical
- Removed incorrect call to `self.hass.config_entries.async_create_entry()` which doesn't exist in the ConfigEntries API
- Added `async_step_import()` method to handle programmatic device setup for additional devices
- Refactored multi-device setup to use proper Home Assistant config flow patterns
- First device is created through normal flow, additional devices use import flow
- Addressed code review feedback to eliminate redundant data keys

### Added
- Automated version management system
  - Created `scripts/bump_version.py` for automated version bumping across all project files
  - Added GitHub Actions workflow (`.github/workflows/version-bump.yml`) for automatic version updates on PR merge
  - Version bump type determined automatically from PR labels or title
  - Automatic changelog entry creation with PR details
  - Auto-creation and pushing of git tags for releases
- Comprehensive version management documentation in `docs/VERSION_MANAGEMENT.md`
  - Detailed guide on semantic versioning usage
  - Instructions for both automated and manual version bumping
  - Changelog writing guidelines with examples
  - Best practices for contributors and maintainers

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
