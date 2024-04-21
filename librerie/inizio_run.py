import json
import os
import random
from termcolor import colored
from combattimento import attaccare,difendersi,fuoco,curarsi,AI_nemico,aspetta_input,riordina_lista_giocatori_in_battaglia,riordina_lista_giocatori_fuori_battaglia

#python -> json = .dump
#json -> python = .load
def inizio_run(): #tutte le stat sono portare a 0
    #dichiarazione delle statistiche basi

    with open("json_data/lista_giocatori.json","r") as file_json_lista_giocatori: #spostamento dei giocatori nella lista in gioco
        lista_giocatori = json.load(file_json_lista_giocatori)
    with open("json_data/lista_giocatori_in_game.json","w") as file_json_lista_giocatori_giocatori_in_game:
        json.dump(lista_giocatori,file_json_lista_giocatori_giocatori_in_game,indent=4)

    with open("json_data/oggetti_curativi.json","r") as lista_oggetti_curativi:
        lista_oggetti_curativi = json.load(lista_oggetti_curativi)

    #3 cure parziali, 2 cure ps, un med metà
    #TODO in base alla difficoltà, aumentare/diminuire, costo/quantità degli oggetti
    zaino = [{
        "name":"cura parziale",
        "effetto":50,
        "valore":3.5,
        "type":"hp"
    },
    {
        "name":"cura parziale",
        "effetto":50,
        "valore":3.5,
        "type":"hp"
    },
    {
        "name":"cura pesante",
        "effetto":80,
        "valore":6.8,
        "type":"hp"
    },
    {
        "name":"cura sp",
        "effetto":30,
        "valore":7.5,
        "type":"sp"
    },
    {
        "name":"cura sp",
        "effetto":30,
        "valore":7.5,
        "type":"sp"
    },
    {
        "name":"med metà",
        "effetto":"metà",
        "valore":16.0,
        "type":"revive"
    },
    {
        "name":"med metà",
        "effetto":"metà",
        "valore":16.0,
        "type":"revive"
    },
    
    ]
    with open("json_data\zaino.json","w") as zaino_json:
        json.dump(zaino,zaino_json,indent=4)



def scelta_percentuali(numero_piano):

    lista_nemici = []
    flip = ["1","2","3"]

    if numero_piano < 5: #il livello dei nemici fa variare la quantità che appariranno #GLOBAL_LEVEL
        
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


def scelta_nel_turno(giocatore_vivo_,lista_nemici,lista_giocatori_v):
    battaglia_vinta = False
    if lista_nemici == []:
        battaglia_vinta = True

    player_vivo_nome = colored(giocatore_vivo_["name"],"cyan")
    print(f"è il turno del {player_vivo_nome}\n")

    for nemico in lista_nemici:
        nomi_nemico = nemico["name"]
        print(colored(f"{nomi_nemico}   ","yellow"),end="   ")
    print(colored("\nattaccare   difendersi                             curarsi","blue"))
    if battaglia_vinta == False:
        
        rifai_input = True

        while rifai_input == True:
            rifai_input = False
            choice = input(colored("\n1             2           3           4           5\n","red"))

            try:
                choice = int(choice)
            except:
                print(colored("rifare inserendo un valore numerico...","grey"))
                rifai_input = True

        match choice:
            case 1: #attaccare HA bisogno di un "rifai input"
                giocatore_vivo_,lista_nemici = attaccare(giocatore_vivo_,lista_nemici)

            case 2: #difendersi NON ha bisogno un "rifai input"
                difendersi(giocatore_vivo_)


            case 3: #TODO magie
                pass
            case 4: #TODO tag out (solo se protagonista)
                pass
            case 5: #oggetti/inventario(eccetto armature/armi...). HA bisono di un "rifai input"
                curarsi(lista_giocatori_v)
    return lista_nemici

    
def sistema_turni(lista_nemici,numero_piano):
    #with open("json_data/lista_giocatori_in_game.json","r") as lista_giocatori_:
    #    lista_giocatori_ = json.load(lista_giocatori_)

    with open("json_data/lista_giocatori_in_game.json","r") as lista_giocatori: #da non cambiare
        lista_giocatori = json.load(lista_giocatori)
    lista_giocatori_v = []
    for giocatori in lista_giocatori: #spostati tutti i giocatori nella lista di giocatori vivi/attivi
        lista_giocatori_v.append(giocatori)

    with open("json_data\lista_giocatori_in_game.json","w") as lista_giocatori_v:
        json.dump(lista_giocatori,lista_giocatori_v,indent=4)

    battaglia_vinta = False
    battaglia_persa = False
    turno = 0
    lista_giocatori_m = [] #lista dei giocatori morti

