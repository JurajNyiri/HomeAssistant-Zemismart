# HomeAssistant - Zemismart

Custom component - Zemismart - to add Zemismart devices into Home Assistant

This integration allows full local control of your Zemismart devices along with Zemismart specific features not available in the official [Tuya](https://www.home-assistant.io/integrations/tuya/) or [local tuya](https://github.com/rospogrigio/localtuya) integrations.

It also allows you to use the application along with the Home Assistant running, or even multiple Home Assistant instances communicating with the same device. While you are using the application, the control via Home Assistant is not available.

## Requirements

### Network

Broadcast UDP ports 6666 and 6667 **must be open** in firewall for the discovery process.

### Tuya device's Key

There are several ways to obtain the localKey depending on your environment and the devices you own. A good place to start getting info is https://github.com/codetheweb/tuyapi/blob/master/docs/SETUP.md .

### If you block cloud access

You must block DNS requests too (to the local DNS server eg 192.168.1.1). If you only block outbound internet then the device will sit in zombie state, it will refuse / not respond to any connections with the localkey. Connect the devices first with an active internet connection, grab each device localkey and then implement the block.

## Usage

Add devices via Integrations (search for Zemismart) in Home Assistant UI.

To add multiple devices, add integration multiple times.
