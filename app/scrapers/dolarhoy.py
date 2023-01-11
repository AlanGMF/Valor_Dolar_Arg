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


def dolarhoy_scraping() -> list[dict] | None:
    """ Get the dollar values on the page

    :return: list with a json that contains the values of purchase,
            sale and date of each dollar
    :rtype: list[dict]
    """

    url = "https://dola" + "rhoy.com/cotizacion-do" + "lar-blue"
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

    date_now = datetime.now()
    date = date_now.strftime("%d/%m/%Y %H:%M:%S")

    # Collect data
    dollar_values_list = parser.xpath(xpath)
    logging.info(f"Extracted values: {len(dollar_values_list)}")

    # Structure the data
    list_jsn = []
    jsn = {}

    try:

        for position_number in range(0, len(dollar_values_list), 3):

            # Save the values in the json
            jsn[dollar_values_list[position_number]] = {
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
    return list_jsn
