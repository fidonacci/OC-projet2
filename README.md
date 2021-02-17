# OC - DA Python V2 - Projet 2 : Scraper of http://books.toscrape.com/

Pour utitliser le programme, mettez-vous dans le répértoire de votre choix

`$ git clone https://github.com/fidonacci/OC-projet2.git`  
`$ cd OC-projet2/`

Avec pipenv installer les modules du fichier requirements

`$ pipenv install -r requirements.txt`

Activer l'environnement virtuel
`$ pipenv shell`

> Le programme crée un dossier **scraping_files_exercices** 
> dans le répértoire courant.
> Les fichiers CSV de chaque catégorie y sont déposés.
> Un sous répértoire **images** au répértoire **scraping_files_exercices** 
> est créer pour stocker les images de tous les livres du site.
> Le nom du fichier de l'image correspond au titre du livre concerné.
>> **Attention le programme prend une dizaine de minutes pour scraper tout le site une fois lancé**

Pour lancer le programme
`$ python3 main.py`



