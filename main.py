
import csv
import os
import requests
from scrap_functions import scrap_book, scrap_categories, scrap_category_books
from constants import url_home, csv_columns


csv_files_directory = os.getcwd() + '/scraping_files_exercice/'
print(csv_files_directory)
csv_images_directory = os.path.join(csv_files_directory,'images/') 
print(csv_images_directory)

try:
    os.makedirs(csv_images_directory,exist_ok=True)
    
except OSError:
    print('Le dossier csv existe')

if __name__ == '__main__':

    for categorie in scrap_categories(url_home):

        csv_file = os.getcwd() + '/scraping_files_exercice/' + \
            categorie[0] + ".csv"

        with open(csv_file, 'w+') as csvfile:

            writer = csv.DictWriter(csvfile,delimiter=';', fieldnames=csv_columns)
            writer.writeheader()


            for book in scrap_category_books(categorie[1]):

                scrap = scrap_book(book)

                writer.writerow(scrap)

                myfile = requests.get(scrap['image_url'])
                myfile_name = scrap['title'].replace('#','').replace(',',' ').replace(':','-').replace('.',' ').replace('/','-')

                open(csv_images_directory+ myfile_name   +
                     '.png', 'wb').write(myfile.content)
                
                print(scrap['category'], scrap['title'])
