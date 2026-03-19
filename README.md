#  Dashboard SITADEL - Construction en Île-de-France

Ce projet est une application web interactive permettant de visualiser et d'analyser les données **SITADEL** (système d'information et de traitement des données élémentaires sur les logements et les locaux). 

L'objectif est de suivre l'évolution des **autorisations de construire** et des **mises en chantier** de logements à travers les départements de l'Île-de-France.

##  Lien de l'application
L'application est déployée sur Render et consultable ici : 👉 [https://sitadel-idf.onrender.com] 

##  Fonctionnalités
- **Vue d'ensemble (KPIs)** : Visualisation rapide du nombre total d'autorisations, de mises en chantier et du taux de réalisation.
- **Analyse Temporelle** : Comparaison annuelle des logements autorisés vs commencés via des graphiques interactifs (Bar & Line charts).
- **Répartition par Type** : Analyse de la part des logements collectifs, individuels (purs ou groupés) et des résidences.
- **Analyse Géographique** : Filtres par départements (75, 77, 78, 91, 92, 93, 94, 95).
- **Interactivité complète** : Filtres dynamiques par plage d'années et sélection multiple de zones géographiques.

##  Technologies utilisées
- **Langage** : Python 3.x
- **Framework Dashboard** : [Dash](https://dash.plotly.com/) (par Plotly)
- **Composants UI** : Dash Bootstrap Components (Thème : Flatly)
- **Manipulation de données** : Pandas
- **Format de données** : Apache Parquet (pour des performances optimales et un stockage léger)
- **Serveur de production** : Gunicorn
- **Déploiement** : Render

##  Structure du projet
- `app.py` : Code principal de l'application Dash (Layout et Callbacks).
- `processed/` : Contient les bases de données nettoyées au format `.parquet`.
- `requirements.txt` : Liste des dépendances Python pour le déploiement.
- `Procfile` : Fichier de configuration pour le lancement sur Render.

##  Installation locale
Pour lancer ce projet sur votre machine :

1. Clonez le dépôt :
   ```bash
   git clone [https://github.com/habib-07/sitadel-idf.git](https://github.com/habib-07/sitadel-idf.git)
