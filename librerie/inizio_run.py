import json
import os
import random
from termcolor import colored
from combattimento import attaccare,difendersi,curarsi,AI_nemico,aspetta_input,riordina_lista_giocatori_in_battaglia,riordina_lista_giocatori_fuori_battaglia,magie

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
    i = 1
    for oggetto in zaino:
        oggetto.update({"numero_nella_lista":i})
        i = i + 1
    with open("json_data\zaino.json","w") as zaino_json:
        json.dump(zaino,zaino_json,indent=4)
        
    with open("json_data/magie.json","r") as lista_magie:
        lista_magie = json.load(lista_magie)




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


def print_nemici(lista_nemici,lista_giocatori_v,player_vivo_nome):
    os.system("cls")
    print(f"è il turno del {player_vivo_nome}",end="\n\n")
    #nemici
    i = -1
    print()
    for nemico in lista_nemici:

        i = i+1
        if i > 0:
            print("",end = "  " * i) #crea una scaletta di spazi
        quanti_tab = nemico["quanti_tab"]
        nome_nemico = nemico["name"]
        vita_max = nemico["max_health"]
        
        vita_max_c = colored(vita_max,"light_green")
        vita = nemico["health"]
        vita_c = colored(vita,"green")

        nemico_atterrato = nemico["atterrato"]
        if nemico_atterrato == True:
            nome_nemico_c = colored(nome_nemico,"grey")
            print(colored("ATTERRATO","grey"),end="     ")

        elif nemico_atterrato == False:
            nome_nemico_c = colored(nome_nemico,"yellow")

        quanti_tab = "\t" * quanti_tab
        print(nome_nemico_c + quanti_tab,end="")
        if i > 0:
            print("",end = "  " * i)
        print(f"{vita_c}/{vita_max_c}")
    print("\n\n",end="")

    #giocatori
    i = 0
    for giocatore in lista_giocatori_v:

        i = i+1
        if i > 1:
            print("",end = " " * i) #crea una scaletta di spazi

        nome_giocatore = giocatore["name"]
        nome_giocatore_c = colored(nome_giocatore,"cyan")
        print(nome_giocatore_c,end=" ")

        vita_giocatore = giocatore["health"]
        print(colored(vita_giocatore,"light_green"),end="/")

        vita_max_giocatore = giocatore["max_health"]
        print(colored(vita_max_giocatore,"green"))


def random_che_nemico_pescare(lista_nemici,id):
    with open("json_data/enemy_stats_dungeon_1.json","r") as file_nemici:
        lista_nemici_json = json.load(file_nemici)

    nemico_uscito = random.choice(lista_nemici_json)
    nome = nemico_uscito["name"]
    nemico_uscito["id"] = id
    nemico_uscito.update({"name":(nome + f" ({id})")})

    lista_nemici.append(nemico_uscito)

    return lista_nemici


