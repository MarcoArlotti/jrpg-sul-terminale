import json
import os
import random
import termcolor
#python -> json = .dump
#json -> python = .load
def inizio_run(): #tutte le stat sono portare a 0
    #dichiarazione delle statistiche basi
    health = int(240)
    sp = int(26)
    global_level = 1
    #NAME = input(str("\ninsersci il nome del tuo personaggio:\n'"))
    NAME = "Galo"
    speed = float(19)
    damage_base = float(10) #danno percentuale da aggiungere al danno grezzo dell'arma
    damage = int(32)
    melee = {
        "damage":damage,
        "price":0,
        "type":None
    }
    player = {
        "name":NAME,
        "health":health,
        "speed":speed,
        "exp":0.00,
        "sp":sp,
        "damage_base":damage_base,
        "current_equip_melee":melee
    }
    lista_player = []
    lista_player.append(player)

    with open("lista_giocatori.json","w") as file_json: #creazione del json player_stats
        json.dump(lista_player, file_json, indent=4)
    return global_level


def dichiara_enemy(): #trasporta una lista con tutti i tipi di nemici e li converte in un json (list-->.json)
    
    shadow = {
    "HEALTH":46,                   
    "NAME":"SHADOW",               
    "SPEED":15.00,
    "TYPE":"ice",
    "dungeon":1
    }
    flying_shadow = {
        "HEALTH":20,
        "NAME":"FLYING SHADOW",
        "SPEED":37.00,
        "TYPE":"air",
        "dungeon":1
    }

    nemici = [shadow,flying_shadow]
    with open("enemy_stats_dungeon_1.json","w") as file_json:
        json.dump(nemici,file_json,indent=4)


#def fix_uguali(lista_nemici,quanti_nemici):
#    print(quanti_nemici)
#    if quanti_nemici == ["2"]:
#
#       primo = lista_nemici[0]
#       
#       secondo = lista_nemici[1]
#       
#       primo_nome = primo["NAME"]
#       secondo_nome = secondo["NAME"]
#
#       if primo_nome == secondo_nome:
#           primo_nome = primo_nome+" a"
#           primo.update({"NAME":primo_nome})
#
#           secondo_nome = secondo_nome+" b"
#           secondo.update({"NAME":secondo_nome})
#
#    elif quanti_nemici == ["3"]:
#
#        primo = lista_nemici[0]
#        secondo = lista_nemici[1]
#        terzo = lista_nemici[2]
#        primo_nome = primo["NAME"]
#        secondo_nome = secondo["NAME"]
#        terzo_nome = terzo["NAME"]
#
#        if primo_nome == secondo_nome and primo_nome != terzo_nome: # a = b,  a != c
#            primo_nome = primo_nome+" a"
#            primo.update({"NAME":primo_nome})
#            
#            secondo_nome = secondo_nome+" b"
#            secondo.update({"NAME":secondo_nome})
#        elif primo_nome != secondo_nome and primo_nome == terzo_nome: # a != b, a = c
#            primo_nome = primo_nome+" a"
#            primo.update({"NAME":primo_nome})
#                            
#            terzo_nome = terzo_nome+" b"
#            terzo.update({"NAME":terzo_nome})
#        elif primo_nome != secondo_nome and secondo_nome == terzo_nome: # a != b, b = c
#            
#            secondo_nome = secondo_nome+" a"
#            secondo.update({"NAME":secondo_nome})
#                            
#            terzo_nome = terzo_nome+" b"
#            terzo.update({"NAME":terzo_nome})
#            
#        elif primo_nome == secondo_nome and secondo_nome == terzo_nome: # a = b = c
#            primo_nome = primo_nome+" a"
#            primo.update({"NAME":primo_nome})
#            secondo_nome = secondo_nome+" b"
#            secondo.update({"NAME":secondo_nome})
#            terzo_nome = terzo_nome+" c"
#            terzo.update({"NAME":terzo_nome})
#    lista_nemici_fix = []
#
#    print(lista_nemici)

#    return lista_nemici_fix
    
def crea_battaglia(global_level):
    with open("enemy_stats_dungeon_1.json") as file_nemici:
        lista_nemici_json = json.load(file_nemici)

    lista_nemici = []
    flip = ["1","2","3"]
    lista_hp = []
    lista_nomi = []
    if global_level < 5: #il livello dei nemici fa variare la quantità che appareranno #GLOBAL_LEVEL
        
        quanti_nemici = random.choices(flip,weights=[20,40,15],k=1)

        lista_nemici = spawn_nemici(quanti_nemici,lista_nemici_json,lista_nemici)
        
    elif 5 < global_level < 15:

        quanti_nemici = random.choices(flip,weights=[15,50,40],k=1)
        lista_nemici = spawn_nemici(quanti_nemici,lista_nemici_json,lista_nemici)
    

    #imposta_hud(lista_hp,lista_nomi)
    return lista_nemici


