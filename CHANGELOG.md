# Changelog

## 2026.4.4

- When the automation is reactivated, the lights will be turned off after the set delay if the sensors are  off. 

## 2026.4.3

- Night mode revamped :
  - You can choose to automatically turn on the lights when a motion sensor or door is active at night, during the day or both ;
  - "Night" is defined by default using the sun position, and you can add two additional sources : a light sensor with a treshold and an entity ;
  - The night settings for the adaptative light are in the adaptative settings now.

## 2026.4.2

- Much better texts and organization, hopefully.

## 2026.4.1

- Sync of the switch entity based on the lights (keep everything more stable and useful). The idea being, you can always toggle the entity from a physical switch using an automation and get the proper result.
- Reorganisation of the blueprint's "UI".
- Optimization of the code, to avoid too many triggers.

## 2026.4

- Big refactor and simplification of the blueprint, hopefully without breaking anything ;
- The entity linked to a switch should turn the lights on and off immédiately.
- 
## 2026.3.1

- Use an optional `input_boolean` instead of trying to handling a real switch, it was too hard.

## 2026.3

- Initial release.
