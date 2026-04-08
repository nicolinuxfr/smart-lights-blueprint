# Smart Lights Blueprint

This blueprint includes everything needed to control lights managed by Home Assistant. It turns lights on and off based on sensors and can optionally adapt the lighting throughout the day.

[French version](README.fr.md)

## Installation

Click this button to open your Home Assistant instance and import the blueprint right away:

[![Open your Home Assistant instance and show the blueprint import dialog.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fnicolinuxfr%2Fsmart-lights-blueprint%2Fgh-pages%2Fen%2Fsmart_lights.yaml)

Or copy this URL and paste it into the Home Assistant blueprint import field:

```text
https://raw.githubusercontent.com/nicolinuxfr/smart-lights-blueprint/gh-pages/en/smart_lights.yaml
```

## How to use it

Here is how to configure the automation, step by step, with detailed explanations for each option and what it does.

### Selecting the lights

#### Lights

The only setting required for the automation to work properly is choosing the lights. You can select a single smart bulb, several lights, a group of lights, or even an area or tag.

> [!NOTE]
> You can choose any type of light. The automation should adapt automatically to its capabilities. If it does not, feel free to [open an issue](https://github.com/nicolinuxfr/smart-lights-blueprint/issues/new) with details about the light so I can fix the bug.

### Configuring automatic turn-on and turn-off

#### Turn-on and turn-off sensors

For the automation to turn the lights on and off automatically, select at least one binary sensor in the **Turn-on and turn-off sensors** field. You can select motion or presence sensors, door sensors, or any other sensor with a true/false state.

> [!TIP]
> As an example, I use a binary sensor that reports whether my desktop computer is active or my TV is on, which keeps the related lights on even when the other sensors are no longer active.

The lights turn on as soon as at least one selected sensor becomes true. They turn off once all selected sensors are false.

**Keep the light on with open doors**

This option treats doors differently from the other sensors in the list and keeps the lights on as long as they stay open. By default, those sensors are handled differently and only turn the light on, without keeping it on.

#### Delay before turn-off

Choose how long to wait before turning the lights off once all sensors become inactive (2 minutes by default).

#### Turn-on with switch

This option is designed to control the lights from a connected physical switch. Instead of handling the switch directly in the automation, which would require supporting too many different cases, you can select an `input_boolean` entity that will be controlled from another automation.

The lights are turned on and off immediately whenever the selected helper changes state. This behavior is independent from the rest, and the lights will still turn off even if a motion sensor is still active, for example.

> [!TIP]
> For consistency, its state is synchronized with automatic turn-ons and turn-offs. In practice, if the lights are turned on because a motion sensor triggered the automation, then the helper dedicated to the switch is also turned on, and vice versa.

Leave the field empty if you do not want to use this option.

#### Control entities

Choose one or more `input_boolean` entities that block automatic turn-ons and turn-offs when they are true. This option is useful if you want to make sure some lights stay on.

Leave the field empty if you do not want to use this option.

### Adaptive lighting

Adaptive lighting changes the light settings throughout the day by following the course of the sun. The general idea is to have warmer, dimmer light in the morning and evening, and cooler, brighter light around noon when the sun is at its highest point.

#### Enable adaptive lighting

This box must be checked for the automation to adapt the settings of the selected lights. Otherwise, the automation only turns the lights on and off.

#### Brightness and temperature settings

The following options are fairly self-explanatory: define the minimum and maximum values you want, and the automation will work within that range. The idea is to choose the brightness and white temperature for the morning and evening, and the ones for the middle of the day, when the sun is highest.

The automation automatically calculates two curves, one for brightness and one for temperature. As long as managed lights are on, the new values are sent every 5 minutes, with a transition so they evolve smoothly.

#### Specific settings at night

Check the box to apply different settings at night. By default, the minimum values selected above are used. If you prefer other values, enable the option and choose the temperature and brightness below.

> [!NOTE]
> By default, night depends on the sun and is calculated automatically by Home Assistant. The automation still takes your preferences into account, as defined later in the automation.

#### Control entity

Same principle as with automatic turn-on and turn-off: choose an `input_boolean` entity that disables adaptive lighting when it is itself disabled. In that case, the last setting is kept as long as it stays inactive.

The following two options are tied to it:

- **Automatic re-activation**: by default, the automation does not manage the control entity, but if you want, it can be re-enabled once all managed lights are off.
- **Disable on color mode**: when this option is enabled, the control entity is automatically disabled if one light switches to color mode. The idea here is that the automation only manages white light, but you can temporarily enable colors and keep them until the control entity is enabled again.

These two options can be enabled at the same time. In that case, the lights return to white after they turn off.

#### Adjust with the weather

Select a weather entity to enable a slight adjustment to white temperature and brightness based on the weather conditions. It is subtle, but the lights become a little dimmer and a little warmer than the selected maximum values when the weather is poor.

### Night mode

The automation handles day and night differently, with two opposite goals that you can choose depending on your preferences. This section also defines what counts as night, with several options to adapt the automation to as many needs as possible.

#### Automatic turn-on

By default, the automation only runs during the day, which means the lights do not turn on automatically at night. Change this setting to invert its behavior and activate the lights only at night, or to keep the automation active all the time.

> [!NOTE]
> To be clear, this only concerns automatic turn-on from a sensor. By design, turn-on through the entity managed by a switch always remains available: if you press a switch, you always want to turn the lights on or off.

#### Use sun position

By default, the automation uses the sun position provided by Home Assistant to determine whether it is day or night. As soon as the sun is up, it is day. As soon as it has set, it is night.

You can disable this option, provided that you configure one of the two other methods used to determine whether it is night.

#### Illuminance sensors (optional)

First alternative method: choose illuminance sensors for night mode. If you select several sensors, the automation automatically calculates the average value.

The next field lets you define the brightness threshold from which it becomes day (30 lux by default). Any lower value is considered night.

#### Night mode entity (optional)

Second alternative method: an `input_boolean` entity or a `binary_sensor` that determines night mode when the entity or sensor is active.

> [!TIP]
> These three methods are not mutually exclusive and you can use them at the same time. In that case, night mode is active as soon as at least one criterion is true.

## Limitations

This blueprint intentionally does not handle some adaptive-lighting features:

- No color handling: only white temperature and brightness are adjusted throughout the day.
- No alternative curve presets: the selected parameters are the ones that match my needs.
- No manual start and end times: only sunrise and sunset at your home location are used.

On the automatic turn-on and turn-off side, I covered all the needs in my home, but there are probably other cases that I have not thought about.

If you have suggestions to improve the whole thing, I am always interested, even if the automation generated by the blueprint is already fairly complex.

## Warning

I did not directly code this blueprint myself. I used tools such as Codex and Claude Code to create it. It is therefore provided without any guarantee, except that it works correctly in my own setup. I tested it with many configurations and many lights, and I have not noticed any issue.

All French texts were written by me. Those tools handled the translation.
