import json
import os
import random
from termcolor import colored
from combattimento import attaccare,difendersi,fuoco,curarsi,AI_nemico,aspetta_input
#os.system("cls")
#python -> json = .dump
#json -> python = .load
def inizio_run(): #tutte le stat sono portare a 0
    #dichiarazione delle statistiche basi
    numero_piano = 1
    melee = {
        "damage":int(32),
        "price":0,
        "type":None
    }
    lista_player = [
        {
            "name":"Galo",
            "max_health":240,
            "health":int(130),
            "speed":float(19),
            "exp":0.00,
            "sp":int(26),
            "damage_base":float(10),
            "current_equip_melee":melee,
            "guard":False
        }
        ,{
            "name":"Caso",
            "max_health":220,
            "health":int(210),
            "speed":float(23),
            "exp":0.00,
            "sp":int(22),
            "damage_base":float(9),
            "current_equip_melee":melee,
            "guard":False
        }
    ]
    

    with open("json_data/lista_giocatori.json","w") as file_json: #creazione del json player_stats
        json.dump(lista_player, file_json, indent=4)
    return numero_piano


#def dichiara_enemy(): #trasporta una lista con tutti i tipi di nemici e li converte in un json (list-->.json)
#    
#    shadow = {
#    "name":"SHADOW", 
#    "health":110,                        
#    "speed":15.00,
#    "type":"ice",
#    "dungeon":1,
#    "exp_drop":3
#    }
#    flying_shadow = {
#        "name":"FLYING SHADOW",
#        "health":76,
#        "speed":37.00,
#        "type":"air",
#        "dungeon":1,
#        "exp_drop":2.3
#    }
#
#    nemici = [shadow,flying_shadow]
#    with open("json_data/enemy_stats_dungeon_1.json","w") as file_json:
#        json.dump(nemici,file_json,indent=4)


def scelta_percentuali(numero_piano):

    lista_nemici = []
    flip = ["1","2","3"]

    if numero_piano < 5: #il livello dei nemici fa variare la quantità che appareranno #GLOBAL_LEVEL
        
        quanti_nemici = random.choices(flip,weights=[20,40,15],k=1)

        lista_nemici = random_quanti_nemici(quanti_nemici,lista_nemici)
        
    elif numero_piano < 15 and numero_piano >= 5:

        quanti_nemici = random.choices(flip,weights=[15,50,40],k=1)
        lista_nemici = random_quanti_nemici(quanti_nemici,lista_nemici)
    

    
    return lista_nemici


def random_quanti_nemici(quanti_nemici,lista_nemici):

    if quanti_nemici == ["1"]: # tra le quandre perchè il random da come uscita una lista
        id = 1
        lista_nemici = random_che_nemico_pescare(lista_nemici,id)




    elif quanti_nemici == ["2"]:
        id = 1
        lista_nemici = random_che_nemico_pescare(lista_nemici,id)
        id = 2
        lista_nemici = random_che_nemico_pescare(lista_nemici,id)




    elif quanti_nemici ==  ["3"]:
        id = 1
        lista_nemici = random_che_nemico_pescare(lista_nemici,id)
        id = 2
        lista_nemici = random_che_nemico_pescare(lista_nemici,id)
        id = 3
        lista_nemici = random_che_nemico_pescare(lista_nemici,id)



    return lista_nemici


def random_che_nemico_pescare(lista_nemici,id):
    with open("json_data/enemy_stats_dungeon_1.json","r") as file_nemici:
        lista_nemici_json = json.load(file_nemici)

    nemico_uscito = random.choice(lista_nemici_json)
    nome = nemico_uscito["name"]
    nemico_uscito["id"] = id
    nemico_uscito.update({"name":(nome + f" ({id})")})

    lista_nemici.append(nemico_uscito)

    return lista_nemici


