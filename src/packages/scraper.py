import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url):
        self.url = url

    def returnPlayers(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find('p', {'class': 'text-lead font-caption-body wait-for-i18n-format-render'})
        players = element.text.strip()

        return players.replace(',', '')