#inizio sistema a turni
    while battaglia_vinta == False and battaglia_persa == False: #ciclo di turni fino alla morte di tutti i nemici o alleati
        #TODO ad ogni loop i player vengono resettati e il json dei nemici in game non viene aggiornato
        with open("json_data/lista_giocatori_in_game.json","r") as lista_giocatori_v:
            lista_giocatori_v = json.load(lista_giocatori_v)
        
        lista_hp_nemico = []
        lista_hp_nemico_max = []
        lista_nomi_nemico = []
        lista_nomi_player = []
        lista_sp = []
        lista_sp_max = []
        lista_hp_player = []
        lista_hp_player_max = []

        if lista_nemici == []: #fine battaglia (vittoria) se lista_nemici è vuota
            
            print(colored("battaglia vinta!","light_blue"))
            battaglia_vinta = True
            lista_giocatori = []

            for persona in lista_giocatori_m: #sposta la lista giocatori morti cambiandogli la vita in lista_giocatori(fuoori dalla battaglia)
                persona.update({"health":1})
                lista_giocatori.append(persona)

            for persona_ in lista_giocatori_v:
                lista_giocatori.append(persona_)
            lista_giocatori = riordina_lista_giocatori_fuori_battaglia(lista_giocatori)
        elif lista_giocatori_v == []: #avviene la fine della partita (perdendo) se lista_giocatori_v == vuota

            print(colored("team asfaltato...\n","red"))
            battaglia_persa = True
            #os.system("shutdown/c\"/SKILL ISSUE\"")
                  
        if battaglia_vinta == False and battaglia_persa == False: 

            for giocatore_vivo in lista_giocatori_v:

                nome_player = giocatore_vivo["name"]
                lista_nomi_player.append(nome_player)

                sp = giocatore_vivo["sp"]
                lista_sp.append(sp)

                hp_player = giocatore_vivo["health"]
                lista_hp_player.append(hp_player)

            for nemico_ in lista_nemici:

                hp_nemico = nemico_["health"]
                lista_hp_nemico.append(hp_nemico) 

                nomi_nemici = nemico_["name"]
                lista_nomi_nemico.append(nomi_nemici)

            for giocatore_vivo_ in lista_giocatori_v:
                lista_nemici = scelta_nel_turno(giocatore_vivo_,lista_nemici,lista_giocatori_v) #giocatore_vivo_ in return?
            
            lista_nomi_nemico = imposta_hud_nemici(lista_hp_nemico,lista_hp_player,lista_nomi_nemico,lista_nomi_player,lista_sp)

            for nemico in lista_nemici:
                lista_giocatori_v = AI_nemico(nemico,lista_nemici,lista_giocatori_v,numero_piano,lista_giocatori_m)
                for persona in lista_giocatori_v:

                    vita_rimasta = colored(persona["health"],"green")
                    vita_max = colored(persona["max_health"],"light_green")
                    nome_persona = colored(persona["name"],"cyan")
                    print(f"il {nome_persona} {vita_rimasta}/{vita_max}hp",end="    ")

            with open("json_data\lista_giocatori_in_game.json","w") as lista_giocatori_v_:
                json.dump(lista_giocatori_v,lista_giocatori_v_,indent=4)

            turno = turno + 1
            turno_c = colored(turno,"light_cyan")
            print(f"Turno {turno_c}") #conteggio turni

            

    

    #with open("json_data\lista_giocatori_in_game.json","w") as lista_giocatori:
    #    json.dump(lista_giocatori_,lista_giocatori,indent=4)

    return battaglia_persa,battaglia_vinta,numero_piano


#il global level potrebbe essere usato per il conteggio dei piani per una sorta di palazzo/dungeon a piani

os.system("cls")
iniziare_run = str(input("iniziare una nuova run?\n\nyes\nno\n\n"))
os.system("cls")
if iniziare_run == "yes":

    inizio_run() 
    print("salvataggio creato...")

    numero_piano = 0
    
elif iniziare_run == "no":
    
    print("continuando dall'ultimo salvataggio...")

    pass




for numero_piano in range(6):
    os.system("cls")
    numero_piano_c = colored(numero_piano + 1 ,"light_red")
    lista_nemici = scelta_percentuali(numero_piano)
    
    battaglia_persa,battaglia_vinta,numero_piano = sistema_turni(lista_nemici,numero_piano)

    with open("json_data/lista_giocatori_in_game.json","r") as lista_giocatori:
        lista_giocatori = json.load(lista_giocatori)

    print(lista_giocatori)
    if battaglia_vinta == True:
        #TODO vuoi salvare?
        #TODO vuoi chiudere il programa?
        print(f"\n\nSALENDO IL PIANO [{numero_piano_c}]\n\n")
        aspetta_input()
    elif battaglia_persa == True:
        #TODO vuoi riprovare?
        #TODO vuoi salvare?
        #TODO vuoi chiudere il programa?
        #TODO vuoi
        break

    