
from bs4 import BeautifulSoup
from core.aesthetix import ConsoleColored
from requests_html import HTMLSession

def get_soup(url):
    fancy_url = ConsoleColored(url, "yellow", bold=1, underlined=1)
    message = "HTTP GET request to URL: {} ...".format(fancy_url)
    print(message)
    del message
    
    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=1)
    print("creating soup...")
    soup = BeautifulSoup(response.html.html, "html.parser")
    print(ConsoleColored("soup created successfully.", "yellow", bold=1))
    return soup