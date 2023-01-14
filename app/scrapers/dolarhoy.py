import requests
from datetime import datetime
import logging

from lxml import html
from pathlib import Path

log_file = str(Path(__file__).parent.joinpath("logs_web_scraping.log"))

logging.basicConfig(
    level=logging.DEBUG,
    filename=log_file,
    filemode="a",
    format='%(asctime)s - %(levelname)s - %(filename)s -%(message)s',
    datefmt="%Y-%m-%dT%H:%M:%S%z"
)


def dolarhoy_scraping() -> list[dict]:
    """ Get the dollar values on the page

    :return: list with a json that contains the values of purchase,
            sale and date of each dollar
    :rtype: list[dict]
    """

    url = "https://dolarhoy.com/cotizacion-dolar-blue"
    xpath = r"""//div[@class="tile is-child"]
                /a[contains(@href,"dolar")]/div/text()"""

    # Request url
    try:
        response = requests.get(url)
    except Exception as e:
        logging.error("Error with Dol" + "arhoy url: " + str(e))
        return None

    try:
        response = response.content.decode("utf-8")
        parser = html.fromstring(response)
    except Exception as e:
        logging.error("Error procecing dol" + "arhoy response" + str(e))
        return None

    # Get date
    try:
        date = parser.xpath("//div[@class='tile is-child']/span/text()")[0]
    except Exception as e:
        print("Can not get date from html")
        logging.error("Can not get date from html: " + str(e))
        date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    try:
        # Get name, parchase value, sele value
        dollar_values_list = parser.xpath(xpath)
        logging.info(f"Extracted values: {len(dollar_values_list)}")

        # Structure the data
        list_jsn = []
        jsn = {}

        for position_number in range(0, len(dollar_values_list), 3):

            # Save the values in the json

            if "naci" in dollar_values_list[position_number].lower():
                dollar_name = "dólar oficial"
            elif "liq" in dollar_values_list[position_number].lower():
                dollar_name = "dólar ccl"
            else:
                dollar_name = dollar_values_list[position_number].lower()

            jsn[dollar_name] = {
                "compra": dollar_values_list[position_number+1],
                "venta": dollar_values_list[position_number+2],
                "date": date
            }
        logging.info("Data was successfully structured")
    except Exception as e:
        logging.error("Error getting data from html: " + str(e))
        return None

    # Put the json in a list to be able to save it in mongodb
    list_jsn.append(jsn)
    return jsn
