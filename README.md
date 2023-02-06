Books-Scraping 
=======

Ce code s'appplique uniquement sur le site _https://books.toscrape.com_.  
Il permet d'enregistrer les informations des livres dans un fichier _.csv_ pour chaque catégorie de livre. 

Comment ça marche ?
----------

Le script énumère toutes les catégories de livres présentes sur la page d'accueil et récupère les _url_ de tous les produits de chaque page de chaque catégorie. Il vient ensuite charger les données des produits dans un sous-dossier _data_ sous la forme d'un fichier _.csv_ correspondant à la catégorie énumérée. Chaque image des livres est chargée dans un sous-dossier _assets_ sous la forme d'un fichier _.png_.


# Pré-requis.

## Installer **git** et **python3** sur son ordinateur.

Ouvrir le terminal, et lancer les commandes suivantes :  
    
    pip install python3
    pip install git


## Créer un **espace de travail**.

Pour créer l'espace de travail, il nous faut un dossier cible sur l'ordinateur pour ce projet.  
Créer un dossier à l'endroit que vous souhaitez. Copier le lien du repository Github, puis depuis le terminal, se placer dans le dossier cible et lancer la commande suivante :
    
    git clone "lien du repository"


## Créer un **environnement virtuel**.

Depuis le terminal, se placer dans le dossier où le repository a été téléchargé, puis rentrer la commande suivante pour créer un environnement virtuel et l'activer :
    
    python -m venv env
    source env/bin/activate

_(Remplacer "bin" par "scripts" si vous êtes sur Windows.)_
    

## Installer les **requirements** dans l'environnement.
Toujours dans le terminal depuis le dossier cible, lancer la commande suivante :

    pip install -r requirements.txt

Vérifier l'installation en rentrant la commande suivante :

    pip freeze

Les requirements présents dans le fichier _requirements.txt_ doivent apparaitre.
  
 
## Créer un sous-dossier _assets_ et un sous-dossier _data_.
Créer 2 sous-dossiers qui récupèreront les _data_ des différents produits.
Le sous-dossier _assets_ récupèrera les images en _.png_ des livres.  
Le sous-dossiers _data_ récupèrera les fichiers _.csv_ pour chaque catégorie contenants les donnés des livres.
 
 
Lancer le script python.
----------

Depuis le terminal, toujours dans le dossier cible, lancer la commande suivante :
    
    python books-scraping.py


---

Alexandre Brisé, Books_Scraping, Février 2023
