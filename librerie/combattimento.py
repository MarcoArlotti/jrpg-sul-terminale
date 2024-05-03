import json
import os
import random
from termcolor import colored
def aspetta_input():
    a = input(colored("press return to continue...","grey"))

def debolezze(tipo_magia_player,nemico_):
    print(colored(tipo_magia_player,"red"))
    lista_magia_debole_nemico = nemico_["debole"] 
    lista_magia_resiste_nemico = nemico_["resiste"]
    status = "normale"
    for resistenza in lista_magia_resiste_nemico:
        if resistenza == tipo_magia_player:
            status = "resiste"
            break
    for debolezza in lista_magia_debole_nemico:
        if debolezza == tipo_magia_player:
            status = "debole"
            break
    
    return status

def magie_funzionamento(giocatore_vivo_,percentuale_boost_potenza_magie,magia,nemico_):
    
    potenza = magia["potenza"]
    tipo_magia_player = magia["type"]
    
    status = debolezze(tipo_magia_player,nemico_)
    nome_nemico_c = colored(nemico_["name"],"yellow")
    
    if status == "debole":
        print(f"{nome_nemico_c} è",end = " ")
        print(colored("DEBOLE","blue"))
        
        nemico_atterrato = nemico_["atterrato"]
        if nemico_atterrato == True:

            nemico_.update({"one_more":False})
        elif nemico_atterrato == False:

            nemico_.update({"one_more":True})
            nemico_.update({"atterrato":True})

        if potenza == "scarsa":

            danno_inflitto = 70 * percentuale_boost_potenza_magie
        elif potenza == "normale":

            danno_inflitto = 90 * percentuale_boost_potenza_magie
        elif potenza == "devastante":

            danno_inflitto = 110 * percentuale_boost_potenza_magie

    elif status == "resiste":
        print(f"{nome_nemico_c} è",end = " ")
        print(colored("RESISTENTE","grey"))
        
        if potenza == "scarsa":
            

            danno_inflitto = 4 * percentuale_boost_potenza_magie
        elif potenza == "normale":

            danno_inflitto = 25 * percentuale_boost_potenza_magie
        elif potenza == "devastante":

            danno_inflitto = 30 * percentuale_boost_potenza_magie

    if status == "normale":
        

        if potenza == "scarsa":

            danno_inflitto = 40 * percentuale_boost_potenza_magie
        elif potenza == "normale":

            danno_inflitto = 70 * percentuale_boost_potenza_magie
        elif potenza == "devastante":

            danno_inflitto = 90 * percentuale_boost_potenza_magie

    return danno_inflitto

