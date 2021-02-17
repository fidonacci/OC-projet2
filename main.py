""" This module is the main module from which the program is lanched """

import csv
import os
import requests
from scrap_functions import scrap_book, scrap_categories, scrap_category_books
from constants import url_home, csv_columns
import time


csv_files_directory = os.getcwd() + '/scraping_files_exercice/'
print(csv_files_directory)
csv_images_directory = os.path.join(csv_files_directory, 'images/')
print(csv_images_directory)

try:
    os.makedirs(csv_images_directory, exist_ok=True)

except OSError:
    print('Le dossier csv existe')

if __name__ == '__main__':

    tic = time.perf_counter()
    scraped_categories = scrap_categories(url_home)
    toc = time.perf_counter()
    print(f"scraped_categories in {toc - tic:0.4f} seconds")

    for categorie in scraped_categories:

        csv_file = os.getcwd() + '/scraping_files_exercice/' + \
            categorie[0] + ".csv"

        with open(csv_file, 'w+') as csvfile:

            writer = csv.DictWriter(
                csvfile, delimiter=';', fieldnames=csv_columns)
            writer.writeheader()

            tic = time.perf_counter()
            scraped_category_books = scrap_category_books(categorie[1])
            toc = time.perf_counter()
            print(f"scraped_category_books of {categorie[1]} in {toc - tic:0.4f} seconds")

            for book in scraped_category_books:
                
                tic = time.perf_counter()
                scraped_book = scrap_book(book)
                toc = time.perf_counter()
                print(f"scraped_book of {scraped_book['title']} in {toc - tic:0.4f} seconds")

                tic = time.perf_counter()
                writer.writerow(scraped_book)
                toc = time.perf_counter()
                print(f"Adding one line to CSV in {toc - tic:0.4f} seconds")

                tic = time.perf_counter()
                myfile = requests.get(scraped_book['image_url'])
                myfile_name = scraped_book['title'].replace('#', '').replace(
                    ',', ' ').replace(':', '-').replace('.', ' ').replace('/', '-')

                open(csv_images_directory + myfile_name +
                     '.png', 'wb').write(myfile.content)
                
                toc = time.perf_counter()
                print(f"Downloading image of {scraped_book['title']} in {toc - tic:0.4f} seconds")

                print(scraped_book['category'], scraped_book['title'])
