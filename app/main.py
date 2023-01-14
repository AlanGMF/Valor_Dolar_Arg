from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

from .config import db

from .routers.cronista import cronista_router
from .routers.dolarhoy import dolarhoy_router
from .routers.root import root_router

from .scrapers.dolarhoy import dolarhoy_scraping
from .scrapers.cronista import cronista_scraping

app = FastAPI()
app.include_router(dolarhoy_router)
app.include_router(cronista_router)
app.include_router(root_router)

MINUTES_FOR_RERUN = 20


def compare_last_date(collection, data: dict) -> dict:
    """ gets the last values of the dollars loaded on the page

    :param collection: Mongo collection
    :type collection: pymongo.collection
    :param page: page name
    :type page: str
    :return: returns a dict with page
        as key and last values from collection as value
    :rtype: dict
    """

    try:
        last_documents_in_db = collection.find({}).sort(
            [('$natural', -1)]).limit(1)

        if len(list(last_documents_in_db)) <= 0:
            return False

        for document in last_documents_in_db:

            if (
                data["dólar libre"] and
                data["dólar libre"]["date"]
            ) is False and (
                    document["dólar libre"] and
                    document["dólar libre"]["date"]
            ) is False:

                return False

            if data["dólar libre"]["date"] != document["dólar libre"]["date"]:
                return False

            return True

    except Exception as e:
        print("Error: " + str(e))
        return False


@app.on_event("startup")
@repeat_every(seconds=60*MINUTES_FOR_RERUN, wait_first=False)
def save_dolarhoy_dollars_values() -> None:

    dolarhoy_dollars_data = dolarhoy_scraping()
    cronista_dollars_data = cronista_scraping()

    if compare_last_date(
                        db.db["dolarhoy"],
                        dolarhoy_dollars_data
                        ) is not True:
        db.db["dolarhoy"].insert_one(dolarhoy_dollars_data)

    if compare_last_date(
                        db.db["cronista"],
                        cronista_dollars_data
                    ) is not True:
        db.db["cronista"].insert_one(cronista_dollars_data)
