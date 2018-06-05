from src import chess
from bs4 import BeautifulSoup

def assert_eq(actual, expected):
    assert actual == expected, f"\n*Expected:\n{expected}\n*Actual:\n{actual}"

def read_file(file_name):
    with open(f"./tests/{file_name}", 'r') as f:
        return f.read()

def test_get_opening_links():
    test_content = read_file('homepage.html')
    sut = chess.Parser()

    a = sut.get_opening_parameters(test_content)

def test_single_search_request():
    # arrange
    parser = chess.Parser()
    test_content = read_file('homepage.html')
    a = parser.get_opening_parameters(test_content)
    k = list(a.keys())[0]
    opening_search_term = a[k]

    sut = chess.ChessScraper()
    
    # act
    sut.search_for_opening(opening_search_term)

def test_get_game_links_from_opening_page():
    test_content = read_file('openings_list.html')
    sut = chess.Parser()

    sut.get_list_of_games(test_content)

def test_visit_game():
    test_content = read_file('openings_list.html')
    game_links = chess.Parser().get_list_of_games(test_content)

    sut = chess.ChessScraper()
    print(game_links[0].link)
    sut.visit_game(game_links[0].link)

def test_parse_game():
    test_content = read_file('game.html')
    sut = chess.Parser()
    actual = sut.get_game_contents(test_content)
    print('hi')
    assert False