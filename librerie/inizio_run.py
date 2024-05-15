import json
import os
import random
from art import text2art
from termcolor import colored
from combattimento import attaccare,difendersi,curarsi,AI_nemico,aspetta_input,riordina_lista_giocatori_in_battaglia,riordina_lista_giocatori_fuori_battaglia,magie
from sys import platform
if platform == "linux":
    clear = "clear"

    p_lista_giocatori = "json_data/lista_giocatori.json"
    p_lista_giocatori_in_game  = "json_data/lista_giocatori_in_game.json"
    p_oggetti_curativi = "json_data/oggetti_curativi.json"
    p_zaino = "json_data/zaino.json"
    p_magie = "json_data/magie.json"
    p_enemy_stats_dungeon = "json_data/enemy_stats_dungeon_1.json"
    
elif platform == "win32":
    clear = "cls"

    p_lista_giocatori = "json_data\lista_giocatori.json"
    p_lista_giocatori_in_game  = "json_data\lista_giocatori_in_game.json"
    p_oggetti_curativi = "json_data\oggetti_curativi.json"
    p_zaino = "json_data\zaino.json"
    p_magie = "json_data\magie.json"
    p_enemy_stats_dungeon = "json_data\enemy_stats_dungeon_1.json"

#python -> json = .dump
#json -> python = .load
def inizio_run(): #tutte le stat sono portare a 0
    #dichiarazione delle statistiche basi

    with open(p_lista_giocatori,"r") as file_json_lista_giocatori: #spostamento dei giocatori nella lista in gioco
        lista_giocatori = json.load(file_json_lista_giocatori)
    with open(p_lista_giocatori_in_game,"w") as file_json_lista_giocatori_giocatori_in_game:
        json.dump(lista_giocatori,file_json_lista_giocatori_giocatori_in_game,indent=4)

    with open(p_oggetti_curativi,"r") as lista_oggetti_curativi:
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
    with open(p_zaino,"w") as zaino_json:
        json.dump(zaino,zaino_json,indent=4)
        
    with open(p_magie,"r") as lista_magie:
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


def print_battaglia(lista_nemici,lista_giocatori_v,giocatore_vivo_,one_more,turno,crit):

    if one_more == True:
        os.system(clear)
        Art = text2art("o n e  m o r e",font="sub-zero")
        print(colored(Art,"blue"))
        aspetta_input()
        os.system(clear)
    if crit == True:
        os.system(clear)
        Art = text2art("c r i t",font="sub-zero")
        print(Art)
        aspetta_input()
        os.system(clear)
        

    nome = giocatore_vivo_["name"]
    colore_nome = giocatore_vivo_["colore_nome"]

    player_vivo_nome_c = colored(nome,colore_nome)
    turno_c = colored(turno,"red")

    print(colored(f"TURNO |{turno_c}",colore_nome),end="")
    print(colored("|",colore_nome))

    print(colored(f" è il turno del {player_vivo_nome_c}\n","grey"))

    
    

    #nemici
    i = -1
    for nemico in lista_nemici:

        i = i+1
        print("  " * i,end="") #crea una scaletta di spazi
        print(colored("                        HP","green"),end="\n")
        if i > 0:
            print("",end = "  " * i) #crea una scaletta di spazi
        quanti_tab = nemico["quanti_tab"]
        nome_nemico = nemico["name"]
        vita_max = nemico["max_health"]
        
        vita_max_c = colored(f"{vita_max}|","light_green")
        vita = nemico["health"]
        vita = int(vita)
        vita_c = colored(f"|{vita}","green")

        nemico_atterrato = nemico["atterrato"]
        if nemico_atterrato == True:
            nome_nemico_c = colored(nome_nemico,"grey")

        elif nemico_atterrato == False:
            nome_nemico_c = colored(nome_nemico,"light_red")

        quanti_tab = "\t" * quanti_tab
        print(nome_nemico_c + quanti_tab,end="")
        if i > 0:
            print("",end = "  " * i)
        print(f"{vita_c}/{vita_max_c}")
        
    print("\n\n",end="")

    #giocatori
    i = 0
    print(colored("-"*69,"grey"))
    for giocatore in lista_giocatori_v:
        
        i = i+1
        print("\t" * i,end="") #crea una scaletta di spazi
        
        print(colored("HP","green"),end="\t  ")
        print(colored("SP","magenta"),end="\n")
        if i > 1:
            print("",end = "  " * i)
        
        nome_giocatore = giocatore["name"]
        colore_nome = giocatore["colore_nome"]
        nome_giocatore_c = colored(f"|{nome_giocatore}|",colore_nome)
        print(nome_giocatore_c,end="\t")

        vita_giocatore = giocatore["health"]
        
        print(colored(f"|{vita_giocatore}","light_green"),end="/")

        vita_max_giocatore = giocatore["max_health"]
        print(colored(f"{vita_max_giocatore}|","green"),end="")

        sp_giocatore = giocatore["sp"]
        print(colored(f"|{sp_giocatore}","light_magenta"),end="/")

        sp_max_giocatore = giocatore["max_sp"]
        print(colored(f"{sp_max_giocatore}|","magenta"),end="\n")

    print(colored("-"*69,"grey"))

