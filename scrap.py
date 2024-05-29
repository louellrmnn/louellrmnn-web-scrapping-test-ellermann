import requests
from bs4 import BeautifulSoup
import csv

# Constantes pour les URLs
BASE_URL = "https://quotes.toscrape.com"
LOGIN_URL = f"{BASE_URL}/login"

# Informations d'authentification
LOGIN_DATA = {
    'username': 'test',
    'password': 'test'
}

# Tags cibles pour les citations
TARGET_TAGS = {"love", "inspirational", "life", "humor", "books"}

def login_and_get_session():
    """Effectue l'authentification et retourne la session"""
    session = requests.Session()
    response = session.get(LOGIN_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('input', {'name': 'csrf_token'})['value']
    LOGIN_DATA['csrf_token'] = csrf_token
    response = session.post(LOGIN_URL, data=LOGIN_DATA)
    if response.status_code != 200:
        return None
    return session

def extract_quotes(page_num, session):
    """Extrait les citations de la page spécifiée"""
    url = f"{BASE_URL}/page/{page_num}/"
    response = session.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.find_all("div", class_="quote")
    filtered_quotes = []
    for quote in quotes:
        tags = {tag.text for tag in quote.find_all("a", class_="tag")}
        if TARGET_TAGS.intersection(tags) or (page_num <= 2 and "books" in tags):
            text = quote.find("span", class_="text").text
            filtered_quotes.append({"text": text, "tags": ", ".join(tags)})
    return filtered_quotes

def scrape_quotes(session, pages=5):
    """Récupère les citations des premières pages spécifiées"""
    all_quotes = []
    for page_num in range(1, pages + 1):
        quotes = extract_quotes(page_num, session)
        all_quotes.extend(quotes)
    return all_quotes

def save_quotes_to_csv(quotes, token, filename="results.csv"):
    """Sauvegarde les citations dans un fichier CSV"""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Token", token])  # Écrire le token
        writer.writerow(["Citation", "Tags"])  # Écrire l'en-tête
        for quote in quotes:
            writer.writerow([quote['text'], quote['tags']])

if __name__ == "__main__":
    session = login_and_get_session()
    if session:
        quotes = scrape_quotes(session)
        token = session.cookies.get_dict().get('session', None)
        if token:
            save_quotes_to_csv(quotes, token)
            print("Tout a été sauvegardé dans le fichier results.csv.")
        else:
            print("Impossible de récupérer le token.")
    else:
        print("Impossible de se connecter.")
