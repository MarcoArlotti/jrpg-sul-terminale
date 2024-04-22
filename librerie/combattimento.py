import json
import os
import random
from termcolor import colored
def aspetta_input():
    a = input(colored("press return to continue...","grey"))

def fuoco(potenza,persona_v): #fuoco ad attacco debole,medio,pesante,area
    pass


def attaccare(giocatore_vivo_,lista_nemici): #TODO si rompe il programma perchè il def non si interrompe quando muoiono tutti i nemici

    battaglia_vinta = False
    if lista_nemici == []: #fine battaglia (vittoria) se lista_nemici è vuota
        battaglia_vinta = True
    if battaglia_vinta == True:
        pass
    elif battaglia_vinta == False:
        current_equip_melee = giocatore_vivo_["current_equip_melee"]
        damage_melee = current_equip_melee["damage"] #preso il danno grezzo dalla arma equipaggiata
        damage_base_percentuale = giocatore_vivo_["damage_base"] #percentuale di danno aumentato all'arma equipaggiata che aumenta di valore livellando
        damage_percentuale = (damage_melee * damage_base_percentuale)/100
        damage_tot = damage_melee + damage_percentuale
        damage_tot = int(damage_tot) #conversione per non avere la virgola nel danno
        

        rifai_input = True
        while rifai_input == True:
            rifai_input = False
            chi_attaccare = input("che nemico attaccare?") #id/nome da prendere
            try:
                chi_attaccare = int(chi_attaccare)
            except:
                print(colored("rifare inserendo un valore numerico...","grey"))
                rifai_input = True


        os.system("cls")
        rifai = True
        
        while rifai == True:
            rifai = False
            for nemico_ in lista_nemici:
                id_nemico = nemico_["id"]
                if chi_attaccare == id_nemico: #serve nome_,damage_tot
                    hp_nemico = nemico_["health"]
                    danno_aggiorato = hp_nemico - damage_tot
                    nemico_.update({"health":danno_aggiorato})                   
                    break
                
            if chi_attaccare != id_nemico:
                print(colored("il nemico selezionato non esite/valore non valido","grey"))
                chi_attaccare = int(input("che nemico attaccare?")) #id da prendere
                rifai = True
            for nemico in lista_nemici:
                vita_rimasta_nemico = nemico["health"]
                if vita_rimasta_nemico <= 0:
                    exp_drop = nemico["exp_drop"]
                    exp_player = giocatore_vivo_["exp"]
                    exp_ottenuta = exp_player + exp_drop
                    giocatore_vivo_.update({"exp":exp_ottenuta})
                    print(colored(f"exp ottenuta: {exp_ottenuta}EXP","light_cyan"))
                    lista_nemici.remove(nemico)
                    break

    return giocatore_vivo_,lista_nemici


def difendersi(giocatore_vivo):
    os.system("cls")
    giocatore_vivo.update({"guard":True})
    giocatore = giocatore_vivo["name"]
    giocatore = colored(giocatore,"light_cyan")
    print(f"il {giocatore} si sta difendendo")
    aspetta_input()
    os.system("cls")


def curarsi(lista_giocatori_v):
    os.system("cls")
    rifai = True
    cura_scelta = None
    while cura_scelta == None:
        cura_scelta = menù_oggetti()
    while rifai == True:
        rifai = False
        chi_curare = str(input(f"chi si vuole curare?\n"))
        vita_recuperata = cura_scelta["effetto"] 
        nome_trovato = False
        for persona in lista_giocatori_v:
            nome_persona = persona["name"]
            if chi_curare == nome_persona:
            
                vita_persona = persona["health"]
                vita_max = persona["max_health"]
                vita_finale = vita_persona + vita_recuperata
                if vita_finale > vita_max:
                    vita_finale = vita_max
                    vita_info = vita_finale
                elif vita_finale < vita_max:
                    vita_info = vita_finale
                persona.update({"health":vita_finale})
                nome_persona = colored(nome_persona,"cyan")
                vita_recuperata = colored(vita_info,"green")
                print(f"{nome_persona} si è curato... {vita_recuperata}/",end="")
                print(colored(f"{vita_max} hp","light_green")) #TODO rimuovere le cure usate dall'inventario dopo l'uso
                nome_trovato = True
                break
        if nome_trovato == False:
            print(colored("persona non trovata...\nriprovare scrivendo lettera per lettera (e maiuscole) il nome della cura\n","grey"))
            rifai = True
def name_item(lista_oggetti_zaino):
    return lista_oggetti_zaino["name"]
