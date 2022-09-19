from fastapi import FastAPI
from fastapi import Path
from fastapi_utils.tasks import repeat_every

from enum import Enum
from config.db import client
import pymongo

from scrapers.infobae import infobae_scraping
from scrapers.dolarhoy import dolarhoy_scraping

app = FastAPI()


class Dolares(Enum):
    dolar_libre = "Dólar Libre"


def get_dolars(cursor, string = None):
    """
    """
    dolares = []
    for key in cursor:
        dolares.append(key["Dólar Libre"])

    return dolares


@repeat_every(seconds= 60*20 ,wait_first=False)
@app.on_event("startup")
def first_scraping():
    """
    Get the dollar value when the server starts and every twenty minutes
    """

    # Scraping Infobae
    db = client["dolares"]
    dolars_jsn = infobae_scraping()
    collec = db["infobae"]
    collec.insert_many(dolars_jsn)

    # Scraping Dolarhoy
    db = client["dolares"]
    dolar_jsn = dolarhoy_scraping()
    collec = db["dolarhoy"]
    collec.insert_many(dolar_jsn)


@app.get("/")
def home():

    # Consulta mongo
    db = client["dolares"]
    collec_inf = db["infobae"]  
    collec_dlrhoy = db["dolarhoy"] 

    dolares_inf =  collec_inf.find()
    dolares_dlrhoy =  collec_dlrhoy.find()
    
    dlres = get_dolars(dolares_dlrhoy,)

    return dlres


@app.get("/infobae")
def home():
    return {"infobae":"dolar"}

@app.get("/dolarhoy/dolar_blue") 
def home():
    
    db = client["dolares"]
    collec_dlrhoy = db["dolarhoy"] 

    dolares_dlrhoy =  collec_dlrhoy.find()
    dlres = get_dolars(dolares_dlrhoy)

    return dlres

#@app.get("/dolarhoy/{dolar}")
def dolarhoy_dolar(
    dolar : str = Path(...)
):
    db = client["dolares"]
    collec_dlrhoy = db["dolarhoy"] 

    cursor_dlrhoy =  collec_dlrhoy.find()
    dlres = get_dolars(cursor_dlrhoy,dolar)

    return dlres


