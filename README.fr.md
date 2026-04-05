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
2. Renseignez les **Capteurs d'allumage** et/ou l'**Interrupteur** si vous voulez l'allumage/extinction automatique.
3. Utilisez **Mode nuit** pour choisir quand l'allumage automatique par capteur est autorisé.
4. Ouvrez **Éclairage adaptatif** uniquement si vous voulez des valeurs adaptatives ou des réglages dédiés la nuit.

## Configuration

### Paramètres racine

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Lumières** | Lumières, appareils ou zones à contrôler | — |

### Paramètres principaux

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Capteurs d'allumage** | Capteurs binaires utilisés pour l'allumage/extinction automatique | `[]` |
| **Délai d'extinction** | Délai avant extinction après l'inactivité des capteurs | `00:02:00` |
| **Interrupteur** | `input_boolean` optionnel utilisé comme interrupteur externe qui allume ou éteint toujours immédiatement les lumières gérées, tout en restant synchronisé avec leur état global allumé/éteint | `""` |

### Mode nuit

Cette section sert uniquement à déterminer quand le blueprint doit considérer qu'il fait nuit, et si l'allumage automatique par capteur doit fonctionner le jour, la nuit, ou les deux. Les valeurs d'éclairage de nuit se règlent dans **Éclairage adaptatif**.

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Allumage automatique** | Choisit si l'allumage via capteur est autorisé en journée, la nuit, ou en permanence | `day` |
| **Capteurs de luminosité** | Critère optionnel de faible luminosité ajouté en mode OU à la détection du mode nuit | `[]` |
| **Seuil de luminosité** | Le mode nuit s'active quand la luminosité moyenne passe sous cette valeur | `30 lx` |
| **Entité de critère nuit** | `input_boolean` ou `binary_sensor` optionnel ajouté en mode OU à la détection du mode nuit | `""` |

### Allumage auto – Options

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Maintenir les lumières avec portes ouvertes** | Les capteurs de porte/fenêtre ouverts maintiennent les lumières allumées | `false` |
| **Entités de contrôle** | Entités `input_boolean` devant rester désactivées pour l'allumage/extinction auto | `[]` |

### Éclairage adaptatif

| Paramètre | Description | Défaut |
|-----------|-------------|--------|
| **Activer l'éclairage adaptatif** | Active ou désactive la luminosité et la température de blanc adaptatives | `false` |
| **Luminosité minimale** | Luminosité autour du lever et du coucher du soleil | `30 %` |
| **Luminosité maximale** | Luminosité autour du milieu de journée | `100 %` |
| **Température minimale** | Température de blanc la plus chaude autour du lever et du coucher du soleil | `2700 K` |
| **Température maximale** | Température de blanc la plus froide autour du milieu de journée | `5500 K` |
| **Réglages différents la nuit** | Active des valeurs adaptatives dédiées quand le mode nuit est actif | `false` |
| **Luminosité spécifique la nuit** | Luminosité dédiée appliquée la nuit quand l'option ci-dessus est activée | `20 %` |
| **Température spécifique la nuit** | Température de blanc dédiée appliquée la nuit quand l'option ci-dessus est activée | `2200 K` |
| **Entité de contrôle adaptatif** | `input_boolean` ou `binary_sensor` optionnel qui autorise les mises à jour adaptatives | `""` |
| **Réactivation automatique** | Réactive l'entité de contrôle adaptatif quand toutes les lumières gérées s'éteignent | `false` |
| **Désactiver sur mode couleur** | Désactive l'entité de contrôle adaptatif quand une lumière gérée passe en mode couleur | `false` |
| **Entité météo** | Entité météo optionnelle utilisée pour décaler les valeurs adaptatives | `""` |

## Combinaisons possibles

- **Allumage/extinction automatique uniquement** : renseignez les **Capteurs d'allumage**, des **entités de contrôle** et/ou l'**Interrupteur**, sans activer l'éclairage adaptatif.
- **Éclairage adaptatif uniquement** : activez l'éclairage adaptatif et laissez les **Capteurs d'allumage**, l'**Interrupteur** et les **entités de contrôle** vides si vous ne voulez pas d'allumage/extinction automatique.
- **Les deux activés** : combinez les entrées d'allumage/extinction automatique avec l'éclairage adaptatif.

## Conditions d'allumage

Ces conditions s'appliquent uniquement à l'allumage via capteur. L'interrupteur optionnel les contourne et bascule toujours les lumières immédiatement. Il contourne aussi les entités de contrôle ci-dessous.

- La **détection de nuit** commence avec `sun.sun` sous l'horizon.
- Les **capteurs de luminosité + seuil** peuvent aussi activer le mode nuit quand la luminosité moyenne passe sous le seuil.
- L'**entité de critère nuit** peut aussi activer le mode nuit quand elle est `on`.
- Ces critères de nuit sont combinés en mode OU : un seul suffit à activer le mode nuit.
- **Allumage automatique = day** : l'allumage via capteur fonctionne uniquement quand le mode nuit n'est pas actif.
- **Allumage automatique = night** : l'allumage via capteur fonctionne uniquement quand le mode nuit est actif.
- **Allumage automatique = day and night** : l'allumage via capteur fonctionne en permanence.

## Notes

- L'allumage/extinction automatique devient actif dès qu'au moins un **Capteur d'allumage**, un **Interrupteur** ou une **entité de contrôle** est configuré.
- L'interrupteur optionnel est synchronisé à partir des lumières gérées : il s'active quand elles sont toutes allumées et se désactive quand elles sont toutes éteintes, sans relancer des commandes d'éclairage inutiles.
- Les valeurs adaptatives sont appliquées lorsque la première lumière gérée s'allume depuis un état où tout était éteint, puis rafraîchies toutes les 5 minutes tant que des lumières compatibles restent allumées.
- Quand l'éclairage adaptatif est activé, un allumage manuel via l'interrupteur continue de fonctionner la nuit même si l'allumage automatique par capteur est limité à la journée.
- Si **Réglages différents la nuit** est désactivé, l'éclairage adaptatif retombe sur les valeurs minimales par défaut pendant la nuit.
- Le blueprint continue de fonctionner quand les lumières sont sélectionnées via des entités, des appareils ou des zones.
- **Réactivation automatique** et **Désactiver sur mode couleur** ne prennent effet que si l'entité de contrôle adaptatif est un `input_boolean`.
- Le blueprint conserve maintenant 20 traces et n'utilise plus l'écouteur global `state_changed` qui pouvait remplir l'historique de traces d'exécutions vides.
