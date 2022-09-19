from datetime import datetime
from .base import base_scraping

def infobae_scraping():
    url = "https://www.infobae.com/economia/divisas/dolar-hoy/"
    xpath = '//div[@class="excbar"]//a/p/text()'

    dolars_list = base_scraping(url, xpath)

    date_now = datetime.now()
    date = date_now.strftime("%d/%m/%Y %H:%M:%S")

    list_jsn=[]
    jsn = {}

    for p in range(0,len(dolars_list),2):
        jsn[dolars_list[p]] = {
            "compra" : dolars_list[p+1],
            "venta" : '-',
            "date" : date
        }
        
    list_jsn.append(jsn)

    return list_jsn