def random_che_nemico_pescare(lista_nemici,id):
    with open(p_enemy_stats_dungeon,"r") as file_nemici:
        lista_nemici_json = json.load(file_nemici)

    nemico_uscito = random.choice(lista_nemici_json)
    nome = nemico_uscito["name"]
    nemico_uscito["id"] = id
    id = colored(id,"grey")
    nemico_uscito.update({"name":(nome + f"  |{id}|")})

    lista_nemici.append(nemico_uscito)

    return lista_nemici


def scelta_nel_turno(giocatore_vivo_,lista_nemici,lista_giocatori_v,lista_giocatori_m,turno):
    rifai = True
    sp_insufficente = False
    one_more = False
    crit = False
    while rifai == True or sp_insufficente == True:

        sp_insufficente = False
        rifai = False
        battaglia_vinta = False

        if lista_nemici == []:
            battaglia_vinta = True
            break

        if battaglia_vinta == False:

            rifai_input = True
            

            while rifai_input == True:
                
                rifai_input = False
                os.system(clear)

                print_battaglia(lista_nemici,lista_giocatori_v,giocatore_vivo_,one_more,turno,crit)
                one_more = False
                crit = False
                
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
                rifai = True
                break
            crit = nemico_["crit"]
            if crit == True:
                nemico_.update({"crit":False})
                crit = True
                rifai = True
                break


        for i in range(len(lista_nemici)):
            for nemico in lista_nemici:
                vita_rimasta_nemico = nemico["health"]

                if vita_rimasta_nemico <= 0:

                    exp_drop = nemico["exp_drop"]
                    exp_player = giocatore_vivo_["exp"]
                    exp_ottenuta = exp_player + exp_drop
                    exp_ottenuta_c = colored(exp_ottenuta,"light_blue")
                    for giocatore in lista_giocatori_v:
                        giocatore.update({"exp":exp_ottenuta})
                    
                    lista_nemici.remove(nemico)
                    break


    return lista_nemici

    
def sistema_turni(lista_nemici,numero_piano):
    turno = 1
    with open(p_lista_giocatori_in_game,"r") as lista_giocatori: #da non cambiare
        lista_giocatori = json.load(lista_giocatori)

    lista_giocatori_v = []
    for giocatori in lista_giocatori: #spostati tutti i giocatori nella lista di giocatori vivi/attivi
        lista_giocatori_v.append(giocatori)

    with open(p_lista_giocatori_in_game,"w") as lista_giocatori_v:
        json.dump(lista_giocatori,lista_giocatori_v,indent=4)

    battaglia_vinta = False
    battaglia_persa = False
    lista_giocatori_m = [] #lista dei giocatori morti

#inizio sistema a turni
    while battaglia_vinta == False and battaglia_persa == False: #ciclo di turni fino alla morte di tutti i nemici o alleati
        with open(p_lista_giocatori_in_game,"r") as lista_giocatori_v:
            lista_giocatori_v = json.load(lista_giocatori_v)
        
        


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

            for giocatore_vivo_ in lista_giocatori_v:
                lista_nemici = scelta_nel_turno(giocatore_vivo_,lista_nemici,lista_giocatori_v,lista_giocatori_m,turno) #giocatore_vivo_ in return?

            for nemico in lista_nemici:
                lista_giocatori_v,lista_giocatori_m = AI_nemico(nemico,lista_nemici,lista_giocatori_v,numero_piano,lista_giocatori_m)


            with open(p_lista_giocatori_in_game,"w") as lista_giocatori_v_:
                json.dump(lista_giocatori_v,lista_giocatori_v_,indent=4)

            turno = turno + 1
            turno_c = colored(turno,"light_cyan")
            
    return battaglia_persa,battaglia_vinta,numero_piano,lista_giocatori_m,lista_giocatori_v

os.system(clear)


iniziare_run = "yes" #DEBUG
if iniziare_run == "yes":

    inizio_run() 
    print("salvataggio creato...")

    numero_piano = 0
    
elif iniziare_run == "no":
    
    print("continuando dall'ultimo salvataggio...")

    pass

def svuota_lista_giocatori_morti(lista_giocatori_m,lista_giocatori):

    for giocatore_morto in lista_giocatori_m:
        giocatore_morto.update({"health":1})
        lista_giocatori.append(giocatore_morto)

    
    return lista_giocatori




