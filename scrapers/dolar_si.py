import requests

url = "https://www.dolarsi.com/api/api.php?type=valoresprincipales"
api = requests.get(url=url).json()

db = client["dolares"]
collec = db["dolar"]  
collec.insert_many(api)
#x = collec.find({"nombre":"Dolar Blue"})