def magie(giocatore_vivo_,lista_nemici):
    sp_giocatore = giocatore_vivo_["sp"]
    sp_max_giocatore = giocatore_vivo_["max_sp"]
    nome_giocatore = giocatore_vivo_["name"]

    nome_giocatore_c = colored(nome_giocatore,"cyan")
    sp_giocatore_c = colored(sp_giocatore,"light_blue")
    sp_max_giocatore_c = colored(sp_max_giocatore,"blue")
    
    print(f"{nome_giocatore} {sp_giocatore_c}/{sp_max_giocatore_c}sp")

    i = 0
    lista_magie_giocatore = giocatore_vivo_["magie"]
    for magia in lista_magie_giocatore:
        i = i+1
        magia.update({"posizione":i})

    battaglia_vinta = False
    if lista_nemici == []: #fine battaglia (vittoria) se lista_nemici è vuota
        battaglia_vinta = True
    if battaglia_vinta == True:
        pass
    elif battaglia_vinta == False:

        sp_insufficente = True
        while sp_insufficente == True:
            sp_insufficente = False
            for magia_ in lista_magie_giocatore:

                nome_magia = magia_["nome"]
                print(colored(nome_magia,"light_cyan"),end=" ")
                numero_magia = magia_["posizione"]
                print(colored(numero_magia,"grey"))

            magia_scelta = int(input("inserire il numero di quale magia scegliere..."))
            os.system("cls")
            for magia in lista_magie_giocatore:

                numero_magia = magia["posizione"]

                if magia_scelta == numero_magia:
                    costo_sp_magia = magia["costo"]
                    

                    sp_rimasta = sp_giocatore - costo_sp_magia
                    if sp_rimasta < 0:
                        print(colored("sp insufficente...","grey"))
                        aspetta_input()
                        os.system("cls")
                        sp_insufficente == True
                    elif sp_rimasta >= 0:
                        giocatore_vivo_.update({"sp":sp_rimasta})

                    break
        for magia in lista_magie_giocatore:
            numero_magia = magia["posizione"]

            if magia_scelta == numero_magia:

                rifai_input = True
                while rifai_input == True:
                
                    rifai_input = False
                    raggio = magia["raggio"]
                    if raggio == "singolo":
                        chi_attaccare = input("che nemico attaccare?") #che nemico attaccare(solo se la magia non colpisce tutti)

                        try:
                            chi_attaccare = int(chi_attaccare)
                        except:
                            print(colored("rifare inserendo un valore numerico...","grey"))
                            rifai_input = True                        
                break

        os.system("cls")
        rifai = True
        
        while rifai == True:
            rifai = False

            if raggio == "singolo":
                
                for nemico_ in lista_nemici:
                    nemico = nemico_
                    id_nemico = nemico_["id"]
                    nome_nemico = nemico_["name"]

                    if chi_attaccare == id_nemico: #serve nome_,damage_tot

                        nemico_preso = preso_o_mancato_nemici(nemico_)
                        nome_nemico = colored(nome_nemico,"yellow")

                        if nemico_preso == [True]:
                            percentuale_boost_potenza_magie = giocatore_vivo_["danno_magie"]
                            danno_inflitto = magie_funzionamento(giocatore_vivo_,percentuale_boost_potenza_magie,magia,nemico)
                            vita_nemico = nemico_["health"]
                            vita_rimasta_nemico = vita_nemico - danno_inflitto
                            nemico_.update({"health":vita_rimasta_nemico})

                        elif nemico_preso == [False]:
                            print(f"il nemico {nome_nemico} ha mancato l'attacco")
                        break
                if chi_attaccare != id_nemico:
                    print(colored("il nemico selezionato non esite/valore non valido","grey"))
                    chi_attaccare = int(input("che nemico attaccare?")) #id da prendere
                    rifai = True


            elif raggio == "gruppo":

                for nemico in lista_nemici:

                    battaglia_vinta = False
                    
                    if lista_nemici == []: #fine battaglia (vittoria) se lista_nemici è vuota

                        battaglia_vinta = True
                        break
                    if battaglia_vinta == False:
                        id_nemico = nemico["id"]
                        nome_nemico = nemico["name"]

                        nemico_preso = preso_o_mancato_nemici(nemico)
                        nome_nemico = colored(nome_nemico,"yellow")

                        if nemico_preso == [True]:

                            percentuale_boost_potenza_magie = giocatore_vivo_["danno_magie"]
                            danno_inflitto = magie_funzionamento(giocatore_vivo_,percentuale_boost_potenza_magie,magia,nemico)
                            print(colored(danno_inflitto,"magenta"))
                            vita_nemico = nemico["health"]
                            vita_rimasta_nemico = vita_nemico - danno_inflitto
                            nemico.update({"health":vita_rimasta_nemico})

                        elif nemico_preso == [False]:
                            print(f"il nemico {nome_nemico} ha mancato l'attacco")

#            for nemico in lista_nemici:
#
#                vita_rimasta_nemico = nemico["health"]
#                
#                if vita_rimasta_nemico <= 0:
#
#                    exp_drop = nemico["exp_drop"]
#                    exp_player = giocatore_vivo_["exp"]
#                    exp_ottenuta = exp_player + exp_drop
#                    giocatore_vivo_.update({"exp":exp_ottenuta})
#                    print(colored(f"exp ottenuta: {exp_ottenuta}EXP","light_cyan"))
#                    lista_nemici.remove(nemico)
#                    break
    return giocatore_vivo_,lista_nemici

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
                nome_nemico = nemico_["name"]
                if chi_attaccare == id_nemico: #serve nome_,damage_tot

                    nemico_preso = preso_o_mancato_nemici(nemico_)
                    nome_nemico = colored(nome_nemico,"yellow")
                    if nemico_preso == [True]:

                        hp_nemico = nemico_["health"]
                        danno_aggiorato = hp_nemico - damage_tot
                        damage_tot_c = colored(damage_tot,"red")

                        nemico_.update({"health":danno_aggiorato})
                        print(f"il nemico {nome_nemico} ha subito -{damage_tot_c} hp")
                    elif nemico_preso == [False]:

                        print(f"il nemico {nome_nemico} ha mancato l'attacco")

                    break
                
            if chi_attaccare != id_nemico:
                print(colored("il nemico selezionato non esite/valore non valido","grey"))
                chi_attaccare = int(input("che nemico attaccare?")) #id da prendere
                rifai = True

    return giocatore_vivo_,lista_nemici

