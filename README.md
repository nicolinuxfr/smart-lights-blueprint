# Smart Lights Blueprint

Control one or more lights with a single blueprint. It can run sensor-based automatic on/off, adaptive lighting, or both at the same time.

[Lire en français](README.fr.md)

## Installation

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fnicolinuxfr%2Fsmart-lights-blueprint%2Fgh-pages%2Fen%2Fsmart_lights.yaml)

Or copy this URL manually:

```text
https://raw.githubusercontent.com/nicolinuxfr/smart-lights-blueprint/gh-pages/en/smart_lights.yaml
```

## Quick start

1. Select the target **Lights**.
2. Enable **automatic on/off** and/or **adaptive lighting**.
3. Fill only the sections needed for the features you enabled.

## Configuration

### Root inputs

| Input | Description | Default |
|-------|-------------|---------|
| **Lights** | Lights, devices, or areas to control | — |
| **Enable automatic on/off** | Turn sensor-based automatic on/off on or off | `true` |
| **Enable adaptive lighting** | Turn adaptive brightness and white temperature on or off | `false` |

### Auto on/off – Basics

| Input | Description | Default |
|-------|-------------|---------|
| **Sensors** | Binary sensors used for automatic on/off | `[]` |
| **Turn off delay** | Delay before lights turn off after sensors go inactive | `00:02:00` |

### Auto on/off – Options

| Input | Description | Default |
|-------|-------------|---------|
| **Switch entity** | Optional `input_boolean` used as an external toggle that always turns the managed lights on or off immediately | `""` |
| **Night only** | Allow sensor-based turn-on only when the sun is below the horizon | `false` |
| **Illuminance sensors** | Sensors used by the low-lux rules | `[]` |
| **Illuminance threshold** | Average lux must be below this value for the illuminance condition to allow turn-on | `30 lx` |
| **Keep lights on with open doors** | Open door/window sensors keep lights on | `false` |
| **Control switches that must be on** | `input_boolean` entities that must stay on for auto on/off to run | `[]` |
| **Control switches that must be off** | `input_boolean` entities that must stay off for auto on/off to run | `[]` |

### Adaptive – Brightness and color

| Input | Description | Default |
|-------|-------------|---------|
| **Minimum brightness** | Brightness around sunrise and sunset | `30%` |
| **Maximum brightness** | Brightness around midday | `100%` |
| **Minimum temperature** | Warmest white temperature around sunrise and sunset | `2700 K` |
| **Maximum temperature** | Coolest white temperature around midday | `5500 K` |

### Adaptive – Options

| Input | Description | Default |
|-------|-------------|---------|
| **Adaptive control entity** | Optional `input_boolean` or `binary_sensor` that enables adaptive updates | `""` |
| **Automatic re-activation** | Re-enable the adaptive control entity when all managed lights turn off | `false` |
| **Disable on color mode** | Disable the adaptive control entity when a managed light switches to color mode | `false` |
| **Weather entity** | Optional weather entity used to shift adaptive values | `""` |
| **Night mode entity** | Optional `input_boolean` or `binary_sensor` that activates fixed night values | `""` |
| **Night brightness** | Fixed brightness while night mode is active | `20%` |
| **Night temperature** | Fixed white temperature while night mode is active | `2200 K` |

## Feature combinations

- **Automatic on/off only**: the blueprint reacts to sensors and optional control entities, but does not change brightness or color temperature adaptively.
- **Adaptive lighting only**: the blueprint tracks managed light state changes and refreshes adaptive values while lights are on, without using sensors for on/off.
- **Both enabled**: sensor-based on/off and adaptive updates are both active.

## Turn-on conditions

These conditions apply only to sensor-based turn-on. The optional switch entity bypasses them and always toggles the lights immediately. It also bypasses the control switches below.

- **Night only** enabled: sensor-based turn-on is allowed only when `sun.sun` is below the horizon.
- **Illuminance sensors + threshold** configured: sensor-based turn-on is allowed when the average illuminance is below the threshold.
- **Both configured**: sensor-based turn-on is allowed when either condition is true.
- **Neither configured**: sensor-based turn-on is always allowed.

## Notes

- Adaptive values are applied when a managed light turns on and refreshed every 5 minutes while compatible target lights remain on.
- The blueprint keeps working when lights are selected via entities, devices, or areas.
- **Automatic re-activation** and **Disable on color mode** only take effect when the adaptive control entity is an `input_boolean`.
