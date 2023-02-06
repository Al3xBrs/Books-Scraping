# Books-Scraping
https://books.toscrape.com/ - scraping informations from books


#1 - Installer git et python3 sur son ordinateur.
Ouvrir le terminal, et lancer les commandes suivantes :
    
    pip install python3
    pip install git


#2 - 
Créer un dossier sur l'ordinateur pour ce projet, copier le lien du repository Github, puis depuis le terminal, se placer dans le dossier cible et    lancer la commande suivante :
    
    git clone "lien du repository"


#3 - 
Depuis le terminal, se placer dans le dossier où le repository a été téléchargé, puis rentrer la commande suivante pour créer un environnement virtuel et l'activer :
    
    python -m venv env
    source env/bin/activate

(Remplacer "bin" par "scripts" si vous êtes sur Windows.)
    

#4 -
Toujours dans le terminal depuis le dossier cible, lancer la commande suivante :

    pip install -r requirements.txt

Vérifier l'installation en rentrant la commande suivante :

    pip freeze

Les requirements présents dans le fichier .txt doivent apparaitre.
  
 
#5 - Créer un sous-dossier "assets" et un sous-dossier "data".
 
 
#6 - Lancer le script python : 
depuis le terminal, toujours dans le dossier cible, lancer la commande suivante :
    
    python books-scraping.py
