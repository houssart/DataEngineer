# DataEngineering - TENNIS L'équipe
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Scrapy](https://img.shields.io/badge/Scrapy-%2314D08C.svg?style=for-the-badge&logo=scrapy&logoColor=white)
![Dash](https://img.shields.io/badge/Dash-%2574D08D.svg?style=for-the-badge&logo=dash&logoColor=white)
![Mongo](https://img.shields.io/badge/Mongo-FF0000?style=for-the-badge&logo=mongodb&logoColor=white)

## Description

Dans ce projet on scrape le site [L'équipe](https://www.lequipe.fr/Tennis/) avec Scrapy (plusieurs pages à scraper) et plus particulièrement la partie Tennis, les résultats des Grands Chelems hommes et femmes (gagnants - finaliste - score), et les classements ATP et WTA. On stocke toutes ces données dans une base de données MongoDB (on stocke également dans un fichier CSV en cas de problème de scraping dans ScrapyTennis/Data). Afin de visualiser ces données dans un dashboard on utilise Dash, vous pourrez y retrouver différents graphiques et diverses informations sur les joueurs et compétitions. Afin de faciliter l'ensemble on organise tout avec Docker Compose afin de tout manipuler plus aisément.

## Prérequis

Afin de tout exécuter correctement il y a besoin de :
- Docker Compose
- Docker Desktop

## Utilisation

Afin de correctement utiliser ce projet, il faut suivre ces différentes étapes :

1. **Images Docker** : Se placer à la racine du projet et faire la commande ```docker-compose build``` dans le terminal

2. **Lancement des conteneurs** : Démarrer ensuite les conteneurs avec la commande ```docker-compose -d``` dans le terminal

3. **Accès au dashboard** : Se rendre à l'adresse : [http://localhost:8050/](http://localhost:8050/)

4. **Arrêt des conteneurs** : Pour arrêter les conteneurs, faire la commande ```docker-compose down -v``` on ajoute "-v" afin de supprimer tous les volumes

## Le dashboard

Pour se rendre sur le dashboard il faut se rendre à l'adresse [ici](http://localhost:8050/). L'idéal est de s'y rendre une fois que le docker scrapy s'éteint (scraping terminé).
Plusieurs graphiques sont disponibles afin de se rendre compte des joueurs les plus dominants de tous les temps. 
Il y a ensuite un menu déroulant sur lequel on peut choisir la compétition (homme ou femme) afin d'en observer les joueurs les plus dominants. 
La dernière partie contient un menu déroulant qui permet de choisir l'année (disponible depuis le début des recensements) à laquelle est ainsi associée nombre d'informations pour chaque compétition (Gagnant, finaliste, score de la finale) ainsi que les classements ATP et WTA de cette année-là.

## Composants

- **Scrapy** : Afin de scraper le site L'équipe Tennis. La spider permet de récupérer les données, on les stocke ensuite dans différents CSV (un pour chaque page) que l'on merge ensuite sur les années en un seul CSV (avec merge_CSV.py).

- **Mongo** : On crée ensuite une base mongo dans laquelle on insert le CSV nouvellement merged.

- **Dash** : On vient ensuite prendre les informations de la base Mongo que l'on utilise pour créer le dashboard intéractif de visualisation de données.

## Auteurs

### Arthur LEROUVILLOIS 
- arthur.lerouvillois@edu.esiee.fr

### Mathieu HOUSSART
- mathieu.houssart@edu.esiee.fr