def preso_o_mancato_nemici(nemico_):
    nemico_velocità = nemico_["speed"]
    nemico_velocità_opposto = 100 - nemico_velocità
    flip = True,False
    
    nemico_preso = random.choices(flip,weights=[nemico_velocità_opposto,nemico_velocità],k=1)

    return nemico_preso
def difendersi(giocatore_vivo):
    os.system("cls")
    giocatore_vivo.update({"guard":True})
    giocatore = giocatore_vivo["name"]
    giocatore = colored(giocatore,"light_cyan")
    print(f"il {giocatore} si sta difendendo")
    aspetta_input()
    os.system("cls")

def rimuovi_cura(lista_oggetti_zaino,cura_scelta):
    posizione_oggetto_scelto = cura_scelta["numero_nella_lista"]
    for oggetto in lista_oggetti_zaino:
        posizione_oggetto = oggetto["numero_nella_lista"]
        if posizione_oggetto == posizione_oggetto_scelto:
            lista_oggetti_zaino.remove(oggetto)
            break
    with open("json_data/zaino.json","w") as zaino:
        json.dump(lista_oggetti_zaino,zaino,indent=4)

def curarsi(lista_giocatori_v,lista_giocatori_m): #BUG gli sp non si rimuovono

    rifai_input = False
    os.system("cls")
    rifai = True
    cura_scelta = None
    while cura_scelta == None:
        cura_scelta = menù_oggetti()
    
    while rifai == True:
        with open("json_data/zaino.json","r") as lista_oggetti_zaino:
            lista_oggetti_zaino = json.load(lista_oggetti_zaino)
        rifai = False
        tipo_oggetto = cura_scelta["type"]

        if tipo_oggetto == "hp":
            chi_curare = str(input(f"a chi si vuole curare gli HP?\n"))
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
                    print(colored(f"{vita_max} hp","light_green"))
                    nome_trovato = True
                    rimuovi_cura(lista_oggetti_zaino,cura_scelta)
                    break
            if nome_trovato == False:
                print(colored("persona non trovata...\nriprovare scrivendo lettera per lettera (e maiuscole) il nome della cura\n","grey"))
                rifai = True          

        elif tipo_oggetto == "sp":
            chi_curare = str(input(f"a chi si vuole curare gli SP?\n"))
            sp_recuperato = cura_scelta["effetto"] 
            nome_trovato = False
            for persona in lista_giocatori_v:
                nome_persona = persona["name"]
                if chi_curare == nome_persona:
                
                    sp_persona = persona["sp"]
                    sp_max = persona["max_sp"]
                    sp_finale = sp_persona + sp_recuperato
                    if sp_finale > sp_max:
                        sp_finale = sp_max
                        sp_info = sp_finale
                    elif sp_finale < sp_max:
                        sp_info = sp_finale
                    persona.update({"sp":sp_finale})
                    nome_persona = colored(nome_persona,"cyan")
                    sp_recuperata = colored(sp_info,"blue")
                    print(f"{nome_persona} si è curato... {sp_recuperata}/",end="")
                    print(colored(f"{sp_max} sp","light_blue"))
                    nome_trovato = True
                    rimuovi_cura(lista_oggetti_zaino,cura_scelta)
                    break
            if nome_trovato == False:
                print(colored("persona non trovata...\nriprovare scrivendo lettera per lettera (e maiuscole) il nome della cura\n","grey"))
                rifai = True

        elif tipo_oggetto == "revive" and not lista_giocatori_m == []:

            chi_curare = str(input(f"chi si vuole far resuscitare?\n"))
            vita_recuperata = cura_scelta["effetto"] 
            nome_trovato = False
            for persona in lista_giocatori_m:
                nome_persona = persona["name"]
                if chi_curare == nome_persona:
                    vita_max = persona["max_health"]
                    
                    if vita_recuperata == "met\u00e0":
                        vita_finale = vita_max / 2
                        vita_finale = int(vita_finale)

                    elif vita_recuperata == "max":
                        vita_finale = vita_max

                    persona.update({"health":vita_finale})
                    nome_persona = colored(nome_persona,"cyan")
                    vita_recuperata = colored(vita_finale,"green")
                    print(f"{nome_persona} è ora vivo... {vita_recuperata}/",end="")
                    print(colored(f"{vita_max} hp","light_green"))
                    nome_trovato = True
                    lista_giocatori_v.append(persona)
                    lista_giocatori_m.remove(persona)
                    print(colored(lista_giocatori_m,"red"),end="\n\n") #MOMENTANEO
                    print(colored(lista_giocatori_v,"blue"))
                    rimuovi_cura(lista_oggetti_zaino,cura_scelta)
                    break
            if nome_trovato == False:
                print(colored("persona non trovata...\nriprovare scrivendo lettera per lettera (e maiuscole) il nome della cura\n","grey"))
                rifai = True

        elif tipo_oggetto == "revive" and lista_giocatori_m == []:
            print(colored("tutti i giocatori sono vivi, cura non usata...","grey"))
            rifai_input = True
            
        if rifai_input == False:
            i = 1
            for oggetto in lista_oggetti_zaino:
                oggetto.update({"numero_nella_lista":i})
                i = i + 1
            with open("json_data\zaino.json","w") as zaino_json:
                json.dump(lista_oggetti_zaino,zaino_json,indent=4)
    return rifai_input
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
        os.system("cls")
        finito = False

        if len(lista_oggetti_cure) > 9 and finito == False: # menù
            fare_if = True
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
                    fare_if = False
            except:
                lunghezza_lista_meno_min = len(lista_oggetti_cure) - numero_min - 1
                for j in range(lunghezza_lista_meno_min):
                    n_attuale = j + numero_min 

                    cura_attuale = lista_oggetti_cure[n_attuale]
                    print(colored(cura_attuale["name"],"green"),end=" ")
                    print(colored(cura_attuale["numero_nella_lista"],"grey"))
                scelta = input(colored("mettere cosa scegliere tra \">\",\"<\",\"stop\", il numero in grigio...\n","grey"))
                try:
                    scelta = int(scelta) 
                except:
                    scelta = str(scelta)
                    fare_if = False
            if scelta == ">":
                numero_min = numero_min + 9
                if numero_min > len(lista_oggetti_cure):
                    numero_min = numero_min - 9
                    
            elif scelta == "<":
                if numero_min >= 9:
                    numero_min = numero_min - 9

            elif scelta == "stop":
                #TODO torna indietro (cancella scelta cura)

                pass
            if fare_if == True:
                if scelta <= len(lista_oggetti_cure):
                    finito = True
                    cura_scelta = lista_oggetti_cure[scelta - 1]

                if finito == True:
                    pass
                
        elif len(lista_oggetti_cure) <= 9 and finito == False: #selezione basica di max len di 9
            fai_if = True
            for a in range(len(lista_oggetti_cure)):
                cura_attuale = lista_oggetti_cure[a]
                print(colored(cura_attuale["name"],"green"),end=" ")
                print(colored(cura_attuale["numero_nella_lista"],"grey"))
            scelta = input(colored("mettere cosa scegliere \"stop\" o  un numero tra 1 e 9...\n","grey"))
            try:
                scelta = int(scelta)
                
            except:
                scelta = str(scelta)
                fai_if = False


            lunghezza_lista = len(lista_oggetti_cure)
            if fai_if == True and scelta <= lunghezza_lista:
                finito = True
                cura_scelta = lista_oggetti_cure[scelta - 1]
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
    nemico.update({"atterrato":False})
    nemico.update({"one_more":False})
    print(nemico["atterrato"])
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
        #elif numero_piano > 2:
            #i nemici posso attaccare con magie
             
    
    for giocatore in lista_giocatori_v:
        vita_player = giocatore["health"]
        if vita_player <= 0:
            
            lista_giocatori_m.append(giocatore)
            lista_giocatori_v.remove(giocatore)

            print(colored("il","red"),end=" ")
            print(colored(giocatore["name"],"cyan"),end=" ")
            print(colored("è morto","red"),end="\n")

    return lista_giocatori_v