def scelta_nel_turno(giocatore_vivo,lista_nemici,lista_giocatori_v):
    player_vivo_nome = colored(giocatore_vivo["name"],"cyan")
    print(f"è il turno del {player_vivo_nome} ")

    for nemico in lista_nemici:
        nomi_nemico = nemico["name"]
        #os.system("cls")# NON FUNZIONANTE QUI, TODO trovare un punto miglore
        print(colored(f"{nomi_nemico}   ","yellow"),end="   ")
    print(colored("\nattaccare   difendersi                             curarsi","blue"))
    choice = str(input("\n\n1               2           3           4           5\n"))
    match choice:
        case "1": #attaccare HA bisogno di un "rifai input"
            giocatore_vivo,lista_nemici = attaccare(giocatore_vivo,lista_nemici)
       
        case "2": #difendersi NON ha bisogno un "rifai input"
            difendersi(giocatore_vivo)


        case "3": #TODO magie
            pass
        case "5": #oggetti/inventario(eccetto armature/armi...). HA bisono di un "rifai input"
            with open("json_data/oggetti_curativi.json","r") as lista_oggetti_curativi:
                lista_oggetti_curativi = json.load(lista_oggetti_curativi)

            for cura in lista_oggetti_curativi:
                print(cura["name"])
            curarsi(lista_giocatori_v)
    return giocatore_vivo,lista_nemici

    
def sistema_turni(lista_nemici,piano_livello):
    with open("json_data/lista_giocatori.json","r") as lista_giocatori:
        lista_giocatori = json.load(lista_giocatori)
        lista_giocatori_v = []

    for giocatori in lista_giocatori: #spostati tutti i giocatori nella lista di giocatori vivi/attivi
        lista_giocatori_v.append(giocatori)

    battaglia_vinta = False
    battaglia_persa = False
    turno = 0
    lista_giocatori_m = [] #lista dei giocatori morti

    while battaglia_vinta == False and battaglia_persa == False: #ciclo di turni fino alla morte di tutti i nemici o alleati
        lista_hp_nemico = []
        lista_nomi_nemico = []
        lista_nomi_player = []
        lista_sp_player = []
        lista_hp_player = []
        

        if lista_nemici == []: #fine battaglia (vittoria) se lista_nemici è vuota
            
            print(colored("battaglia vinta!!","light_blue"))
            battaglia_vinta = True
        elif lista_giocatori_v == []: #avviene la fine della partita (perdendo) se lista_giocatori_v == vuota

            print(colored("team asfaltato... \n\nF","red"))
            battaglia_persa = True
            
        if battaglia_vinta == False and battaglia_persa == False:
            for giocatore_vivo in lista_giocatori_v:

                nome_player = giocatore_vivo["name"]
                lista_nomi_player.append(nome_player)

                sp_player = giocatore_vivo["sp"]
                lista_sp_player.append(sp_player)

                hp_player = giocatore_vivo["health"]
                lista_hp_player.append(hp_player)

            for nemico_ in lista_nemici:

                hp_nemico = nemico_["health"]
                lista_hp_nemico.append(hp_nemico) 

                nomi_nemici = nemico_["name"]
                lista_nomi_nemico.append(nomi_nemici)

            for giocatore_vivo in lista_giocatori_v:
                giocatore_vivo,lista_nemici = scelta_nel_turno(giocatore_vivo,lista_nemici,lista_giocatori_v)
            
            #lista_nomi_nemico = imposta_hud(giocatore_vivo,lista_hp_nemico,lista_hp_player,lista_nomi_nemico,lista_nomi_player,lista_sp_player,damage_tot)

            for nemico in lista_nemici:
                lista_giocatori_v = AI_nemico(nemico,lista_nemici,lista_giocatori_v,numero_piano,lista_giocatori_m)
            for persona in lista_giocatori_v:
                vita_rimasta = colored(persona["health"],"green")
                vita_max = colored(persona["max_health"],"light_green")
                nome_persona = colored(persona["name"],"cyan")
                print(f"il {nome_persona} {vita_rimasta}/{vita_max}hp")
            turno = turno + 1
            print(colored(turno,"light_cyan")) #conteggio turni

    




#il global level potrebbe essere usato per il conteggio dei piani per una sorta di palazzo/dungeon a piani
iniziare_run = str(input("iniziare una nuova run?\n\nyes\nno\n\n"))
if iniziare_run == "yes":
    numero_piano = inizio_run() 
    print("salvataggio creato...")
elif iniziare_run == "no":
    print("continuando dall'ultimo salvataggio...")
    pass


numero_piano = 1
lista_nemici = scelta_percentuali(numero_piano)
sistema_turni(lista_nemici,numero_piano)