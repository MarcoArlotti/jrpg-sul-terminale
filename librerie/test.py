import json


with open("json_data\lista_giocatori.json","r") as lista_json:
    lista_giocatori = json.load(lista_json)
for giocatore in lista_giocatori:
    magie = giocatore["magie"]
    for magia in magie:
        magia.update({"cosa_consuma":"sp",})

with open("json_data\lista_giocatori.json","w") as lista_json:
    json.dump(lista_giocatori,lista_json,indent=4)