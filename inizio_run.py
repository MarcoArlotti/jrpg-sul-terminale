import json
import os
import random
import termcolor
from termcolor import colored

os.system("cls")
#python -> json = .dump
#json -> python = .load
def inizio_run(): #tutte le stat sono portare a 0
    #dichiarazione delle statistiche basi
    health = int(240)
    sp = int(26)
    global_level = 1
    #name = input(str("\ninsersci il nome del tuo personaggio:\n'"))
    name = "Galo"
    speed = float(19)
    damage_base = float(10) #danno percentuale da aggiungere al danno grezzo dell'arma
    damage = int(32)
    melee = {
        "damage":damage,
        "price":0,
        "type":None
    }
    player = {
        "name":name,
        "health":health,
        "speed":speed,
        "exp":0.00,
        "sp":sp,
        "damage_base":damage_base,
        "current_equip_melee":melee
    }
    lista_player = []
    lista_player.append(player)

    with open("json_data/lista_giocatori.json","w") as file_json: #creazione del json player_stats
        json.dump(lista_player, file_json, indent=4)
    return global_level


def dichiara_enemy(): #trasporta una lista con tutti i tipi di nemici e li converte in un json (list-->.json)
    
    shadow = {
    "name":"SHADOW", 
    "health":110,                        
    "speed":15.00,
    "type":"ice",
    "dungeon":1,
    "exp_drop":3
    }
    flying_shadow = {
        "name":"FLYING SHADOW",
        "health":76,
        "speed":37.00,
        "type":"air",
        "dungeon":1,
        "exp_drop":2.3
    }

    nemici = [shadow,flying_shadow]
    with open("json_data/enemy_stats_dungeon_1.json","w") as file_json:
        json.dump(nemici,file_json,indent=4)

def scelta_percentuali(global_level):

    lista_nemici = []
    flip = ["1","2","3"]

    if global_level < 5: #il livello dei nemici fa variare la quantità che appareranno #GLOBAL_LEVEL
        
        quanti_nemici = random.choices(flip,weights=[20,40,15],k=1)

        lista_nemici = random_quanti_nemici(quanti_nemici,lista_nemici)
        
    elif global_level < 15 and global_level >= 5:

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

    nemico_ = random.choice(lista_nemici_json)
    nome = nemico_["name"]
    nemico_["id"] = id
    nemico_.update({"name":(nome + f" ({id})")})

    lista_nemici.append(nemico_)

    return lista_nemici


def scelta_nel_turno(giocatore_vivo,lista_nemici):
    
    for nemico in lista_nemici:
        nomi_nemico = nemico["name"]
        os.system("cls") #MOMENTANEAMENTE QUI, TODO trovare un punto miglore
        print(colored(f"{nomi_nemico}   ","yellow"),end="   ")
    choice = str(input("\n\n1        2        3        4\n"))
    match choice:
        case "1": #attacco base
            giocatore_vivo,lista_nemici,T_nome_,damage_tot = attaccare(giocatore_vivo,lista_nemici)
       
        case "2": #TODO difendersi (immagina...)
            pass
        case "3": #TODO magie
            pass
    return giocatore_vivo,lista_nemici,T_nome_,damage_tot



def attaccare(giocatore_vivo,lista_nemici):
    
    current_equip_melee = giocatore_vivo["current_equip_melee"]
    damage_melee = current_equip_melee["damage"] #preso il danno grezzo dalla arma equipaggiata
    damage_base_percentuale = giocatore_vivo["damage_base"] #percentuale di danno aumentato all'arma equipaggiata che aumenta di valore livellando
    damage_percentuale = (damage_melee * damage_base_percentuale)/100
    damage_tot = damage_melee + damage_percentuale
    damage_tot = int(damage_tot) #conversione per non avere la virgola nel danno
    
    chi_attaccare = int(input("che nemico attaccare?")) #id da prendere
    rifai = True
    while rifai == True:
        rifai = False
        for nemico_ in lista_nemici:

            id_nemico = nemico_["id"]
            
            nome_ = nemico_["name"]
            if chi_attaccare == id_nemico: #serve nome_,damage_tot

                T_nome_ = nome_
                hp_nemico = nemico_["health"]
                danno_aggiorato = hp_nemico - damage_tot
                nemico_.update({"health":danno_aggiorato})                   
                
                break
            
        if chi_attaccare != id_nemico:
            print(colored("il nemico selezionato non esite/valore non valido","red"))
            chi_attaccare = int(input("che nemico attaccare?")) #id da prendere
            rifai = True
            
            
        for nemico in lista_nemici:
            vita_rimasta_nemico = nemico["health"]
            
            if vita_rimasta_nemico <= 0:
                exp_drop = nemico["exp_drop"]
                exp_player = giocatore_vivo["exp"]
                exp_ottenuta = exp_player + exp_drop
                giocatore_vivo.update({"exp":exp_ottenuta})
                print(colored(f"exp ottenuta: {exp_ottenuta}EXP","light_cyan"))
                lista_nemici.remove(nemico)
        
                break
        
    return giocatore_vivo,lista_nemici,T_nome_,damage_tot

