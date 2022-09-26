
# Python
from typing import Optional

from fastapi import FastAPI
from fastapi import Path
from fastapi_utils.tasks import repeat_every

from enum import Enum
from config.db import client
import pymongo

from scrapers.infobae import infobae_scrap
from scrapers.dolarhoy import dolarhoy_scrap

app = FastAPI()

# Mongo
db = client["dolares"]
collection_dolarhoy = db["dolarhoy"]
collection_infobae = db["infobae"]

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

#@repeat_every(seconds= 60*20 ,wait_first=False)
#@app.on_event("startup")
def first_scraping():


    # Scraping Infobae
    db = client["dolares"]
    dolars_jsn = infobae_scrap()
    collec = db["infobae"]
    collec.insert_many(dolars_jsn)

    # Dolarhoy
    db = client["dolares"]
    dolar_jsn = dolarhoy_scrap()
    collec = db["dolarhoy"]
    collec.insert_many(dolar_jsn)

    return 0


@app.get("/") # dolares ultima cotizacion infobae y dolarhoy
def home():
    
    response_ = []
    for documento in  collection_dolarhoy.find({}).limit(1).sort([('$natural',-1)]):
        d = documento["Dólar Libre"]
        d["Pagina"] = "Dolarhoy"
        response_.append(d)
        
    for documento in  collection_infobae.find({}).limit(1).sort([('$natural',-1)]):
        d = documento["Dólar Libre"]
        d["Pagina"] = "Infobae"
        response_.append(d)

    return response_

@app.get("/infobae/{dolar}")
def dolarhoy_dolar(
    dolar : Dolares_infobae = Path(
        ...,
        title = "Name of dollars to get",
    ),
):
    dolar_=dicconario[dolar]

    response_ = []
    for documento in  collection_infobae.find({}):
        response_.append(documento[dolar_])
        
    return response_

@app.get("/infobae/{dolar}/{amount}")
def ss(
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
    dolar_=dicconario[dolar]

    response_ = []
    for documento in  collection_infobae.find({}).limit(amount):
        response_.append(documento[dolar_])

    return response_

@app.get("/dolarhoy/{dolar}")
def dolarhoy_dolar(
    dolar : Dolares_dolarhoy = Path(
        ...,
        title = "Name of dollars to get",
    ),
):

    dolar_=dicconario[dolar]
    response_ = []
    for documento in  collection_dolarhoy.find({}):
        response_.append(documento[dolar_])
        
    return response_

@app.get("/dolarhoy/{dolar}/{amount}")
def sss(
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

    dolar_=dicconario[dolar]

    response_ = []    
    for documento in  collection_dolarhoy.find({}).limit(amount):
        response_.append(documento[dolar_])

    return response_


