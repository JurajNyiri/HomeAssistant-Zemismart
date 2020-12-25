# HomeAssistant - Zemismart

Custom component - Zemismart - to add Zemismart devices into Home Assistant

This integration allows full local control of your Zemismart devices along with Zemismart specific features not available in the official [Tuya](https://www.home-assistant.io/integrations/tuya/) or [local tuya](https://github.com/rospogrigio/localtuya) integrations.

It also allows you to use the application along with the Home Assistant running, or even multiple Home Assistant instances communicating with the same device. While you are using the application, the control via Home Assistant is not available.

## Supported Devices

<details>
  <summary>Zemismart Electric Floor Heating Thermostat</summary>

- Product ID: 3uoeudsge0ooafig
- Product version: 3.3
</details>

If you got this integration working with a different product, please let us know by creating a new issue! We will add that device to discovery process.

If an unsupported device is discovered, warning message is sent into log, please paste this message into a new issue if you got that device working.

## Installation

Copy contents of custom_components/zemismart/ to custom_components/zemismart/ in your Home Assistant config folder.

## Installation using HACS

**Coming soon**

HACS is a community store for Home Assistant. You can install [HACS](https://github.com/custom-components/hacs) and then install Zemismart from the HACS store.

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

## Services

Following built in climate services are supported:

- climate.set_hvac_mode
- climate.set_preset_mode
- climate.set_swing_mode
- climate.set_temperature
- climate.turn_off
- climate.turn_on

This integration additionally creates zemismart.\* services to control specific features of the device.

<details>
  <summary>zemismart.calibrate</summary>

Calibrates current temperature

- **entity_id** Required: Entity to calibrate temperature for
- **difference** Required: Temperature difference. Value between -9 and 9.
</details>

<details>
  <summary>zemismart.lock</summary>

Locks thermostat

- **entity_id** Required: Entity to lock
</details>

<details>
  <summary>zemismart.optimal_start</summary>

Turns on or off optimal start mode

- **entity_id** Required: Entity to set optimal start mode for
- **state** Required: Set optimal start mode on or off. Possible values: on, off.
</details>

<details>
  <summary>zemismart.unlock</summary>

Unlocks thermostat

- **entity_id** Required: Entity to unlock
</details>

<details>
  <summary>zemismart.use_sensor</summary>

Chooses temperature sensor to use

- **entity_id** Required: Entity to choose temperature sensor for
- **sensor** Required: Sensor to use. Possible values: internal, external, both
</details>

<details>
  <summary>zemismart.window_mode</summary>

Turns on or off window mode

- **entity_id** Required: Entity to set window mode for
- **state** Required: Set window mode on or off. Possible values: on, off.
</details>

## Have a comment or a suggestion?

Please [open a new issue](https://github.com/JurajNyiri/HomeAssistant-Zemismart/issues/new), or discuss on [Home Assistant: Community Forum](https://community.home-assistant.io/t/custom-component-zemismart/259734).

## Thank you

- [local tuya](https://github.com/rospogrigio/localtuya) by which this integration has been inspired and uses some parts of it

<a href="https://www.buymeacoffee.com/jurajnyiri" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/v2/default-blue.png" alt="Buy Me A Coffee"  width="150px" ></a>

# Disclaimer

Author is in no way affiliated with Zemismart or Tuya.

Author does not guarantee functionality of this integration and is not responsible for any damage.

All product names, trademarks and registered trademarks in this repository, are property of their respective owners.
