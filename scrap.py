import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de base
base_url = "https://quotes.toscrape.com/page/{}/"

# Tags à filtrer
desired_tags = {"love", "inspirational", "life", "humor"}

# Liste pour stocker les citations filtrées
filtered_quotes = []

# Fonction pour récupérer et filtrer les citations d'une page donnée
def get_quotes_from_page(page_number):
    url = base_url.format(page_number)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Trouver toutes les citations sur la page
    quotes = soup.find_all("div", class_="quote")
    
    for quote in quotes:
        text = quote.find("span", class_="text").get_text()
        author = quote.find("small", class_="author").get_text()
        tags = {tag.get_text() for tag in quote.find_all("a", class_="tag")}
        
        # Vérifier si l'une des tags désirées est présente
        if desired_tags.intersection(tags):
            filtered_quotes.append({"text": text, "author": author, "tags": ", ".join(tags)})

# Récupérer les citations des cinq premières pages
for page in range(1, 6):
    get_quotes_from_page(page)