def spawn_nemici(quanti_nemici,lista_nemici_json,lista_nemici):

    if quanti_nemici == ["1"]: # tra le quandre perchè il random da come uscita una lista
        id = 1
        lista_nemici = selettore_nemici(lista_nemici_json,lista_nemici,id)


        #print(f"un nemici è uscito, {lista_nomi}\n{lista_hp}")

    elif quanti_nemici == ["2"]:
        id = 1
        lista_nemici = selettore_nemici(lista_nemici_json,lista_nemici,id)
        id = 2
        lista_nemici = selettore_nemici(lista_nemici_json,lista_nemici,id)


        #print(f"due nemici sono usciti, {lista_nomi}\n{lista_hp}")

    elif quanti_nemici ==  ["3"]:
        id = 1
        lista_nemici = selettore_nemici(lista_nemici_json,lista_nemici,id)
        id = 2
        lista_nemici = selettore_nemici(lista_nemici_json,lista_nemici,id)
        id = 3
        lista_nemici = selettore_nemici(lista_nemici_json,lista_nemici,id)

        #print(f"tre nemici sono usciti, {lista_nomi}\n{lista_hp}")

    return lista_nemici


def selettore_nemici(lista_nemici_json,lista_nemici,id):

    nemico = random.choice(lista_nemici_json)
    nemico["id"] = id
    
    lista_nemici.append(nemico)
    print(nemico)
    return lista_nemici


def scelta_nel_turno(giocatore_vivo,lista_nemici):
    
    
    choice = str(input("che cosa si vuole fare?"))
    match choice:
        case "1": #attacco base
            lista_nemici = attaccare(giocatore_vivo,lista_nemici)
       
        case "2": #TODO difendersi (immagina...)
            pass
        case "3":
            pass



def attaccare(giocatore_vivo,lista_nemici):
    rifai = True
    while rifai == True:
        rifai = False
        current_equip_melee = giocatore_vivo["current_equip_melee"]
        damage_melee = current_equip_melee["damage"] #preso il danno grezzo dalla arma equipaggiata
        damage_base_percentuale = giocatore_vivo["damage_base"] #percentuale di danno aumentato all'arma equipaggiata che aumenta di valore livellando

        damage_percentuale = (damage_melee * damage_base_percentuale)/100
        damage_tot = damage_melee + damage_percentuale
        damage_tot = int(damage_tot) #conversione per non avere la virgola nel danno

        chi_attaccare = int(input("che nemico attaccare?")) #posizione nella lista

        for nemico_ in lista_nemici:

            id_nemico = nemico_["id"]
            
            if chi_attaccare == id_nemico:

                print(f"il nemico {nemico_} subisce {damage_tot}hp di danno!")

                hp_nemico = nemico_["HEALTH"]
                danno_aggiorato = hp_nemico - damage_tot
                nemico_.update({"HEALTH":danno_aggiorato})                   
                
                print(f"chi attacare == {chi_attaccare}")
                print(f"id nemicojjjiji == {id_nemico}") #questo blocco viene eseguito 2 volte BUG
                break
            
        #if chi_attaccare != id_nemico:
        #    print("il nemico selezionato non esite/valore non valido")
        #    rifai == True
            
            
        for nemico in lista_nemici:
            vita_rimasta_nemico = nemico["HEALTH"]
            print(vita_rimasta_nemico)
            if vita_rimasta_nemico <= 0:
                lista_nemici.remove(nemico)
                id_ = nemico["id"]
                print(f"nemico di id {id_} è morto")
                break
        
    return lista_nemici

def sistema_turni(lista_nemici):
    with open("lista_giocatori.json","r") as lista_giocatori:
        lista_giocatori = json.load(lista_giocatori)
        lista_giocatori_v = []
    for giocatori in lista_giocatori: #spostati tutti i giocatori nella lista di giocatori vivi/attivi
        lista_giocatori_v.append(giocatori)

    battaglia_vinta = False
    battaglia_persa = False
    while battaglia_vinta == False and battaglia_persa == False:
        for giocatore_vivo in lista_giocatori_v:
            scelta_nel_turno(giocatore_vivo,lista_nemici)

            if lista_nemici == []: #fine battaglia
                print("battaglia vinta!!")
                battaglia_vinta = True
            if lista_giocatori_v == []: #fine partita
                print("team asfaltato... \n\nF")
                battaglia_persa = True






#il global level potrebbe essere usato per il conteggio dei piani per una sorta di palazzo (dungeon) a piani
global_level = inizio_run() 

dichiara_enemy()

lista_nemici_fix = crea_battaglia(global_level)
sistema_turni(lista_nemici_fix)
