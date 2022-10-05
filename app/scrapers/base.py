import requests
from lxml import html

def base_scraping(url: str, xpath:str) -> list:

    response = requests.get(url)
    response = response.content.decode("utf-8")
    parser = html.fromstring(response)
    dolars_list = parser.xpath(xpath)
    
    return dolars_list