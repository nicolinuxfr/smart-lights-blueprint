# Blueprint Smart Lights

Allume et éteint automatiquement des lumières en fonction de capteurs binaires (capteurs de mouvement, capteurs d'ouverture, etc.), avec un éclairage adaptatif optionnel qui ajuste la luminosité et la température de couleur en fonction de la position du soleil.

[Read in English](README.md)

## Installation

[![Ouvrez votre instance Home Assistant et affichez la boîte de dialogue d'importation de blueprint.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fnicolinuxfr%2Fsmart-lights-blueprint%2Fgh-pages%2Ffr%2Fsmart_lights.yaml)

Ou copiez cette URL manuellement :

```
https://raw.githubusercontent.com/nicolinuxfr/smart-lights-blueprint/gh-pages/fr/smart_lights.yaml
```

## Configuration

| Paramètre | Description | Requis | Défaut |
|-----------|-------------|--------|--------|
| **Lumières** | Les lumières à contrôler | Oui | — |
| **Activer l'allumage/extinction auto** | Allume et éteint les lumières en fonction des capteurs et interrupteurs | Non | Activé |
| **Activer l'éclairage adaptatif** | Ajuste la luminosité et la température de couleur en fonction du soleil | Non | Désactivé |

### Allumage auto – Capteurs et délai

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Capteurs** | Capteurs binaires qui déclenchent les lumières (mouvement, ouverture de porte/fenêtre, etc.) | — |
| **Interrupteur** | Un `input_boolean` utilisé comme toggle pour les lumières, généralement basculé par une autre automatisation. Le désactiver éteint immédiatement les lumières | — |
| **Délai d'extinction** | Temps à attendre avant d'éteindre les lumières après que les capteurs sont devenus inactifs | 00:02:00 |

### Allumage auto – Conditions d'éclairage

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Uniquement la nuit** | N'allume les lumières que lorsque le soleil est couché | Désactivé |
| **Capteurs de luminosité** | Capteurs d'éclairement à vérifier avant l'allumage (moyenne si plusieurs) | — |
| **Seuil de luminosité** | Les lumières ne s'allument que si la luminosité moyenne est inférieure à cette valeur | 30 lx |

### Allumage auto – Avancé

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Maintenir avec portes ouvertes** | Les capteurs de porte/fenêtre ouverts empêchent l'extinction | Désactivé |
| **Interrupteurs de contrôle** | Des `input_boolean` qui activent/désactivent l'automatisation (tous doivent être activés) | — |

### Éclairage adaptatif – Luminosité et couleur

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Luminosité minimale** | Luminosité en début et fin de journée | 30 % |
| **Luminosité maximale** | Luminosité au milieu de la journée | 100 % |
| **Température minimale** | Température du blanc en début et fin de journée | 2700 K |
| **Température maximale** | Température du blanc au milieu de la journée | 5500 K |

### Éclairage adaptatif – Avancé

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Contrôle de l'adaptation** | Un `input_boolean` ou `binary_sensor` qui contrôle les adaptations | — |
| **Réactivation automatique** | Réactive l'entité de contrôle quand toutes les lumières s'éteignent. Nécessite un `input_boolean` | Désactivé |
| **Désactivation sur couleur** | Désactive l'entité de contrôle quand une lumière passe en couleur. Nécessite un `input_boolean` | Désactivé |
| **Variation météo** | Entité météo pour ajuster les paramètres selon les conditions climatiques | — |

### Éclairage adaptatif – Mode nuit

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Mode nuit** | Un `input_boolean` ou `binary_sensor` qui active le mode nuit | — |
| **Luminosité nuit** | Luminosité fixe quand le mode nuit est actif | 20 % |
| **Température nuit** | Température du blanc fixe quand le mode nuit est actif | 2200 K |

## Fonctionnement

### Allumage et extinction automatiques

1. Quand un capteur sélectionné devient actif (mouvement détecté, porte ouverte, etc.), les lumières s'allument.
2. Quand tous les capteurs deviennent inactifs, le blueprint attend le délai configuré avant d'éteindre les lumières.
3. Si un capteur redevient actif pendant le délai, le minuteur se réinitialise et les lumières restent allumées.
4. L'entrée **interrupteur** optionnelle utilise un `input_boolean` comme toggle pour les lumières. Vous pouvez le basculer depuis une autre automatisation, par exemple lors de l'appui sur un interrupteur ou bouton physique. Le désactiver éteint toujours les lumières immédiatement.
5. Par défaut, les capteurs de porte/fenêtre restés ouverts n'empêchent pas l'extinction — seuls les capteurs de mouvement/présence sont vérifiés.

#### Conditions d'éclairage

Les conditions d'éclairage n'affectent que l'**allumage** des lumières, que le déclenchement vienne des capteurs ou de l'interrupteur optionnel. L'extinction fonctionne toujours, indépendamment du soleil ou de la luminosité.

- **Uniquement la nuit** : les lumières ne s'allument que quand le soleil est couché, en utilisant l'entité `sun.sun` intégrée à Home Assistant.
- **Capteurs de luminosité + seuil** : les lumières ne s'allument que si la luminosité moyenne est inférieure au seuil.
- **Les deux activés** : les lumières s'allument si **l'une ou l'autre** des conditions est remplie (nuit OU faible luminosité).
- **Aucune condition** : les lumières s'allument toujours quand un capteur se déclenche.

#### Interrupteurs de contrôle

Si un ou plusieurs **interrupteurs de contrôle** sont configurés, ils doivent tous être activés pour que l'automatisation fonctionne. Quand un interrupteur est désactivé, les lumières s'éteignent après le délai configuré. Quand tous les interrupteurs sont réactivés, l'automatisation reprend immédiatement.

### Éclairage adaptatif

Quand cette option est activée, le blueprint ajuste la luminosité et la température de couleur tout au long de la journée en fonction de la position du soleil :

- **Matin/soir** : luminosité réduite, blanc chaud (2700 K par défaut).
- **Midi** : luminosité maximale, blanc plus froid (5500 K par défaut).
- **Nuit** : si le mode nuit est actif, luminosité basse fixe et blanc très chaud.
- **Météo** : ajuste optionnellement la luminosité et la température en fonction des conditions météo (nuageux, pluvieux, etc.).

Les valeurs adaptatives sont appliquées à l'allumage des lumières et mises à jour toutes les 5 minutes tant que les lumières restent allumées.
Les changements d'état des lumières sont aussi bien suivis quand les cibles sont sélectionnées via des entités, des appareils ou des zones.
