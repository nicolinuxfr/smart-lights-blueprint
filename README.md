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
2. Fill **Turn-on sensors** and/or the **Switch** if you want automatic on/off.
3. Open **Adaptive lighting** or **Night mode** only if you need those optional settings.

## Configuration

### Root inputs

| Input | Description | Default |
|-------|-------------|---------|
| **Lights** | Lights, devices, or areas to control | — |

### Main inputs

| Input | Description | Default |
|-------|-------------|---------|
| **Turn-on sensors** | Binary sensors used for automatic on/off | `[]` |
| **Turn off delay** | Delay before lights turn off after sensors go inactive | `00:02:00` |
| **Switch** | Optional `input_boolean` used as an external toggle that always turns the managed lights on or off immediately, while staying synced with their all-on/all-off state | `""` |

### Night mode

| Input | Description | Default |
|-------|-------------|---------|
| **Night only** | Allow sensor-based turn-on only when the sun is below the horizon | `false` |
| **Night mode entity** | Optional `input_boolean` or `binary_sensor` that activates fixed night values | `""` |
| **Night brightness** | Fixed brightness while night mode is active | `20%` |
| **Night temperature** | Fixed white temperature while night mode is active | `2200 K` |

### Auto on/off – Options

| Input | Description | Default |
|-------|-------------|---------|
| **Illuminance sensors** | Sensors used by the low-lux rules | `[]` |
| **Illuminance threshold** | Average lux must be below this value for the illuminance condition to allow turn-on | `30 lx` |
| **Keep lights on with open doors** | Open door/window sensors keep lights on | `false` |
| **Control entities** | `input_boolean` entities that must stay off for auto on/off to run | `[]` |

### Adaptive lighting

| Input | Description | Default |
|-------|-------------|---------|
| **Enable adaptive lighting** | Turn adaptive brightness and white temperature on or off | `false` |
| **Minimum brightness** | Brightness around sunrise and sunset | `30%` |
| **Maximum brightness** | Brightness around midday | `100%` |
| **Minimum temperature** | Warmest white temperature around sunrise and sunset | `2700 K` |
| **Maximum temperature** | Coolest white temperature around midday | `5500 K` |
| **Adaptive control entity** | Optional `input_boolean` or `binary_sensor` that enables adaptive updates | `""` |
| **Automatic re-activation** | Re-enable the adaptive control entity when all managed lights turn off | `false` |
| **Disable on color mode** | Disable the adaptive control entity when a managed light switches to color mode | `false` |
| **Weather entity** | Optional weather entity used to shift adaptive values | `""` |

## Feature combinations

- **Automatic on/off only**: configure **Turn-on sensors**, **control entities**, and/or the **Switch**, without enabling adaptive lighting.
- **Adaptive lighting only**: enable adaptive lighting and leave **Turn-on sensors** plus the **Switch** empty if you do not want automatic on/off.
- **Both enabled**: combine the automatic on/off inputs with adaptive lighting.

## Turn-on conditions

These conditions apply only to sensor-based turn-on. The optional switch bypasses them and always toggles the lights immediately. It also bypasses the control entities below.

- **Night only** enabled: sensor-based turn-on is allowed only when `sun.sun` is below the horizon.
- **Illuminance sensors + threshold** configured: sensor-based turn-on is allowed when the average illuminance is below the threshold.
- **Both configured**: sensor-based turn-on is allowed when either condition is true.
- **Neither configured**: sensor-based turn-on is always allowed.

## Notes

- Automatic on/off becomes active as soon as at least one **Turn-on sensor**, **Switch**, or **control entity** is configured.
- The optional switch is synchronized from the managed lights: it turns on when they are all on and turns off when they are all off, without re-triggering redundant light commands.
- Adaptive values are applied when the first managed light turns on from an all-off state and refreshed every 5 minutes while compatible target lights remain on.
- The blueprint keeps working when lights are selected via entities, devices, or areas.
- **Automatic re-activation** and **Disable on color mode** only take effect when the adaptive control entity is an `input_boolean`.
- The blueprint now keeps 20 traces and avoids the previous global `state_changed` listener that could flood Home Assistant trace history with empty runs.
