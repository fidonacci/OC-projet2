""" This module encompasses all the functions needed to scrap the books website """

import requests
from bs4 import BeautifulSoup
import re
from constants.constants import url_home

# définitions
categories_list = []
book = {}

# détermination des informations d'une page d'un livre
# ---------------------------------------------------------
def scrap_book(url):
    
    """Return a dict with book informations.
    Keyword arguments:
    url -- the book page url (no default)
    """

    if requests.get(url).ok:
        response = requests.get(url)
        page_book = BeautifulSoup(response.text, 'lxml')
        book["universal_product_code"] = page_book.table.find_all(
            'tr')[0].td.text.encode('utf-8').decode('ascii', 'ignore')
        book["title"] = page_book.h1.text.encode(
            'utf-8').decode('ascii', 'ignore')
        book["price_including_tax"] = page_book.table.find_all(
            'tr')[3].td.text.encode('utf-8').decode('ascii', 'ignore')
        book["price_excluding_tax"] = page_book.table.find_all(
            'tr')[2].td.text.encode('utf-8').decode('ascii', 'ignore')
        book["number_available"] = int(re.findall(
            '[0-9]+', str(page_book.table.find_all('tr')[5]))[0])
        book["product_description"] = page_book.find_all(
            'p')[3].text.encode('utf-8').decode('ascii', 'ignore')
        book["category"] = page_book.find(class_='breadcrumb').find_all(
            'a')[2].text.encode('utf-8').decode('ascii', 'ignore')
        book["review_rating"] = " ".join(page_book.find_all('p')[2]['class'])
        book["image_url"] = "http://books.toscrape.com/"+page_book.find_all(
            'img')[0]['src'].strip('../../').encode('utf-8').decode('ascii', 'ignore')

    return book

# détermination des catégories existantes / renvoie une liste
# ---------------------------------------------------------


def scrap_categories(url):
    """Return a list of lists formed as [category name, category url].
    Keyword arguments:
    url -- the site home page url (no default)
    """

    if requests.get(url).ok:
        response = requests.get(url)
        page_accueil = BeautifulSoup(response.text, 'lxml')
        # récupération des noms et liens de catégories dans un tableau de tableau [nom catégorie, url catégorie]
        # suppression du premier "li" qui concerne "Books" qui n'est pas une catégorie
        categories = page_accueil.find(class_='nav nav-list').find_all('a')
        categories.pop(0)
        for a in categories:
            categories_list.append([a.text.strip(), url+a['href']])

    return categories_list

# renvoie un tableau de l'ensemble des urls des livres de toutes les pages de la catégorie
# url pris en entrée est l'url "home" de la catégorie
# ---------------------------------------------------------


def scrap_category_books(url):
    """Return a list of books urls of the whole category.
    Keyword arguments:
    url -- the category home page url (no default)
    """

    category_books = []

    if requests.get(url).ok:
        response = requests.get(url)
        category_home = BeautifulSoup(response.text, 'lxml')

    # s'il n'y pas de bouton next on s'arrête à la page home, sinon on parcourt les url de toutes les catégories
    if category_home.find(class_='next') == None:

        category_books = scrap_page_books(url)
        return category_books

    else:
        j = 1
        category_page_url = url.rstrip('/index.html')+f'/page-{j}.html'

        while requests.get(category_page_url).status_code == 200:

            category_books.extend(scrap_page_books(category_page_url))
            j += 1
            category_page_url = url.rstrip('/index.html')+f'/page-{j}.html'

        return category_books

# fonction qui detrmine les blocs de page / renvoie un tableau de url des livres affichés / page en argument est une url
# ---------------------------------------------------------


def scrap_page_books(url):
    """Return a list of books urls of the specific category page.
    Keyword arguments:
    url -- the category page url (no default)
    """
    if requests.get(url).ok:
        response = requests.get(url)
        page = BeautifulSoup(response.text, 'lxml')

    page_books = page.find_all(class_='col-xs-6 col-sm-4 col-md-3 col-lg-3')
    url_table = []

    for p in page_books:
        url_table.append(url_home + 'catalogue/' +
                         p.h3.a['href'].strip('../../../'))
    return url_table
