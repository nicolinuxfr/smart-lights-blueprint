# Blueprint lumières intelligentes

Ce blueprint intègre tout le nécessaire pour contrôler des éclairages gérés par Home Assistant. Il allume et éteint des lumières en fonction de capteurs et en option, peut adapter l'éclairage tout au long de la journée.

[Version anglaise](README.md)

## Installation

Cliquez sur ce bouton pour ouvrir votre instance Home Assistant et importer le blueprint dans la foulée :

[![Ouvrez votre instance Home Assistant et affichez la boîte de dialogue d'importation de blueprint.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fnicolinuxfr%2Fsmart-lights-blueprint%2Fgh-pages%2Ffr%2Fsmart_lights.yaml)

Ou copiez cette URL pour la coller dans le champ d'import de blueprint de Home Assistant :

```text
https://raw.githubusercontent.com/nicolinuxfr/smart-lights-blueprint/gh-pages/fr/smart_lights.yaml
```

## Mode d'emploi

Voici comment configurer l'automatisation, pas-à-pas et avec des explications détaillées sur chaque option et son rôle.

### Sélection des éclairages

#### Lumières

Le seul paramètre indispensable au bon fonctionnement de l'automatisation est le choix des lumières. Vous pouvez choisir une seule lampe connectée, en configurer plusieurs, sélectionner un groupe d'éclairages voire une zone ou un tag. 

> [!NOTE]
> Vous pouvez choisir n'importe quel type d'éclairage, l'automatisation devrait s'adapter automatiquement à ses capacités. Si ce n'est pas le cas, n'hésitez pas à [ouvrir une *issue*](https://github.com/nicolinuxfr/smart-lights-blueprint/issues/new) en donnant les détails sur l'éclairage, pour que je corrige le bug.

### Configuration de l'allumage et de l'extinction automatiques

#### Capteurs d’allumage et extinction

Pour que l'automatisation allume et éteigne les lumières automatiquement, sélectionnez au moins un capteur binaire dans le champ « Capteurs d’allumage et extinction ». Vous pouvez sélectionner des capteurs de mouvements ou de présence, des capteurs d'ouverture ou tout autre type de capteur vrai ou faux.

> [!TIP]
> Pour donner un exemple, j'utilise un capteur binaire qui signale que mon ordinateur de bureau est actif ou que mon téléviseur est allumé, ce qui permet de maintenir les lumières associées, même si les autres capteurs ne sont plus activés.

Les lumières s'allumeront dès lors qu'au moins un des capteurs sélectionnés devient vrai. Elles s'éteindront dès que tous les capteurs sélectionnés sont faux. 

#### Maintenir la lumière avec les portes ouvertes

Cette option distingue les portes des autres capteurs dans la liste et maintient les lumières allumées tant qu'elles restent ouvertes. Par défaut, ces capteurs sont gérés différemment et ne servent qu'à allumer la lumière, pas à la maintenir allumée.

#### Délai avant extinction

Choisissez la durée avant d'éteindre les lumières, une fois que tous les capteurs deviennent inactifs (2 minutes par défaut). 

#### Allumage avec interrupteur

Cette option est pensée pour contrôler la lumière depuis un interrupteur physique connecté. Au lieu de gérer l'interrupteur directement dans l'automatisation, ce qui obligerait à gérer trop de cas de figure différents, vous pouvez choisir une entité de type entrée logique (`input_boolean`) qui sera contrôlée depuis une autre automatisation.

Les lumières seront immédiatement allumées et éteintes quand l'entité choisie change de statut. Ce fonctionnement est indépendant du reste et l'extinction aura lieu même si un capteur de mouvements est encore actif, par exemple.

> [!TIP]
> Pour plus de cohérence, son état est synchronisé avec les allumages et extinctions automatisés. Concrètement, si les lumières sont allumées parce qu'un capteur de mouvement déclenche l'automatisation, alors le capteur dédié à l'interrupteur sera lui aussi allumé, et vice-versa.

Laissez le champ vide si vous ne voulez pas utiliser cette option.

#### Entités de contrôle

Choisissez une ou plusieurs entités type entrée logique (`input_boolean`) qui bloqueront les allumages et extinctions automatiques **si elles sont vraies**. Cette option est utile pour s'assurer que des lumières restent allumées. 

Laissez le champ vide si vous ne souhaitez pas utiliser cette option.

### Éclairage adaptatif

L'éclairage adaptatif modifie les paramètres des éclairages tout au long de la journée en suivant la course du soleil. Le principe général est d'avoir une lumière plus chaude et moins lumineuse le matin et le soir, une lumière plus froide et forte autour de midi quand le soleil est à son zénith.

#### Activer l'éclairage adaptatif

La case doit être cochée pour que l'automatisation adapte les paramètres des éclairages sélectionnés. Sans cela, l'automatisation se contentera d'allumer et éteindre les lumières. 

#### Paramètres de luminosité et température

Les options suivantes sont assez explicites : définissez les valeurs minimales et maximales désirées et l'automatisation travaillera à l'intérieur de ce cadre. L'idée est de choisir la luminosité et la température des blancs pour le matin et le soir et celles pour le milieu de la journée, quand le soleil est au point le plus haut.

L'automatisation calcule automatiquement deux courbes, une pour la luminosité et une pour la température. Tant que des lumières contrôlées sont allumées, les nouvelles valeurs sont transmises toutes les 5 minutes, avec une transition pour les faire évoluer en douceur.

#### Réglages spécifiques la nuit

Cochez la case pour appliquer des réglages différents la nuit. Par défaut, les valeurs minimales sélectionnées précédemment sont utilisées. Si vous préférez d'autres valeurs, cochez l'option et choisissez la température et la luminosité en-dessous.

> [!NOTE]
> Par défaut, la nuit dépend du soleil et elle est calculée automatiquement par Home Assistant. L'automatisation tient toutefois compte de vos préférences, définies dans la suite de l'automatisation.

#### Entité de contrôle

Même principe que pour l'allumage et l'extinction automatique, choisissez une entité de type entrée logique (`input_boolean`) qui désactivera l'éclairage adaptatif si elle est elle-même désactivée. Le cas échéant, le dernier réglage sera maintenu tant qu'elle restera inactive.

Les deux options suivantes sont liées à celle-ci : 

- **Réactivation automatique** : par défaut, l'automatisation ne gère pas l'entité de contrôle, mais si vous le souhaitez, elle peut être réactivée dès lors que les lumières contrôlées sont toutes éteintes ;
- **Désactiver avec de la couleur** : en cochant cette option, l'entité de contrôle sera automatiquement désactivée si une lumière passe aux couleurs. L'idée ici étant que l'automatisation ne gère que le blanc, mais vous pouvez activer temporairement des couleurs et les maintenir tant que l'entité de contrôle n'est pas réactivée.

Ces deux options peuvent être activées en même temps, auquel cas les lumières reviendront au blanc après leur extinction.

#### Ajuster avec la météo

Sélectionnez une entité de type météo pour activer un léger ajustement de la température de blanc et de la luminosité en fonction des conditions météorologiques. C'est subtil, mais les lumières seront un petit peu moins lumineuses et un petit peu plus chaudes que les valeurs maximales sélectionnées lorsqu'il fait mauvais temps.

### Mode nuit

L'automatisation gère différemment le jour et la nuit, avec deux objectifs opposés, à choisir en fonction de vos préférences. Cette section permet aussi de définir ce qu'est la nuit, avec plusieurs options pour adapter l'automatisation à un maximum de besoins.

#### Allumage automatique

Par défaut, l'automatisation ne travaille que de jour, ce qui veut dire que les lumières ne s'allument pas de nuit. Changez ce paramètre pour inverser son comportement et n'activer les lumières que de nuit, ou alors pour activer l'automatisation en permanence. 

> [!NOTE]
> Précisons que cela ne concerne que l'allumage automatique des lumières à partir d'un capteur. Par choix, l'allumage par l'entité gérée par un interrupteur est fonctionnel en permanence : si vous cliquez sur un interrupteur, vous voulez toujours allumer ou éteindre les lumières. 

#### Utiliser la position du soleil

Par défaut, l'automatisation utilise la position du soleil fournie par Home Assistant pour déterminer s'il fait jour ou nuit. Dès que le soleil est levé, il fait jour, dès qu'il est couché, il fait nuit. 

Vous pouvez décocher l'option, à condition toutefois de configurer une des deux autres méthodes pour déterminer qu'il fait nuit.

#### Capteurs de luminosité (optionnel)

Première méthode alternative : choisissez des capteurs de luminosité pour le mode nuit. Si vous sélectionnez plusieurs capteurs, l'automatisation calculera automatiquement la valeur moyenne.

Le champ suivant permet de déterminer le seuil de luminosité à partir duquel il fait jour (30 lux par défaut). Toute valeur inférieure sera alors considérée comme nuit.

#### Entité mode nuit (optionnel)

Deuxième méthode alternative : une entité de type entrée logique (`input_boolean`) ou un capteur binaire (`binary_sensor`) qui détermine le mode nuit quand l'entité ou le capteur est actif.

> [!TIP]
> Ces trois méthodes ne sont pas exclusives et vous pouvez les utiliser en même temps. Dans ce cas, le mode nuit est actif dès lors qu'au moins un critère est vrai. 

## Limites

Ce blueprint ne gère volontairement pas certaines fonctionnalités liées à l'éclairage adaptatif : 

- Pas de gestion des couleurs, seule la température du blanc et la luminosité sont ajustés tout au long de la journée ;
- Pas de réglages différents des courbes, les paramètres retenus sont ceux qui conviennent à mes besoins ;
- Pas d’ajustements possibles sur les heures de début et fin, seules les heures de lever et coucher du soleil à la position de votre domicile sont utilisées.

Du côté des allumages et extinctions, j'ai couvert tous les besoins de mon domicile, mais il y a sûrement d'autres cas de figure que je n'ai pas envisagés.

Si vous avez des suggestions pour améliorer l'ensemble, je suis toujours preneur, même si l'automatisation générée par le blueprint est déjà bien complexe.

## Mise en garde

Je n’ai pas directement codé ce blueprint moi-même, j’ai utilisé des outils comme Codex et Claude Code pour le créer. Il est ainsi proposé sans garantie, si ce n’est qu’il fonctionne correctement chez moi. Je l’ai testé avec de multiples configurations et de nombreux éclairages et je n’ai noté aucun problème.

Tous les textes en français ont été écrits par mes soins. Ces outils se sont chargés de la traduction.
