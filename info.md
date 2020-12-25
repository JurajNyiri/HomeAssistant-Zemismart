# HomeAssistant - Zemismart

Custom component - Zemismart - to add Zemismart devices into Home Assistant

This integration allows full local control of your Zemismart devices along with Zemismart specific features not available in the official [Tuya](https://www.home-assistant.io/integrations/tuya/) or [local tuya](https://github.com/rospogrigio/localtuya) integrations.

## Requirements

### Network

Broadcast UDP ports 6666 and 6667 **must be open** in firewall for the discovery process.

### Tuya device's Key

There are several ways to obtain the localKey depending on your environment and the devices you own. A good place to start getting info is https://github.com/codetheweb/tuyapi/blob/master/docs/SETUP.md .

## Usage

Add devices via Integrations (search for Zemismart) in Home Assistant UI.

To add multiple devices, add integration multiple times.
