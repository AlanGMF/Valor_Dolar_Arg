from enum import Enum
from ..config import db
from fastapi import Path, Query
from fastapi import APIRouter
from .constans import PATH_STR_DOLLARS

cronista_router = APIRouter()


class Cronista_dollars(str, Enum):
    dolar_oficial = "dolar_oficial"
    dolar_libre = "dolar_libre"
    dolar_turista = "dolar_turista"
    dolar_mayorista = "dolar_mayorista"
    dolar_ccl = "dolar_ccl"
    dolar_mep = "dolar_mep"


@cronista_router.get("/cronista/{dolar}/")
def cronista_dollar_amount(
    dolar: Cronista_dollars = Path(
        ...,
        title="Name of dollars to get",
    ),
    amount: int = Query(
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
    collection = db.db["cronista"]
    response_ = []

    for documento in collection.find({}).limit(
                amount).sort([('$natural', -1)]):
        response_.append(documento[PATH_STR_DOLLARS[dolar]])

    return response_


@cronista_router.get("/cronista/{dolar}")
def cronista_dollar(
    dolar: Cronista_dollars = Path(
        ...,
        title="Name of dollars to get",
    ),
):
    """
    Return, according to the specified amount,
    the values of the required dollar values collected from dolarhoy.com
    """
    collection = db.db["cronista"]
    response_ = []

    for documento in collection.find({}).limit(1).sort([('$natural', -1)]):
        response_.append(documento[PATH_STR_DOLLARS[dolar]])

    return response_
