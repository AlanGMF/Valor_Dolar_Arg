
# Python
from typing import Optional

from fastapi import FastAPI
from fastapi import Path
from fastapi_utils.tasks import repeat_every

from enum import Enum
from .config.db import *


from .scrapers.infobae import infobae_scraping
from .scrapers.dolarhoy import dolarhoy_scraping

app = FastAPI()

dicconario = {
    "dolar_libre" : "Dólar Libre",
    "dolar_targeta" : "Dólar tarjeta",
    "dolar_mep" : "Dólar MEP",
    "ccl" : "Contado con liqui",
    "banco_nacion" : "Dólar Banco Nación",
    "riesgo_pais" : "Riesgo País",
    "dolar_mayorista" : "Dólar Mayorista",
    "dolar_bolsa" : "Dólar Bolsa",
    "banco_nacion" : "Banco Nación",
}


class Dolares_dolarhoy(str, Enum):
    dolar_libre = "dolar_libre"
    dolar_mayorista = "dolar_mayorista"
    dolar_bolsa = "dolar_bolsa"
    ccl = "ccl"
    banco_nacion = "banco_nacion"

class Dolares_infobae(str, Enum):
    dolar_libre = "dolar_libre"
    dolar_targeta = "dolar_targeta"
    dolar_mep = "dolar_mep"
    ccl = "ccl"
    banco_nacion = "banco_nacion"
    riesgo_pais = "riesgo_pais"


@app.on_event("startup")
@repeat_every(seconds= 60*20 ,wait_first=False)
def save_infobae_dollars_values():

    # Scraping Infobae
    #db = client["dolares"]
    list_of_dollars = infobae_scraping()
    #collec = db["infobae"]
    collection_infobae.insert_many(list_of_dollars)

    return 0

@app.on_event("startup")
@repeat_every(seconds= 60*20 ,wait_first=False)
def save_dolarhoy_dollars_values():

    # Dolarhoy
    #db = client["dolares"]
    list_of_dollars = dolarhoy_scraping()
    #collecc = db["dolarhoy"]
    collection_dolarhoy.insert_many(list_of_dollars)

    return 0


def get_last_dolar_libre_value(collection, pagina: str, lis: list):
    """
    takes the last document in the collection, adds the "Page" element 
    and returns the list adding this document in the last position.
    """

    for documento in  collection.find({}).limit(1).sort([('$natural',-1)]):

        d = documento[dicconario["dolar_libre"]]
        d["Pagina"] = pagina
        lis.append(d)

    return lis

@app.get("/")
def lastest_values():
    """
    Return the latest free dollar values that pages have
    """
    info = "infobae"
    dolarhoy = "dolarhoy"
    response_ = []
    
    response_ = get_last_dolar_libre_value(
                                            collection_dolarhoy, 
                                            dolarhoy, 
                                            response_
                                            )

    response_ = get_last_dolar_libre_value(
                                            collection_infobae,
                                            info,
                                            response_
                                            )

    return response_


@app.get("/infobae/{dolar}")
def infobae_dolar(
    dolar : Dolares_infobae = Path(
        ...,
        title = "Name of dollars to get",
    ),
):
    """
    Shows all values of the specified dollar collected from infobae.com
    """   
    dolar_=dicconario[dolar]
    response_ = []
    for documento in  collection_infobae.find({}).sort([('$natural',-1)]):
        response_.append(documento[dolar_])

    return response_

@app.get("/infobae/{dolar}/{amount}")
def infobae_dolar_amount(
    dolar : Dolares_infobae = Path(
        ...,
        title = "Name of dollars to get",
    ),
    amount : Optional[int] = Path(
        ...,
        gt=0,
        le=101,
        title="Amounts of values of dollars to get",
        description="Integers between zero and hundred"
    )  
):
    """
    Return, according to the specified amount,
    the values of the required dollar values collected from infobae.com
    """

    dolar_= dicconario[dolar]
    response_ = []

    for documento in  collection_infobae.find({}).limit(amount).sort([('$natural',-1)]):
        response_.append(documento[dolar_])

    return response_

@app.get("/dolarhoy/{dolar}")
def dolarhoy_dolar(
    dolar : Dolares_dolarhoy = Path(
        ...,
        title = "Name of dollars to get",
    ),
):
    """
    Shows all values of the specified dollar collected from dolarhoy.com
    """
    dolar_= dicconario[dolar]
    response_ = []
    for documento in  collection_dolarhoy.find({}).sort([('$natural',-1)]):
        response_.append(documento[dolar_])
        
    return response_

@app.get("/dolarhoy/{dolar}/{amount}")
def dolarhoy_dolar_amount(
    dolar : Dolares_dolarhoy = Path(
        ...,
        title = "Name of dollars to get",
        
    ),
    amount : Optional[int] = Path(
        ...,
        gt=0,
        le=101,
        title="Amounts of values of dollars to get",
        description="Integers between zero and hundred"
    )  
):  
    """
    Return, according to the specified amount,
    the values of the required dollar values collected from dolarhoy.com
    """
    dolar_= dicconario[dolar]
    response_ = []    
    for documento in  collection_dolarhoy.find({}).limit(amount).sort([('$natural',-1)]):
        response_.append(documento[dolar_])

    return response_


