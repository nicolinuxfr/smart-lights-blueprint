# Changelog

## 2026.3

- Initial release: merged auto-lights and adaptive lighting into a single blueprint.
- Two optional features that can be enabled independently:
  - **Automatic on/off**: turn lights on and off based on motion sensors, door sensors, and switches.
  - **Adaptive lighting**: adjust brightness and color temperature based on the sun position, weather conditions, and night mode.
- Switch support (Zigbee buttons, smart switches) with configurable event type filter for toggle behavior.
- Automation runs in `parallel` mode to avoid conflicts between the adaptive tick and turn-off delay.
