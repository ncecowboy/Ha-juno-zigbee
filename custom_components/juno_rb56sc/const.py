"""Constants for the Juno RB56SC Zigbee Light integration."""

DOMAIN = "juno_rb56sc"
MANUFACTURER = "Juno"
MODEL = "RB56SC"

# Configuration
CONF_DEVICE = "device"

# Platforms
PLATFORMS = ["light", "sensor"]

# Device attributes
ATTR_FIRMWARE_VERSION = "firmware_version"
ATTR_LIGHT_LEVEL = "light_level"
ATTR_MANUFACTURER = "manufacturer"
ATTR_MODEL = "model"

# Zigbee clusters
CLUSTER_ON_OFF = 0x0006
CLUSTER_LEVEL = 0x0008
CLUSTER_BASIC = 0x0000

# Update interval
SCAN_INTERVAL = 30  # seconds