def menù_oggetti():
    with open("json_data/zaino.json","r") as lista_oggetti_zaino:
        lista_oggetti_zaino = json.load(lista_oggetti_zaino)
    lista_oggetti_zaino.sort(key=name_item) #riordinamento oggetti per nome

    lista_oggetti_cure = []
    lista_oggetti_vari = [] #oggetti che non sono cure che verranno usate dopo per riaggiornare zaino.json?
    lista_oggetti_tutti = []
    for oggetto in lista_oggetti_zaino:
        tipologia_oggetto = oggetto["type"]

        if tipologia_oggetto == "hp" or tipologia_oggetto == "sp" or tipologia_oggetto == "revive": #smistamento tra cure ed altri oggetti
            lista_oggetti_cure.append(oggetto)
        else:
            lista_oggetti_vari.append(oggetto)

    #menù a 9 scelte + 2 di movimento + torna inditro
    numero_cura = 1
    for cura in lista_oggetti_cure:
        cura.update({"numero_nella_lista":numero_cura})
        numero_cura = numero_cura + 1

    finito = False
    numero_min = 0
    while finito == False:
        non_fare_for = False 
        finito = False
        if len(lista_oggetti_cure) > 9: # menù
            try:
                for i in range(9): #TODO come capire se è più lungo di 9 (se no crash programma)
                    n_attuale = i + numero_min
                    cura_attuale = lista_oggetti_cure[n_attuale]
                    print(colored(cura_attuale["name"],"green"),end=" ")
                    print(colored(cura_attuale["numero_nella_lista"],"grey"))
                scelta = input(colored("mettere cosa scegliere tra \">\",\"<\",\"stop\", il numero in grigio...\n","grey"))
                try:
                    scelta = int(scelta)
                except:
                    scelta = str(scelta)
            except:
                lunghezza_lista_meno_min =len(lista_oggetti_cure) - numero_min - 1
                for j in range(lunghezza_lista_meno_min):
                    n_attuale = j + numero_min 

                    cura_attuale = lista_oggetti_cure[n_attuale] #BUG lui va i out of index
                    print(colored(cura_attuale["name"],"green"),end=" ")
                    print(colored(cura_attuale["numero_nella_lista"],"grey"))
                scelta = input(colored("mettere cosa scegliere tra \">\",\"<\",\"stop\", il numero in grigio...\n","grey"))
                try:
                    scelta = int(scelta)
                except:
                    scelta = str(scelta)

            if scelta == ">":
                numero_min = numero_min + 9
                non_fare_for = True
            elif scelta == "<" and numero_min >= 9:
                if numero_min != 0:
                    numero_min = numero_min -9
                non_fare_for = True
                

            elif scelta == "stop":
                #TODO torna indietro (cancella scelta cura)
                non_fare_for = True
                pass
            else:
                #TODO VALORE MESSO NON VALIDO rifai = True
                non_fare_for = True
                pass
            if non_fare_for == False:

                if scelta >= 1:
                    finito = True
                    cura_scelta = lista_oggetti_cure[scelta - 1]
                    lista_oggetti_cure.remove(cura_scelta)
                    finito = True
                if finito == True:
                    for oggetto_ in lista_oggetti_vari:
                        lista_oggetti_tutti.append(oggetto_)
                    for cura_ in lista_oggetti_cure:
                        lista_oggetti_tutti.append(cura_)
                    with open("json_data/zaino.json","w") as zaino:
                        json.dump(lista_oggetti_tutti,zaino,indent=4)
                
        elif len(lista_oggetti_cure) <= 9 and finito == False: #selezione basica di max len di 9
            for a in range(len(lista_oggetti_cure)):
                cura_attuale = lista_oggetti_cure[a]
                print(colored(cura_attuale["name"],"green"),end=" ")
                print(colored(cura_attuale["numero_nella_lista"],"grey"))
            scelta = input(colored("mettere cosa scegliere \"stop\" o  un numero tra 1 e 9...\n","grey"))
            try:
                scelta = int(scelta)
            except:
                scelta = str(scelta)


            lunghezza_lista = len(lista_oggetti_cure)
            if scelta <= lunghezza_lista and scelta == type(int):
                finito = True
                cura_scelta = lista_oggetti_cure[scelta - 1]
                lista_oggetti_cure.remove(cura_scelta)
                
                for oggetto_ in lista_oggetti_vari:
                    lista_oggetti_tutti.append(oggetto_)
                for cura_ in lista_oggetti_cure:
                    lista_oggetti_tutti.append(cura_)
                with open("json_data/zaino.json","w") as zaino:
                    json.dump(lista_oggetti_tutti,zaino,indent=4)
            elif scelta == "stop":
                pass
    return cura_scelta








        
    


def posizione(lista_giocatori):
    return lista_giocatori["posizione"]
#da fare per quella in battaglia
def riordina_lista_giocatori_in_battaglia(lista_giocatori_v):
    pass
def riordina_lista_giocatori_fuori_battaglia(lista_giocatori):

    lista_giocatori.sort(key=posizione)
    return lista_giocatori

def AI_nemico(nemico,lista_nemici,lista_giocatori_v,numero_piano,lista_giocatori_m):
    giocatori_morti = False

    if lista_giocatori_v == []:
        giocatori_morti = True
        
    if giocatori_morti == False:
        nemico_nome = colored(nemico["name"],"light_red")
        if numero_piano <= 2: #se i nemici si trovano al piano 3 o inferiore attaccheranno e basta
            danno_nemico = nemico["damage"]

            chi_attaccare_player = random.choice(lista_giocatori_v)
            chi_attaccare_player_nome = chi_attaccare_player["name"]

            for giocatore in lista_giocatori_v:
                nome_giocatore = giocatore["name"]

                if nome_giocatore == chi_attaccare_player_nome:
                    vita_player = giocatore["health"]
                    parata_attiva = giocatore["guard"]

                    if parata_attiva == True:
                        danno_nemico = int(danno_nemico / 2)

                    vita_player = vita_player - danno_nemico
                    giocatore_nome = colored(nome_giocatore,"cyan")
                    danno_nemico = colored(danno_nemico,"red")

                    print(f"il nemico {nemico_nome} ha inflitto -{danno_nemico}hp al {giocatore_nome}")
                    giocatore.update({"health":vita_player})
                    aspetta_input()
                    os.system("cls")
                    break
            
    
    for giocatore in lista_giocatori_v:
        vita_player = giocatore["health"]
        if vita_player <= 0:
            
            lista_giocatori_m.append(giocatore)
            lista_giocatori_v.remove(giocatore)

            print(colored("il","red"),end=" ")
            print(colored(giocatore["name"],"cyan"),end=" ")
            print(colored("è morto","red"),end="\n")

    return lista_giocatori_v