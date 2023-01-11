from datetime import datetime
import requests
from lxml import html

import logging
from pathlib import Path

log_file = str(Path(__file__).parent.joinpath("logs_web_scraping.log"))

logging.basicConfig(
    level=logging.DEBUG,
    filename=log_file,
    filemode="a",
    format='%(asctime)s - %(levelname)s - %(filename)s -%(message)s',
    datefmt="%Y-%m-%dT%H:%M:%S%z"
)

def cronista_scraping() -> list[dict] | None:
    """ Get the dollar values on the page

    :return: list with a json that contains the values of purchase,
            sale and date of each dollar
    :rtype: list[dict]
    """

    url = "https://www.cr" + "onista.com/MercadosOnline/dolar.html"

    # Request url
    try:
        response = requests.get(url)
    except Exception as e:
        logging.error("Error with Cro" + "nista url: " + str(e))
        return None
    
    try:
        parser = html.fromstring(response.content)
    except Exception as e:
        logging.error("Error procecing Cro" + "nista response" + str(e))
        return None

    # Get data from html
    dollar_name_list = parser.xpath(
        '//tr//td[@class="name"]/a/text()'
        )
    logging.info(f"Extracted dollar names: {len(dollar_name_list)}")
    dollar_buy_list = parser.xpath(
        '//tr//td[@class="buy"]/a//div[@class="buy-value"]/text()'
        )
    logging.info(f"Purchase prices of dollars extracted: {len(dollar_buy_list)}")
    dollar_sell_list = parser.xpath(
        '//tr//td[@class="sell"]/a//div[@class="sell-value"]/text()'
        )
    logging.info(f"Sell prices of dollars extracted: {len(dollar_sell_list)}")
    dollar_date_list = parser.xpath(
        '//tr//td[@class="date"]/a/text()'
        )
    logging.info(f"Extracted update dates: {len(dollar_date_list)}")
    
    # Structure the data
    list_jsn = []
    jsn = {}

    try:
        for position in range(len(dollar_name_list)):
            
            if dollar_name_list[position] == "DÓLAR TURISTA":

                jsn[dollar_name_list[position]] = {
                    "venta": dollar_sell_list[position],
                    "date": dollar_date_list[position],
                }

                # A number is added in the position to balance
                # the length of the lists, due to the fact that
                # "tourist dollar" is the only dollar that
                #  does not have a purchase price 
                dollar_buy_list.insert(0,position)

            else:
                jsn[dollar_name_list[position]] = {
                        "compra": dollar_buy_list[position],
                        "venta": dollar_sell_list[position],
                        "date": dollar_date_list[position],
                    }
        logging.info("Data was successfully structured")
    except Exception as e:
        logging.error("Error structuring data: " + str(e))
        return None
    
    list_jsn.append(jsn)

    return list_jsn