def scelta_nel_turno(giocatore_vivo_,lista_nemici,lista_giocatori_v,lista_giocatori_m):
    one_more = True
    sp_insufficente = False
    while one_more == True or sp_insufficente == True:

        sp_insufficente = False
        one_more = False
        battaglia_vinta = False

        if lista_nemici == []:
            battaglia_vinta = True
            break

        player_vivo_nome = colored(giocatore_vivo_["name"],"cyan")

        print_nemici(lista_nemici,lista_giocatori_v,player_vivo_nome)

        
        if battaglia_vinta == False:

            rifai_input = True

            while rifai_input == True:
                rifai_input = False
                os.system("cls")

                print_nemici(lista_nemici,lista_giocatori_v,player_vivo_nome)

                print(colored("\n1","grey"),end=" ")
                print(colored("ATTACCARE","light_blue"),end="")
                
                print(colored("\n\t2","grey"),end=" ")
                print(colored("PARARE","cyan"),end="")

                print(colored("\n\t\t3","grey"),end=" ")
                print(colored("MAGIE","light_blue"),end="")

                print(colored("\n\t\t\t4","grey"),end=" ")
                print(colored("CURE","cyan"),end="\n")
        
                choice = input(colored("...","grey"))

                try:
                    choice = int(choice)
                except:
                    print(colored("rifare inserendo un valore numerico...","grey"))
                    aspetta_input()
                    rifai_input = True

                match choice:
                    case 1: #attaccare HA bisogno di un "rifai input"
                        giocatore_vivo_,lista_nemici = attaccare(giocatore_vivo_,lista_nemici)

                    case 2: #difendersi NON ha bisogno un "rifai input"
                        difendersi(giocatore_vivo_)


                    case 3: #magie
                        lista_giocatori_v,sp_insufficente,giocatore_vivo_,lista_nemici = magie(giocatore_vivo_,lista_giocatori_v,lista_nemici)
                    case 4:#oggetti/inventario(eccetto armature/armi...). HA bisono di un "rifai input"
                        rifai_input = curarsi(lista_giocatori_v,lista_giocatori_m)


        for nemico_ in lista_nemici:

            one_more_ = nemico_["one_more"]
            if one_more_ == True:
                nemico_.update({"one_more":False})
                one_more = True
                print(colored("ONE MORE","cyan"))

        #for nemico in lista_nemici: #funziona solo se si deve cancellare un solo nemico
        for i in range(len(lista_nemici)):
            for nemico in lista_nemici:
                vita_rimasta_nemico = nemico["health"]

                if vita_rimasta_nemico <= 0:

                    exp_drop = nemico["exp_drop"]
                    exp_player = giocatore_vivo_["exp"]
                    exp_ottenuta = exp_player + exp_drop
                    exp_ottenuta_c = colored(exp_ottenuta,"light_blue")
                    giocatore_vivo_.update({"exp":exp_ottenuta})
                    print(colored(f"exp ottenuta: {exp_ottenuta_c}EXP","light_cyan"))
                    lista_nemici.remove(nemico)
                    break


    return lista_nemici

    
def sistema_turni(lista_nemici,numero_piano):

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
                lista_nemici = scelta_nel_turno(giocatore_vivo_,lista_nemici,lista_giocatori_v,lista_giocatori_m) #giocatore_vivo_ in return?
                #ddeeweeaew
            
            #lista_nomi_nemico = imposta_hud_nemici(lista_hp_nemico,lista_hp_player,lista_nomi_nemico,lista_nomi_player,lista_sp)

            for nemico in lista_nemici:
                lista_giocatori_v = AI_nemico(nemico,lista_nemici,lista_giocatori_v,numero_piano,lista_giocatori_m)
                for persona in lista_giocatori_v:

                    vita_rimasta = colored(persona["health"],"green")
                    vita_max = colored(persona["max_health"],"light_green")
                    nome_persona = colored(persona["name"],"cyan")
                    print(f"il {nome_persona} {vita_rimasta}/{vita_max}sp",end="    ")

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
#iniziare_run = str(input("iniziare una nuova run?\n\nyes\nno\n\n"))
#os.system("cls")



#iniziare_run = str(input("iniziare una nuova run?\n\nyes\nno\n\n"))
#os.system("cls")
iniziare_run = "yes" #DEBUG
if iniziare_run == "yes":

    inizio_run() 
    print("salvataggio creato...")

    numero_piano = 0
    
elif iniziare_run == "no":
    
    print("continuando dall'ultimo salvataggio...")

    pass


for numero_piano in range(6):
    with open("json_data/lista_giocatori_in_game.json","r") as lista_giocatori:
        lista_giocatori = json.load(lista_giocatori)
    os.system("cls")
    numero_piano_c = colored(numero_piano + 1 ,"light_red")
    lista_nemici = scelta_percentuali(numero_piano)
    battaglia_persa,battaglia_vinta,numero_piano = sistema_turni(lista_nemici,numero_piano)

    with open("json_data/lista_giocatori_in_game.json","r") as lista_giocatori:
        lista_giocatori = json.load(lista_giocatori)

    if battaglia_vinta == True:
        #TODO vuoi salvare?
        #TODO vuoi chiudere il programa?
        print(f"\n\nSALENDO IL PIANO [{numero_piano_c}]\n\n") #BUG persone duplicate/le persone non resuscitate dopo una vittoria non ritornano in vita con 1 hp
        aspetta_input()
    elif battaglia_persa == True:
        #TODO vuoi riprovare?
        #TODO vuoi salvare?
        #TODO vuoi chiudere il programa?
        #TODO vuoi
        break

    