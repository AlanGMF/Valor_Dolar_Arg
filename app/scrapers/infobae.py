
from datetime import datetime
import requests

def infobae_scraping() -> list[dict]:
    
    url = "https://www.infobae.com/pf/api/v3/content/fetch/exchange-feed?query=%7B%7D&d=1069&_website=infobae"
    dictionary = {}
    elements_list = []

    response_dictionary = requests.get(url).json()
    dollar_dictionaries = response_dictionary["items"]
    
    date_now = datetime.now()
    date = date_now.strftime("%d/%m/%Y %H:%M:%S")

    for dollar in dollar_dictionaries:
        
        dictionary[dollar["currency"]] = {
            "compra" : str(dollar["unico"]),
            "venta" : "-",
            "date" : date
        }

        elements_list.append(dictionary)

    return elements_list  