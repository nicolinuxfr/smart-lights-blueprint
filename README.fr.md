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
2. Choisissez le **Mode de fonctionnement** :
   - **Allumage/extinction automatique uniquement**
   - **Éclairage adaptatif uniquement**
   - **Allumage/extinction automatique + éclairage adaptatif**
3. Renseignez uniquement les sections utiles pour ce mode.

## Configuration

### Paramètres racine

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Lumières** | Lumières, appareils ou zones à contrôler | — |
| **Mode de fonctionnement** | Choisit l'allumage/extinction automatique, l'adaptatif seul, ou les deux | `auto_onoff` |

### Allumage auto – Essentiel

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Capteurs** | Capteurs binaires utilisés pour l'allumage/extinction automatique | `[]` |
| **Délai d'extinction** | Délai avant extinction après l'inactivité des capteurs | `00:02:00` |

### Allumage auto – Options

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Entité interrupteur** | `input_boolean` optionnel utilisé comme interrupteur externe qui allume ou éteint toujours immédiatement les lumières gérées | `""` |
| **Règle d'allumage** | Autoriser l'allumage via capteur toujours, la nuit, sur faible luminosité, ou l'un des deux | `always` |
| **Capteurs de luminosité** | Capteurs utilisés par les règles de faible luminosité | `[]` |
| **Seuil de luminosité** | La luminosité moyenne doit être inférieure à cette valeur quand une règle lux est choisie | `30 lx` |
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
| **Comportement du contrôle adaptatif** | Comportement optionnel appliqué à cette entité de contrôle | `manual` |
| **Entité météo** | Entité météo optionnelle utilisée pour décaler les valeurs adaptatives | `""` |
| **Entité de mode nuit** | `input_boolean` ou `binary_sensor` optionnel qui active des valeurs fixes de nuit | `""` |
| **Luminosité nuit** | Luminosité fixe pendant le mode nuit | `20 %` |
| **Température nuit** | Température de blanc fixe pendant le mode nuit | `2200 K` |

## Modes

- **Allumage/extinction automatique uniquement** : le blueprint réagit aux capteurs et aux entités de contrôle optionnelles, sans ajustement adaptatif de la luminosité ou de la température.
- **Éclairage adaptatif uniquement** : le blueprint suit les changements d'état des lumières gérées et rafraîchit les valeurs adaptatives pendant qu'elles restent allumées, sans utiliser les capteurs pour l'allumage/extinction.
- **Allumage/extinction automatique + éclairage adaptatif** : l'allumage/extinction par capteurs et les mises à jour adaptatives sont tous deux actifs.

## Règles d'allumage

Ces règles s'appliquent uniquement à l'allumage via capteur. L'entité interrupteur optionnelle les contourne et bascule toujours les lumières immédiatement. Elle contourne aussi les interrupteurs de contrôle ci-dessous.

- **Toujours** : l'allumage via capteur est toujours autorisé.
- **Nuit uniquement** : l'allumage via capteur n'est autorisé que lorsque `sun.sun` est sous l'horizon.
- **Faible luminosité uniquement** : l'allumage via capteur n'est autorisé que lorsque la moyenne des capteurs de luminosité sélectionnés est sous le seuil.
- **Nuit OU faible luminosité** : l'allumage via capteur est autorisé dès qu'une des deux conditions est vraie.

## Notes

- Les valeurs adaptatives sont appliquées lorsqu'une lumière gérée s'allume puis rafraîchies toutes les 5 minutes tant que des lumières compatibles restent allumées.
- Le blueprint continue de fonctionner quand les lumières sont sélectionnées via des entités, des appareils ou des zones.
- **Réactiver quand tout est éteint** et **Désactiver sur mode couleur** ne prennent effet que si l'entité de contrôle adaptatif est un `input_boolean`.
