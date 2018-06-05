from src.async_client import AsyncHttpClient
from bs4 import BeautifulSoup
import re

from collections import namedtuple

urls = {
    'base': 'http://www.chessgames.com',
    'homepage': '',
    'search': '/perl/chess.pl'
}


def write_file(data):
    with open('game.html', 'w') as the_file:
        the_file.write(data)


class ChessScraper():
    def __init__(self, workers=1, threads=1):
        self.http_client = AsyncHttpClient(
            urls['base'], workers, threads)

    def visit_home_page(self):
        data = self.http_client.get(urls['homepage']).result().text

        return data

    def search_for_opening(self, search_term):
        data = self.http_client.get(urls['search'], {
            'opening': search_term
        }).result().text

        return data

    def visit_game(self, path):
        data = self.http_client.get(path).result().text
        return data


class Parser():
    def __init__(self):
        pass

    def get_opening_parameters(self, data):
        soup = BeautifulSoup(data, "html.parser")
        opening = [el for el in soup.find_all(
            'select') if el['name'] == 'opening'][0]
        params = {}
        for option in opening.find_all('option'):
            if option['value']:
                name_of_opening = re.sub('\s*-\s*', '', option.next).strip()
                search_term_for_opening = re.sub(
                    '\s', '+', option['value'].strip())
                params[name_of_opening] = search_term_for_opening

        return params

    def get_list_of_games(self, data):
        GameLink = namedtuple('GameLink', 'link white black')

        soup = BeautifulSoup(data, "html.parser")
        links = []
        for el in soup.find_all('a'):
            if el['href'].startswith('/perl/chessgame'):
                white, black = el.next.split(' vs ')
                link = el['href']
                links.append(GameLink(link, white, black))

        return links

    def get_game_contents(self, data):
        soup = BeautifulSoup(data, "html.parser")
        contents = soup.find("div", {"id": "olga-data"})

        # Metadata
        game_attrs = re.findall('\[([^\[\]]*)\]', contents['pgn'])
        for attr_pair in game_attrs:
            m = re.search('(\w+)\s*\"(.*)\"', attr_pair)
            if m:
                key, value = m[1], m[2]
            else:
                # TODO log failure
                pass

        # Moves
        moves = re.findall('1\.\s.*[0\-1|1\-0]', contents['pgn'])
        # TODO parse the moves
        print(moves)
