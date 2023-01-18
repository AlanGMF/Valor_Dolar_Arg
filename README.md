# Valor_Dolar_Arg

Collect every 20 minutes the values of the dollar in Argentina from different pages using FastAPI, Mongodb and Docker.

## Prerequisites
* Docker
* Git
* Python

## Get repository
```
git clone https://github.com/AlanGMF/Valor_Dolar_Arg.git
```
## Configs
You can change the container keys in the [docker-compose](https://github.com/AlanGMF/Valor_Dolar_Arg/blob/main/docker-compose.yml) file. Be sure to change them in the [.env](https://github.com/AlanGMF/Valor_Dolar_Arg/blob/main/app/.env) file as well.
## Run
  Start service on /Valor_Dolar_Arg:
  ```
  docker-compose up
  ```
  Stop service on /Valor_Dolar_Arg:
  ```
  docker-compose down
  ```
  
## Swagger Docs

  Access swagger docs by visiting:
  
  http://127.0.0.1:8000/docs
