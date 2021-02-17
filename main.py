
import csv
import os
import requests


from scrap_functions import scrap_book, scrap_categories, scrap_category_books

url_home = 'http://books.toscrape.com/'

csv_files_directory = os.getcwd() + '/scraping_files_exercice/'
print(csv_files_directory)
csv_images_directory = os.path.join(csv_files_directory,'images/') 
print(csv_images_directory)

try:
    os.makedirs(csv_images_directory,exist_ok=True)
    
except OSError:
    print('Le dossier csv existe')



# flemme de réécrire les attributs des livres / récupérés avec une url de livre lambda
csv_columns = scrap_book(
    'http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html').keys()

if __name__ == '__main__':

    for categorie in scrap_categories(url_home):

        csv_file = os.getcwd() + '/scraping_files_exercice/' + \
            categorie[0] + ".csv"

        with open(csv_file, 'w+') as csvfile:

            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()

            for book in scrap_category_books(categorie[1]):

                writer.writerow(scrap_book(book))

                myfile = requests.get(scrap_book(book)['image_url'])
                myfile_name = scrap_book(book)['title']

                open(csv_images_directory+ myfile_name +
                     '.png', 'wb').write(myfile.content)
