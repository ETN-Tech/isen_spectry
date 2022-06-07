Repo initial : https://github.com/Thiebosh/M2_contratpro_5

# M2_contratpro_5

Ce projet a été conceptualisé puis réalisé de septembre 2021 à mai 2022 dans le cadre de la 5e année d'école d'ingénieurs informatique ISEN LILLE par Thibaut Juzeau, Antoine Asset, Etienne Schelfhout, Benjamin Grosbety, Youssef Houra et Delano Koyouo.

<hr>

Il consiste en une application collaborative qui permet de rédiger des spécifications sous forme de mindmap arborescente, afin de générer rapidement des prototypes opérationnels. Les spécifications sont guidées par une syntaxe prédéfinie et la génération est rendue possible par un compilateur associé à cette syntaxe. Ainsi, les utilisateurs peuvent développer leur propre syntaxe et compilateur afin de pouvoir générer en no code tout type d'application.

## Exécution

Pour exécuter l'application sur un serveur, il suffit d'ajouter les variables d'environnement et les fichiers de crédentials (voir plus bas), puis d'exécuter docker-compose.

Les variables d'environnement sont stockés dans un fichier '.env' stocké à la racine de l'application. Elles prennent la forme suivante :
```
MONGO_URL=***
MONGO_USERNAME=***
MONGO_PASSWORD=***
```

Le fichier de credentials sont stockés dans un fichier 'service_account.json', stocké dans les dossier 'credentials' à la racine des dossiers 'rest_server' et 'websocket_server'. Il est à récupérer sur un compte google, en tant que compte de service, de façon à accéder à son Drive sans connexion explicite.

## Technologies

Le projet est cross langages:
- Le front est en ReactJS, avec un service via Nginx
- Le back dédié à la gestion des utilisateurs et des projets est en Quart python
- le back dédié à la gestion collaborative des specs et des proto est en socket python
- l'élément de back dédié à la génération des prototypes est en c++, avec un makefile en bash
- le back dédié à l'exécution des prototypes est en php

Les communications réseau sont soit de type http, soit de type socket, dépendamment des serveurs. Dans les deux cas, les transferts d'information sont réduits au minimum d'information, à l'aide de la syntaxe json et de choix stratégiques.

La construction de chaque serveur est décrite dans un dockerfile et l'exécution coordonnée de tous les serveurs est orchestrée à l'aide d'un docker-compose.

## Ajout de syntaxe + compilateur

Pour ajouter une syntaxe, il faut :
- Dans la DB, table 'syntax', ajouter un document et relever l'id du document
- Dans le docker-compose, comme argument de 'socket', ajouter cet id dans la liste des syntaxes
- Dans les fichiers de 'front_builder_react', dossier 'public/syntaxes', ajouter le fichier json et le nommer avec l'id syntaxe
- Dans les fichiers de 'websocket_server', dossier 'cpp', ajouter un dossier du nom de l'id syntaxe et y ajouter les fichiers cpp

## Base de données : tables et documents types

Nous avons utilisé une base de données MongoDB, hébergée en ligne, composée de 3 tables:
- 'accounts' stocke les utilisateurs. Son document type est :
```
{
    _id: ObjectId(""),
    name: string,
    password: string
}
```
- 'projects' stocke les projets. Son document type est :
```
{
    _id: ObjectId(""),
    name: string,
    users: [
        userId as string
    ],
    description: string,
    syntax_id: syntaxId as string,
    creation: date,
    last_specs: date,
    latest_proto: bool,
    specs: {
        root: {}
    },
    pages: [
        {
            Default: string
        }
    ],
    session: {},
    chat: []
}
```
- 'syntax' stocke les syntaxes. Son document type est :
```
{
    _id: ObjectId(""),
    name: string,
    description: string
}
```

## Schéma d'ensemble
![global scheme](https://github.com/Thiebosh/M2_contratpro_5/raw/main/documentation/global%20scheme.png)
