# Smart Lights Blueprint

Automatically turn lights on and off based on binary sensors (motion sensors, door sensors, etc.), with optional adaptive lighting that adjusts brightness and color temperature based on the sun position.

[Lire en français](README.fr.md)

## Installation

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fnicolinuxfr%2Fsmart-lights-blueprint%2Fgh-pages%2Fen%2Fsmart_lights.yaml)

Or copy this URL manually:

```
https://raw.githubusercontent.com/nicolinuxfr/smart-lights-blueprint/gh-pages/en/smart_lights.yaml
```

## Configuration

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| **Lights** | The lights to control | Yes | — |
| **Enable automatic on/off** | Turn lights on and off based on sensors and switches | No | On |
| **Enable adaptive lighting** | Adjust brightness and color temperature based on the sun | No | Off |

### Auto on/off – Sensors and delay

| Input | Description | Default |
|-------|-------------|---------|
| **Sensors** | Binary sensors that trigger the lights (motion, door/window, etc.) | — |
| **Switch** | An `input_boolean` used as a toggle for the lights, typically flipped by another automation. Turning it off turns the lights off immediately | — |
| **Turn off delay** | Time to wait before turning off the lights after sensors become inactive | 00:02:00 |

### Auto on/off – Lighting conditions

| Input | Description | Default |
|-------|-------------|---------|
| **Night only** | Only turn on lights when the sun is below the horizon | Off |
| **Luminosity sensors** | Illuminance sensors to check before turning on (average is used if multiple) | — |
| **Luminosity threshold** | Lights turn on only if average luminosity is below this value | 30 lx |

### Auto on/off – Advanced

| Input | Description | Default |
|-------|-------------|---------|
| **Keep lights on with open doors** | Open door/window sensors prevent lights from turning off | Off |
| **Control switches** | `input_boolean` entities that enable/disable the automation (all must be on) | — |

### Adaptive lighting – Brightness and color

| Input | Description | Default |
|-------|-------------|---------|
| **Minimum brightness** | Brightness at the beginning and end of the day | 30% |
| **Maximum brightness** | Brightness in the middle of the day | 100% |
| **Minimum temperature** | White temperature at the beginning and end of the day | 2700 K |
| **Maximum temperature** | White temperature in the middle of the day | 5500 K |

### Adaptive lighting – Advanced

| Input | Description | Default |
|-------|-------------|---------|
| **Automatic adaptation control** | An `input_boolean` or `binary_sensor` that controls lighting adaptations | — |
| **Automatic re-activation** | Re-enable the control entity when all lights turn off. Requires the control entity to be an `input_boolean` | Off |
| **Automatic deactivation on color** | Disable the control entity when a light switches to color mode. Requires the control entity to be an `input_boolean` | Off |
| **Weather-based variation** | A weather entity to adjust settings based on weather conditions | — |

### Adaptive lighting – Night mode

| Input | Description | Default |
|-------|-------------|---------|
| **Night mode** | An `input_boolean` or `binary_sensor` that activates night mode | — |
| **Night brightness** | Fixed brightness when night mode is active | 20% |
| **Night temperature** | Fixed white temperature when night mode is active | 2200 K |

## How it works

### Automatic on/off

1. When any selected sensor becomes active (motion detected, door opened, etc.), the lights turn on.
2. When all sensors become inactive, the blueprint waits for the configured delay before turning off the lights.
3. If a sensor becomes active again during the delay, the timer resets and the lights stay on.
4. The optional **switch** input uses an `input_boolean` as a toggle for the lights. You can flip it from another automation, for example when a physical switch or button is pressed. Turning it off always turns the lights off immediately.
5. By default, open door/window sensors do not prevent the lights from turning off — only motion/presence sensors are checked.

#### Lighting conditions

The lighting conditions only affect **turning on** the lights, whether the trigger comes from sensors or from the optional switch. Turning off always works regardless of sun or luminosity.

- **Night only**: lights turn on only when the sun is below the horizon, using the built-in Home Assistant `sun.sun` entity.
- **Luminosity sensors + threshold**: lights turn on only when the average luminosity is below the threshold.
- **Both enabled**: lights turn on if **either** condition is met (night OR low luminosity).
- **Neither enabled**: lights always turn on when a sensor triggers.

#### Control switches

If one or more **control switches** are configured, all of them must be on for the automation to work. When any switch is turned off, the lights turn off after the configured delay. When all switches are back on, the automation resumes immediately.

### Adaptive lighting

When enabled, the blueprint adjusts brightness and color temperature throughout the day based on the sun's position:

- **Morning/evening**: lower brightness, warm white (2700 K by default).
- **Midday**: maximum brightness, cooler white (5500 K by default).
- **Night**: if night mode is active, fixed low brightness and very warm white.
- **Weather**: optionally adjusts brightness and color temperature based on weather conditions (cloudy, rainy, etc.).

Adaptive values are applied when lights turn on and updated every 5 minutes while lights remain on.
Light state changes are also tracked correctly when the target lights are selected via entities, devices, or areas.
