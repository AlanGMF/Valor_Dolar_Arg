from ..config import db
from fastapi import APIRouter

root_router = APIRouter()


def get_last_page_values(collection, page: str) -> dict:
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
        for documento in collection.find({}).limit(1).sort([('$natural', -1)]):

            del documento['_id']
            jsn = {
                page: documento
            }

            return jsn
    except Exception as e:
        print("Error: " + str(e))
        print(":________________utils root_______________none ")
        return None


@root_router.get("/")
def lastest_values():
    """
    Return the latest free dollar values that pages have
    """
    cronista = "cronista"
    dolarhoy = "dolarhoy"
    response_ = []

    response_.append(get_last_page_values(db.db[dolarhoy], dolarhoy))
    response_.append(get_last_page_values(db.db[cronista], cronista))

    return response_
