from datetime import datetime
from .base import base_scraping

def dolarhoy_scraping():
    url = "https://dolarhoy.com/cotizacion-dolar-blue"
    xpath = '//div[@class="tile is-child"]/a[contains(@href,"dolar")]/div/text()'

    dolars_list = base_scraping(url, xpath)

    date_now = datetime.now()
    date = date_now.strftime("%d/%m/%Y %H:%M:%S")

    list_jsn=[]
    jsn = {}

    for p in range(0,len(dolars_list),3):
        jsn[dolars_list[p]] = {
            "compra" : dolars_list[p+1],
            "venta" : dolars_list[p+2],
            "date" : date
        }

    list_jsn.append(jsn)

    return list_jsn