def scelta_carte(lista_giocatori,clear):
    os.system(clear)
    Art = text2art("c a r d   s h o u f f l e",font="sub-zero")
    print(colored(Art,"yellow"))
    aspetta_input()
    os.system(clear)
    carte_uscite = []
    recupera_metà_vita = {
            "nome":"+50% hp",
            "funzione":"tutti i tuoi alleati e te stesso recuperano un +50% di |hp| in più in base agli |hp massimi| di ciascuno",
            "colore":"green"
        }
    ventipercento_sp_up = {
            "nome":"+20% sp",
            "funzione":"tutti i tuoi alleati e te stesso recuperano un +20% di |sp| in più in base agli |sp massimi| di ciascuno",
            "colore":"magenta"
        }
    oggetto_curativo_random = {
            "nome":"cura casuale",
            "funzione":"otterrai una cura casuale",
            "colore":"light_green"
        }
    aumenta_attacco = {
            "nome":"+10% attacco magico",
            "funzione":"|EFFETTO PERMANENTE| tutti i tuoi alleati e te stesso otterranno un +10% di |attacco magico|",
            "colore":"red"
        }
    
    scelte_possibili = [recupera_metà_vita,ventipercento_sp_up,oggetto_curativo_random,aumenta_attacco]
    ris = random.randrange(2,4)
    for i in range(ris):
        ris_ = random.choice(scelte_possibili)
        scelte_possibili.remove(ris_)
        carte_uscite.append(ris_)

    i = 0
    for carta in carte_uscite:
        i=i+1
        carta.update({"posizione":i})

        nome = carta["nome"]
        colore_carta = carta["colore"]
        effetto_carta = carta["funzione"]
        if i > 1:
            print("",end="  " * i)

        print(colored(f"|{i}|","grey"),end=" ")
        print(colored(nome,colore_carta),end="   ")
        print(colored(f"\t{effetto_carta}","grey"),end="\n\n")

    rifai = True
    while rifai == True:
        rifai = False
        scelta = input(colored("\n...","grey"))
        try:
            scelta = int(scelta)
        except:
            print(colored("inserire un numero valido","grey"))
            rifai = True
        if len(carte_uscite) < scelta <= 0:
            rifai = True
    
    for carta in carte_uscite:
        
        posizione = carta["posizione"]
        if posizione == scelta:
            break


    nome_carta = carta["nome"]

    if nome_carta == "+50% hp":
        for giocatore in lista_giocatori:
            hp_max = giocatore["max_health"]
            hp = giocatore["health"]
            quanto_somm = int(hp_max/2)

            tot = quanto_somm + hp
            if tot > hp_max:
                tot = hp_max
            giocatore.update({"health":tot})
        
    elif nome_carta == "+20% sp":
        for giocatore in lista_giocatori:
            sp_max = giocatore["max_sp"]

            percentuale = (sp_max * 20)/100
            tot = sp_max + percentuale

            if tot > sp_max:
                tot = sp_max
            giocatore.update({"sp":tot})

    elif nome_carta == "cura casuale":
        with open(p_oggetti_curativi,"r") as oggetti_curativi:
            lista_oggetti_curativi = json.load(oggetti_curativi)

        oggetto_uscito = random.choice(lista_oggetti_curativi)
        with open(p_zaino,"r") as zaino_:
            zaino = json.load(zaino_)

        zaino.append(oggetto_uscito)
        with open(p_zaino,"w") as zaino_json:
            json.dump(zaino,zaino_json,indent=4)
        print(colored(oggetto_uscito,"yellow"))

    elif nome_carta == "+10% attacco magico":
        for giocatore in lista_giocatori:
            danno_magie = giocatore["danno_magie"]

            percentuale = (danno_magie * 10)/100
            tot = danno_magie + percentuale

            giocatore.update({"danno_magie":tot})
    return lista_giocatori





for numero_piano in range(6):

    os.system(clear)
    numero_piano_c = colored(numero_piano + 1 ,"light_red")
    lista_nemici = scelta_percentuali(numero_piano)
    battaglia_persa,battaglia_vinta,numero_piano,lista_giocatori_m,lista_giocatori_v = sistema_turni(lista_nemici,numero_piano)

    if battaglia_vinta == True:
        #TODO vuoi salvare?
        #TODO vuoi chiudere il programa?
        lista_giocatori = svuota_lista_giocatori_morti(lista_giocatori_m,lista_giocatori_v)

        riordina_lista_giocatori_fuori_battaglia(lista_giocatori)
        lista_giocatori = scelta_carte(lista_giocatori,clear)

        with open(p_lista_giocatori_in_game,"w") as lista_giocatori_:
            json.dump(lista_giocatori,lista_giocatori_,indent=4)

        print(f"\n\nSALENDO...\nPIANO:|{numero_piano_c}|\n\n")
        aspetta_input()

    elif battaglia_persa == True:

        riprovare = {
            "funzione":"riprovare",
            "posizione":1
        }
        salvare = {
            "funzione":"salva ed esci",
            "posizione":2
        }
        esci = {
            "funzione":"esci senza salvare",
            "posizione":3
        }
        opzioni = [riprovare,salvare,esci]
        i = 0
        for opzione in opzioni:
            funzione = opzione["funzione"]
            posizione = opzione["posizione"]
            i = i+1
            if i > 1:
                print("",end = "  " * i) #crea una scaletta di spazi
            print(colored(posizione,"grey"),end=" ")
            print(funzione)
        scelta = str(input(colored("...","grey")))
        if scelta == 1:
            #riprova battaglia
            pass
        elif scelta == 2:
            #salva ed esci
            pass
        elif scelta == 3:
            os.system(clear)
            print(colored("uscendo dal programma...","grey"))
            aspetta_input()
            os.system("^C")
            os.system(clear)
    