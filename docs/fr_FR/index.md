# Plugin Zigbee

Le plugin Zigbee permet de communiquer avec la pluspart des équipements Zigbee existants. Il se base sur le (super) projet Zigpy qui est compatible avec les clef zigbee suivantes :

- Deconz. Testé et validé par l'équipe Jeedom. Il n'y a pas besoin d'avoir Deconz d'installé
- EZSP (clef basé sur un chupset Silicon Labs). En cours de test par l'équipe Jeedom
- X-bee. Non testé par l'équipe Jeedom
- Zigate. Non testé par l'équipe, marqué en experimental chez Zigpy
- ZNP (Texas Instrument, Z-stack 3.X.X). Non testé par l'équipe, marqué en experimental chez Zigpy
- CC (Texas Instrument, Z-stack 1.2.X). Non testé par l'équipe, marqué en experimental chez Zigpy

# Configuration du plugin

Après installation du plugin, il vous suffit de bien installer les dépendances, de selectionner votre type de clef, le port (attention seul le type de clef deconz support le port en auto) et de lancer le demon. Vous pouvez aussi choisir le canal pour le zigbee.

>**IMPORTANT**
>
>Tout changement de canal nécessite forcement un redemarrage du démon. Un changement de canal peut aussi nécessiter une reinclusion de certain module


# Inclusion de module

L'inclusion est la partie la plus compliqué en Zigbee. Bien que simple l'opération est à faire souvent plusieurs fois. Coté plugin c'est facile il suffit de cliquer sur le bouton "Mode inclusion", une fois fait vous avez 3minutes pour inclure votre équipement.

Coté équipement ca change en fonction du module, il faut se referer à la documentation de celui-ci à chaque fois.

>**IMPORTANT**
>
>Ne surtout pas oublier de faire une remise à zero (reset) du module avant tout inclusion

# Equipement

Une fois inclus Jeedom doit reconnaitre automatiquement votre module (si ce n'est pas le cas voir chapitre suivant) et donc créer les commandes qui vont bien. A noter qu'a cause de bug dans certain firmware (Ikea, Sonoff...) il est parfois necessaire de choisir le type de module directement dans la liste "Equipement" puis de sauvegarder pour avoir les bonnes commandes.

Vous avez dans l'onglet équipement les parametres suivants :

- **Nom de l'équipement Zigbee** : nom de votre équipement Zigbee
- **ID** : identifiants unique de l'équipements, meme lors d'une reinclusion (ou meme si vous changez de type de clef zigbee)
- **Activer**
- **Visible**
- **Objet parent**
- **Bureau**
- **Catégorie**
- **Ne pas attendre le retour d'éxécution des commandes (plus rapide mais moins fiable)** : n'attends pas la validation de clef pour dire que la commande s'est executé. Ca rend la main plus vite mais ne garantie pas que tout c'est bien passé

Dans l'onglet commande vous retrouvez les commandes de votre module (si celui-ci a bien été reconnu)

## Commande pour les experts

Pour les experts voici comment marche les commandes :

- ``attributes::ENDPOINT::CLUSTER_TYPE::CLUSTER::ATTRIBUT::VALUE``, permet d'écrire la valeur d'un attribut (attention tout les attributs ne peuvent etre changé) avec :
  - ``ENDPOINT`` : numéro du endpoint
  - ``CLUSTER_TYPE`` : type de cluster (IN ou OUT)
  - ``CLUSTER`` : numéro du cluster
  - ``ATTRIBUT`` : numéro de l'attribut
  - ``VALUE`` : valeur à écrire
Exemple : ``attributes::1::in::513::18::#slider#*100``, ici on va ecrire l'attribut dans l'endpoint 1, cluster entrant (``in``) 513, attribut 18 avec pour valeur celle du ``slider*10``
- ``ENDPOINT::CLUSTER:COMMAND::PARAMS``, permet d'éxecuter une commande server, avec :
  - ``ENDPOINT`` : numéro du endpoint
  - ``CLUSTER`` : nom du cluster
  - ``COMMAND`` : nom de la commande
  - ``PARAMS`` parametre dans le bonne ordre séparé par des ::
Exemple : ``1::on_off::on``, ici on execute la commande ``on`` sur l'endpoint 1 du cluster ``on_off`` sans parametres
Exemple : ``1::level::move_to_level::#slider#::0``, ici on execute la commande ``move_to_level`` sur l'endpoint 1 du cluster ``level`` avec les parametres ``#slider#`` et ``0``

# Mon module n'est pas reconnu

Si votre module n'est pas reconnu par jeedom (pas de commande) mais bien inclus alors il faut demander à l'équipe Jeedom de l'ajouter.

>**IMPORTANT**
>
>L'équipe Jeedom se reserve le droit de refuser toute demande d'intégration il vaut toujours mieux prendre un module deja compatible

Pour cela il faut fournir les éléments suivant (toute demande incomplete sera refusé sans réponse de la part de l'équipe Jeedom) :

- Donner le modele exacte de votre module (avec un lien vers la page de vente)
- Sur la page de l'équipement cliquer sur configuration puis onglet "Informations brutes" et envoyer le contenu à l'équipe Jeedom
- Mettre le démon en debug (et le redemarrer), faire des actions sur l'équipement (si c'est un capteur de température faire varier la température par exemple, si c'est une vanne faire varier la consigne...) et envoyer le log en debug zigbee (attention a bien prendre le zigbee et pas le zigbeed)

# Touchlink

Touchlink ou Lightlink est une partie particuliere du Zigbee qui permet d'envoyer des ordres de gestion à un module si on est très pres de celui-ci (50cm). Ca sert par exemple a faire un reset sur les ampoules qui n'ont pas de bouton.

Cela concerne donc tous ce qui est ampoules Zigbee type Philips Hue, Ikea, Osram, Icasa... et j'en passe. Le principe est très simple pour pouvoir associer ce type de module à un réseaux zigbee il faut d'abord faire un reset. Ensuite lors du redemarrage le module va automatiquement essayer de s'associer au premier réseaux Zigbee ouvert qu'il trouve.

## Faire un reset en Touchlink

C'est la partie compliqué (comme toujours en Zigbee le plus dur c'est le reset/association). Plusieurs methodes :

- Faire 5 ou 6 fois du on/off rapidement, l'ampoule clignote normalement rapidement à la fin pour signaler que c'est bon (marche rarement)
- Utiliser une télécommande zigbee et
  - appuyer sur en meme temps le bouton ON et OFF pendant 5 à 10 secondes près de l'ampoule alimentée (attention sur certaine ampoule il faut parfois éteindre/allumer l'ampoule juste avant) pour les télécommandes Philips hue
  - appuyer sur le bouton reset (a coté de la batterie) pendant 5 à 10 secondes près de l'ampoule alimentée (attention sur certaine ampoule il faut parfois éteindre/allumer l'ampoule juste avant) pour les télécommandes Ikea
- Pour les ampoules hue vous pouvez aussi les inclures sur le pont hue puis les supprimer de celui-ci

# FAQ

>**Le LQI ou le RSSI est à N/A
>
>C'est normalement suite à un redemarrage du réseaux Zigbee les valeurs sont vidées, il faut attendre que le module recomunique pour que les valeurs reviennent
