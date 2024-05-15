import json

#"json_data\lista_giocatori.json"
#"json_data\magie.json"
with open("json_data\enemy_stats_dungeon_1.json","r") as lista_json:
    lista_nemici = json.load(lista_json)
for nemico in lista_nemici:
    lista=[
        {
            "ATK":0
        },
        {
            "DEF":0
        },
        {
            "AGI":0
        }
    ]
    lista_s=[
        {
            "s_ATK":0
        },
        {
            "s_DEF":0
        },
        {
            "s_AGI":0
        }
    ]
    nemico.update({"effetti":lista})
    nemico.update({"scadenze":lista_s})
with open("json_data\enemy_stats_dungeon_1.json","w") as lista_json:
    json.dump(lista_nemici,lista_json,indent=4)
#
#

#    "effetti":{
#            "DEF":0,
#            "ATK":0,
#            "AGI":0
#            },
#    
#
#    "scadenze":{
#            "s_DEF":0
#            ,
#            "s_ATK":0,
#            "s_AGI":0
#        }