def imposta_hud(giocatore_vivo,lista_hp_nemico,lista_hp_player,lista_nomi_nemico,lista_nomi_player,lista_sp_player,damage_tot):
    
    for nome in lista_nomi_nemico:
        if nome == #id del nemico (da convertire da id a nome)
        print(f"il nemico",end=" ") #print del danno inflitto al nemico selezionato
        print(colored(nome,"red"),end=" ")
        print("ha subito",end= " ")
        print(colored(f"{damage_tot}hp","green"),end=" ")
        print("di danno",end="\n\n")
    giocatore_attivo_nome = giocatore_vivo["name"]
    for nome_player in lista_nomi_player:
        nome_player_ = nome_player["name"]

        print(colored(nome_player_,"cyan"),end="    ")
        if nome_player_ == giocatore_attivo_nome:
            print(colored(nome_player_,"grey"),end="    ")
            


    rallenta_terminale = str(input(colored("press any button...","grey"))) #serve solo per fermare/rallentare il terminale
    return lista_nomi_nemico


    
def sistema_turni(lista_nemici):
    with open("json_data/lista_giocatori.json","r") as lista_giocatori:
        lista_giocatori = json.load(lista_giocatori)
        lista_giocatori_v = []
    for giocatori in lista_giocatori: #spostati tutti i giocatori nella lista di giocatori vivi/attivi
        lista_giocatori_v.append(giocatori)
    battaglia_vinta = False
    battaglia_persa = False
    turno = 0
    while battaglia_vinta == False and battaglia_persa == False:
        lista_hp_nemico = []
        lista_nomi_nemico = []
        lista_nomi_player = []
        lista_sp_player = []
        lista_hp_player = []

        for giocatore_vivo in lista_giocatori_v:

            nome_player = giocatore_vivo["name"]
            lista_nomi_player.append(nome_player)

            sp_player = giocatore_vivo["sp"]
            lista_sp_player.append(sp_player)

            hp_player = giocatore_vivo["health"]
            lista_hp_player.append(hp_player)

        for nemico_ in lista_nemici:
            print(nemico_)

            hp_nemico = nemico_["health"]
            lista_hp_nemico.append(hp_nemico) #BUG

            nomi_nemici = nemico_["name"]
            lista_nomi_nemico.append(nomi_nemici)
        
        giocatore_vivo,lista_nemici,T_nome_,damage_tot = scelta_nel_turno(giocatore_vivo,lista_nemici)
        lista_nomi_nemico = imposta_hud(giocatore_vivo,lista_hp_nemico,lista_hp_player,lista_nomi_nemico,lista_nomi_player,lista_sp_player,damage_tot)

        
        if lista_nemici == []: #fine battaglia (vittoria) se lista_nemici è vuota
            print(colored("battaglia vinta!!","light_blue"))
            battaglia_vinta = True
        if lista_giocatori_v == []: #avviene la fine della partita (perdendo) se lista_giocatori_v == vuota
            print(colored("team asfaltato... \n\nF","red"))
            battaglia_persa = True
        
        for nemico in lista_nemici:
            AI_nemico(nemico,lista_nemici,lista_giocatori_v)

        turno = turno + 1
        print(colored(turno,"light_cyan")) #conteggio turni

        


def AI_nemico(nemico,lista_nemici,lista_giocatori_v):
    pass


#il global level potrebbe essere usato per il conteggio dei piani per una sorta di palazzo/dungeon a piani
global_level = inizio_run() 

dichiara_enemy()

lista_nemici = scelta_percentuali(global_level)
sistema_turni(lista_nemici)