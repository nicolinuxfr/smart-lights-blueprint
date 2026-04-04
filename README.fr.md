# Blueprint Smart Lights

Contrôlez une ou plusieurs lumières avec un seul blueprint. Il peut gérer l'allumage/extinction automatique par capteurs, l'éclairage adaptatif, ou les deux en même temps.

[Read in English](README.md)


## Installation

[![Ouvrez votre instance Home Assistant et affichez la boîte de dialogue d'importation de blueprint.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fnicolinuxfr%2Fsmart-lights-blueprint%2Fgh-pages%2Ffr%2Fsmart_lights.yaml)

Ou copiez cette URL manuellement :

```text
https://raw.githubusercontent.com/nicolinuxfr/smart-lights-blueprint/gh-pages/fr/smart_lights.yaml
```

## Démarrage rapide

1. Sélectionnez les **Lumières** cibles.
2. Activez **l'allumage/extinction automatique** et/ou **l'éclairage adaptatif**.
3. Renseignez uniquement les sections utiles pour les fonctions activées.

## Configuration

### Paramètres racine

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Lumières** | Lumières, appareils ou zones à contrôler | — |
| **Activer l'allumage/extinction automatique** | Active ou désactive l'allumage/extinction piloté par capteurs | `true` |
| **Activer l'éclairage adaptatif** | Active ou désactive la luminosité et la température de blanc adaptatives | `false` |

### Allumage auto – Essentiel

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Capteurs** | Capteurs binaires utilisés pour l'allumage/extinction automatique | `[]` |
| **Délai d'extinction** | Délai avant extinction après l'inactivité des capteurs | `00:02:00` |

### Allumage auto – Options

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Entité interrupteur** | `input_boolean` optionnel utilisé comme interrupteur externe qui allume ou éteint toujours immédiatement les lumières gérées, tout en restant synchronisé avec leur état global allumé/éteint | `""` |
| **Uniquement la nuit** | Autorise l'allumage via capteur seulement quand le soleil est sous l'horizon | `false` |
| **Capteurs de luminosité** | Capteurs utilisés par les règles de faible luminosité | `[]` |
| **Seuil de luminosité** | La luminosité moyenne doit être inférieure à cette valeur pour que la condition de luminosité autorise l'allumage | `30 lx` |
| **Maintenir les lumières avec portes ouvertes** | Les capteurs de porte/fenêtre ouverts maintiennent les lumières allumées | `false` |
| **Interrupteurs de contrôle devant être activés** | Entités `input_boolean` devant rester activées pour l'allumage/extinction auto | `[]` |
| **Interrupteurs de contrôle devant être désactivés** | Entités `input_boolean` devant rester désactivées pour l'allumage/extinction auto | `[]` |

### Adaptatif – Luminosité et couleur

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Luminosité minimale** | Luminosité autour du lever et du coucher du soleil | `30 %` |
| **Luminosité maximale** | Luminosité autour du milieu de journée | `100 %` |
| **Température minimale** | Température de blanc la plus chaude autour du lever et du coucher du soleil | `2700 K` |
| **Température maximale** | Température de blanc la plus froide autour du milieu de journée | `5500 K` |

### Adaptatif – Options

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Entité de contrôle adaptatif** | `input_boolean` ou `binary_sensor` optionnel qui autorise les mises à jour adaptatives | `""` |
| **Réactivation automatique** | Réactive l'entité de contrôle adaptatif quand toutes les lumières gérées s'éteignent | `false` |
| **Désactiver sur mode couleur** | Désactive l'entité de contrôle adaptatif quand une lumière gérée passe en mode couleur | `false` |
| **Entité météo** | Entité météo optionnelle utilisée pour décaler les valeurs adaptatives | `""` |
| **Entité de mode nuit** | `input_boolean` ou `binary_sensor` optionnel qui active des valeurs fixes de nuit | `""` |
| **Luminosité nuit** | Luminosité fixe pendant le mode nuit | `20 %` |
| **Température nuit** | Température de blanc fixe pendant le mode nuit | `2200 K` |

## Combinaisons possibles

- **Allumage/extinction automatique uniquement** : le blueprint réagit aux capteurs et aux entités de contrôle optionnelles, sans ajustement adaptatif de la luminosité ou de la température.
- **Éclairage adaptatif uniquement** : le blueprint suit les changements d'état des lumières gérées et rafraîchit les valeurs adaptatives pendant qu'elles restent allumées, sans utiliser les capteurs pour l'allumage/extinction.
- **Les deux activés** : l'allumage/extinction par capteurs et les mises à jour adaptatives sont tous deux actifs.

## Conditions d'allumage

Ces conditions s'appliquent uniquement à l'allumage via capteur. L'entité interrupteur optionnelle les contourne et bascule toujours les lumières immédiatement. Elle contourne aussi les interrupteurs de contrôle ci-dessous.

- **Uniquement la nuit** activé : l'allumage via capteur n'est autorisé que lorsque `sun.sun` est sous l'horizon.
- **Capteurs de luminosité + seuil** configurés : l'allumage via capteur est autorisé lorsque la luminosité moyenne est sous le seuil.
- **Les deux configurés** : l'allumage via capteur est autorisé dès qu'une des deux conditions est vraie.
- **Aucune condition configurée** : l'allumage via capteur est toujours autorisé.

## Notes

- L'entité interrupteur optionnelle est synchronisée à partir des lumières gérées : elle s'active quand elles sont toutes allumées et se désactive quand elles sont toutes éteintes, sans relancer des commandes d'éclairage inutiles.
- Les valeurs adaptatives sont appliquées lorsqu'une lumière gérée s'allume puis rafraîchies toutes les 5 minutes tant que des lumières compatibles restent allumées.
- Le blueprint continue de fonctionner quand les lumières sont sélectionnées via des entités, des appareils ou des zones.
- **Réactivation automatique** et **Désactiver sur mode couleur** ne prennent effet que si l'entité de contrôle adaptatif est un `input_boolean`.
