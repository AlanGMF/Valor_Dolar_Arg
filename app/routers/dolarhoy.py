from enum import Enum
from ..config import db
from fastapi import Path, Query
from fastapi import APIRouter
from .constans import PATH_STR_DOLLARS

dolarhoy_router = APIRouter()


class Dolarhoy_dollars(str, Enum):
    dolar_oficial = "dolar_oficial"
    dolar_libre = "dolar_libre"
    dolar_mayorista = "dolar_mayorista"
    dolar_bolsa = "dolar_bolsa"
    dolar_ccl = "dolar_ccl"


@dolarhoy_router.get("/dolarhoy/{dolar}/")
def dolarhoy_dollar_amount(
    dolar: Dolarhoy_dollars = Path(
        ...,
        title="Name of dollars to get",
    ),
    amount: int = Query(
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
    collection = db.db["dolarhoy"]
    response_ = []

    for documento in collection.find({}).limit(
                amount).sort([('$natural', -1)]):
        response_.append(documento[PATH_STR_DOLLARS[dolar]])

    return response_


@dolarhoy_router.get("/dolarhoy/{dolar}")
def dolarhoy_dollar(
    dolar: Dolarhoy_dollars = Path(
        ...,
        title="Name of dollars to get",
    ),
):
    """
    Return, according to the specified amount,
    the values of the required dollar values collected from dolarhoy.com
    """
    collection = db.db["dolarhoy"]
    response_ = []

    for documento in collection.find({}).limit(1).sort([('$natural', -1)]):
        response_.append(documento[PATH_STR_DOLLARS[dolar]])

    return response_
