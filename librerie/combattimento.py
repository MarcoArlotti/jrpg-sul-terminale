import json
import os
import random
from art import text2art
from termcolor import colored
from sys import platform
if platform == "linux":
    clear = "clear"

    p_zaino = "json_data/zaino.json"

elif platform == "win32":
    clear = "cls"

    p_zaino = "json_data\zaino.json"

def aspetta_input():
    return_c = colored("\"return\"","red")
    a = input(colored(f"\npress {return_c}...","grey"))

def debolezze(tipo_magia_player,nemico_):
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

def magie_funzionamento(percentuale_boost_potenza_magie,magia,nemico_):
    potenza = magia["potenza"]
    tipo_magia_player = magia["type"]
    status = None
    
    
    if not tipo_magia_player == "cura":
        status = debolezze(tipo_magia_player,nemico_)
    
    if tipo_magia_player == "cura": #la variabile "danno inflitto" verrà convertita in quanta vita curare
            
        if potenza == "scarsa":

            danno_inflitto = 55 * percentuale_boost_potenza_magie
            danno_inflitto = int(danno_inflitto)
        elif potenza == "normale":

            danno_inflitto = 100 * percentuale_boost_potenza_magie
            danno_inflitto = int(danno_inflitto)
        elif potenza == "devastante":

            danno_inflitto = 155 * percentuale_boost_potenza_magie
            danno_inflitto = int(danno_inflitto)


    if status == "debole" and not tipo_magia_player == "cura":
        
        nemico_atterrato = nemico_["atterrato"]
        if nemico_atterrato == True:

            nemico_.update({"one_more":False})
        elif nemico_atterrato == False:

            nemico_.update({"one_more":True})
            nemico_.update({"atterrato":True})

        if potenza == "scarsa":

            danno_inflitto = 60 * percentuale_boost_potenza_magie
            danno_inflitto = int(danno_inflitto)
        elif potenza == "normale":

            danno_inflitto = 80 * percentuale_boost_potenza_magie
            danno_inflitto = int(danno_inflitto)
        elif potenza == "devastante":

            danno_inflitto = 100 * percentuale_boost_potenza_magie
            danno_inflitto = int(danno_inflitto)

    elif status == "resiste" and not tipo_magia_player == "cura":
        
        if potenza == "scarsa":
            

            danno_inflitto = 5 * percentuale_boost_potenza_magie
            danno_inflitto = int(danno_inflitto)
        elif potenza == "normale":

            danno_inflitto = 15 * percentuale_boost_potenza_magie
            danno_inflitto = int(danno_inflitto)
        elif potenza == "devastante":

            danno_inflitto = 20 * percentuale_boost_potenza_magie
            danno_inflitto = int(danno_inflitto)

    if status == "normale" and not tipo_magia_player == "cura":
        

        if potenza == "scarsa":

            danno_inflitto = 35 * percentuale_boost_potenza_magie
            danno_inflitto = int(danno_inflitto)
        elif potenza == "normale":

            danno_inflitto = 65 * percentuale_boost_potenza_magie
            danno_inflitto = int(danno_inflitto)
        elif potenza == "devastante":

            danno_inflitto = 85 * percentuale_boost_potenza_magie
            danno_inflitto = int(danno_inflitto)

    return danno_inflitto


def magie(giocatore_vivo_,lista_giocatori_v,lista_nemici):

    rifai_input = False
    sp_giocatore = giocatore_vivo_["sp"]
    hp_giocatore = giocatore_vivo_["health"]
    hp_max_giocatore = giocatore_vivo_["max_health"]

    sp_max_giocatore = giocatore_vivo_["max_sp"]
    nome_giocatore = giocatore_vivo_["name"]

    colore_nome = giocatore_vivo_["colore_nome"]
    nome_giocatore_c = colored(nome_giocatore,colore_nome)

    hp_giocatore_c = colored(f"|{hp_giocatore}","light_green")
    hp_max_giocatore_c = colored(f"{hp_max_giocatore}|","green")

    sp_giocatore_c = colored(f"|{sp_giocatore}","magenta")
    sp_max_giocatore_c = colored(f"{sp_max_giocatore}|","light_magenta")

    i = 0
    lista_magie_giocatore = giocatore_vivo_["magie"]
    for magia in lista_magie_giocatore:
        i = i+1
        magia.update({"posizione":i})

    battaglia_vinta = False
    if lista_nemici == []: #fine battaglia (vittoria) se lista_nemici è vuota
        battaglia_vinta = True

    elif battaglia_vinta == False:

        rifai = True
        while rifai == True:
            os.system(clear)
            rifai = False

            sp_insufficente = False
            hp_insufficente = False
            i = 0
            print(f"{nome_giocatore_c} {hp_giocatore_c}",end="")
            print(colored("/",colore_nome),end="")
            print(hp_max_giocatore_c,end="")
            print(colored("HP",colore_nome),end="")
            print(sp_giocatore_c,end="")
            print(colored("/",colore_nome),end="")
            print(sp_max_giocatore_c,end="")
            print(colored("SP",colore_nome))

            for magia_ in lista_magie_giocatore:
                i = i+1
                print()
                if i > 0:
                    print("",end = " " * i) #crea una scaletta di spazi
                
                numero_magia = magia_["posizione"]
                print(colored(numero_magia,"grey"),end="  ")

                tipo_magia = magia_["type"]
                effetto = magia_["effetto"]
                if tipo_magia == "fire":
                    colore_magia = "red"
                elif tipo_magia == "ice":
                    colore_magia = "light_blue"
                elif tipo_magia == "wind":
                    colore_magia = "green"
                elif tipo_magia == "elettric":
                    colore_magia = "light_yellow"
                elif tipo_magia == "slash":
                    colore_magia = "light_red"
                elif tipo_magia == "melee":
                    colore_magia = "light_red"
                elif tipo_magia == "cura":
                    colore_magia = "light_green"
                elif effetto == "stats":
                    colore_magia = "white"

                print("[",end="")
                print(colored(f"{tipo_magia}",colore_magia,None,["bold"]),end="")
                print("] ",end=" ")

                cosa_consuma = magia_["cosa_consuma"]
                if cosa_consuma == "hp":
                    
                    costo_magia = magia_["costo"]
                    print(colored(f" |{costo_magia}HP|","green"),end=" ")
                elif cosa_consuma == "sp":

                    costo_magia = magia_["costo"]
                    print(colored(f" |{costo_magia}SP|","magenta"),end=" ")

                nome_magia = magia_["nome"]
                print(colored(nome_magia,"light_cyan"),end="\n")

                
                
            magia_scelta = input(colored("\ninserire il numero (grigio) della magia scelta...","grey"))
            try:
                magia_scelta = int(magia_scelta)
                
            except:
                print(colored("\nrifare inserendo un valore numerico corretto...","grey"))
                aspetta_input()
                os.system(clear)
                rifai = True

            if rifai == False:
                lunghezza_lista_magie = len(lista_magie_giocatore)
                if magia_scelta > lunghezza_lista_magie or magia_scelta < 1:

                    lunghezza_lista_magie_c = colored(lunghezza_lista_magie,"light_red")
                    O_c = colored("0","light_red")

                    print(colored(f"\nrifare inserendo un valore minore di {lunghezza_lista_magie_c},","grey"),end=" ")
                    print(colored(f"o piu grande di {O_c}","grey"))
                    aspetta_input()
                    rifai = True

            
            for magia in lista_magie_giocatore:
                numero_magia = magia["posizione"]
    
                if magia_scelta == numero_magia:
                    costo_magia = magia["costo"]
                    cosa_consuma = magia["cosa_consuma"]

                    if cosa_consuma == "hp":
                        hp_rimasto = hp_giocatore - costo_magia

                        if hp_rimasto <= 0:

                            print(colored("hp insufficente...","grey"))
                            aspetta_input()
                            hp_insufficente = True
                            rifai_input = True
                        elif hp_rimasto >= 1:
                            giocatore_vivo_.update({"health":hp_rimasto})
                            break
                    elif cosa_consuma == "sp":
                        sp_rimasta = sp_giocatore - costo_magia
                        if sp_rimasta < 0:
                        
                            print(colored("sp insufficente...","grey"))
                            aspetta_input()
                            sp_insufficente = True
                            rifai_input = True
                        elif sp_rimasta >= 0:
                        
                            giocatore_vivo_.update({"sp":sp_rimasta})
                            break

        rifai = True
        while rifai == True and sp_insufficente == False and hp_insufficente == False:
            rifai = False
            raggio = magia["raggio"]
            tipo_magia = magia["type"]
            effetto = magia["effetto"]

            fonte = magia["fonte"] #determina se lo sta usando un nemico o giocatatore
            if effetto == "stats": #per le magie che manipolano le statistiche
                statistiche_buff_debuff(tipo_magia,raggio,lista_giocatori_v,lista_nemici,fonte)

            elif effetto == "magia": #per magie che fanno del danno

                lista_nemici = magie_che_tipo(fonte,tipo_magia,raggio,lista_nemici,magia,lista_giocatori_v,giocatore_vivo_)


    return lista_giocatori_v,sp_insufficente,giocatore_vivo_,lista_nemici,rifai_input


def stampa_danno(lista_nemici,lista_giocatori_v,nemico_preso,nome_nemico,chi_attaccare,damage_tot,status,giocatore_vivo_):
    os.system(clear)

    colore_nome = giocatore_vivo_["colore_nome"]
    print(colored("\\" * 69,colore_nome))
    i = -1
    print()
    for nemico in lista_nemici:
        i = i+1
        if i > 0:
            print(" " * i,end="")
        nome_nemico = nemico["name"]
        vita_nemico = nemico["health"]
        max_vita_nemico = nemico["max_health"]

        if vita_nemico < 1:
            nome_nemico_c = colored(nome_nemico,"grey")
            vita_nemico = 0
        else:
            nome_nemico_c = colored(nome_nemico,"red")
        print(nome_nemico_c,end=" ")

        print(colored(f"|{vita_nemico}","light_green"),end="/")
        if nemico["posizione"] == chi_attaccare:
            if nemico_preso == [True]:
                print(colored(f"{max_vita_nemico}|","green"),end=f" -{damage_tot}HP")

                if status == "debole":
                    print(colored("|DEBOLE|","cyan"))
                    nemico.update({"one_more":True})
                    nemico.update({"atterrato":True})
                elif status == "resiste":
                    print(colored("|RESISTE|","grey"))
                elif status == "normale":
                    print()

            else:
                print(colored(f"{max_vita_nemico}|","green"),end="")
                print(colored("|MISS|","grey"))  
        else:
            print(colored(f"{max_vita_nemico}|","green"))
                

    aspetta_input()

def attaccare(giocatore_vivo_,lista_giocatori_v,lista_nemici): 

    battaglia_vinta = False
    if lista_nemici == []: #fine battaglia (vittoria) se lista_nemici è vuota
        battaglia_vinta = True
    elif battaglia_vinta == False:
        current_equip_melee = giocatore_vivo_["current_equip_melee"]
        damage_melee = current_equip_melee["damage"] #preso il danno grezzo dalla arma equipaggiata
        damage_base_percentuale = giocatore_vivo_["damage_base"] #percentuale di danno aumentato all'arma equipaggiata che aumenta di valore livellando
        damage_percentuale = (damage_melee * damage_base_percentuale)/100
        damage_tot = damage_melee + damage_percentuale
        damage_tot = int(damage_tot) #conversione per non avere la virgola nel danno
        

        rifai_input = True
        if len(lista_nemici) == 1:
            chi_attaccare = 1

            rifai_input = False

        while rifai_input == True:
            rifai_input = False
            os.system(clear)
            i = -1
            colore_nome = giocatore_vivo_["colore_nome"]
            print(colored("\\" * 69,colore_nome),end="\n\n")
            for nemico in lista_nemici:

                i = i + 1
                if i > 0:
                    print(" " * i,end="")
                nome_nemico = nemico["name"]
                vita_nemico = nemico["health"]
                max_vita_nemico = nemico["max_health"]
                posizione = nemico["posizione"]

                print(colored(f"|{posizione}|","grey"),end=" ")
                print(colored(nome_nemico,"red"),end="")
                print(colored(f"|{vita_nemico}","light_green"),end="/")
                print(colored(f"{max_vita_nemico}|","green"))

            chi_attaccare = input("\ninserire la posizione (grigio) di chi attaccare...") #id/nome da prendere
            try:
                chi_attaccare = int(chi_attaccare)
            except:
                print(colored("rifare inserendo un valore numerico corretto(guarda il numero in grigio a sinistra del nome del nemico)...","grey"))
                aspetta_input()
                os.system(clear)
                rifai_input = True


        
        rifai = True
        
        while rifai == True:
            rifai = False
            for nemico_ in lista_nemici:
                id_nemico = nemico_["posizione"]
                nome_nemico = nemico_["name"]
                
                if chi_attaccare == id_nemico: #serve nome_,damage_tot
                    tipo_magia = "melee"
                    nemico_preso = preso_o_mancato(nemico_,tipo_magia,giocatore_vivo_)
                    nome_nemico = colored(nome_nemico,"yellow")
                    status = None
                    if nemico_preso == [True]:
                        tipo_magia_player = "slash"
                        status = debolezze(tipo_magia_player,nemico_)
                        hp_nemico = nemico_["health"]
                        atk_ = giocatore_vivo_["ATK"]
                        if atk_ == 1:
                            damage_tot = damage_tot * 1.5
                        elif atk_ == -1:
                            damage_tot = damage_tot / 1.5
                        danno_aggiorato = hp_nemico - damage_tot
                        danno_aggiorato = int(danno_aggiorato)

                        nemico_.update({"health":danno_aggiorato})
                    elif nemico_preso == [False]:
                        os.system(clear)
                        damage_tot = None

                    break
                
            if chi_attaccare != id_nemico:
                print(colored("il nemico selezionato non esite/valore non valido","grey"))
                chi_attaccare = int(input("che nemico attaccare?")) #id da prendere
                rifai = True
    if damage_tot != None:
        damage_tot = int(damage_tot)
    stampa_danno(lista_nemici,lista_giocatori_v,nemico_preso,nome_nemico,chi_attaccare,damage_tot,status,giocatore_vivo_)
    return giocatore_vivo_,lista_nemici

def preso_o_mancato(nemico_,tipo_magia,giocatore_vivo_):

    agi_nemico = nemico_["AGI"]
    nemico_velocità = nemico_["schivata"]

    agi_giocatore = giocatore_vivo_["AGI"]

    if agi_giocatore == 1: #aumenta la possibilità di schivare un attacco
        percentuale = (nemico_velocità * 30)/100
        nemico_velocità = percentuale - nemico_velocità

    elif agi_giocatore == -1: #diminuisce la possibilità di schivare un attacco
        percentuale = (nemico_velocità * 30)/100
        nemico_velocità = nemico_velocità + percentuale

    nemico_velocità_opposto = 100 - nemico_velocità


    if agi_nemico == 1: #avvantaggiata la schivata
        percentuale = (nemico_velocità * 30)/100
        nemico_velocità = percentuale + nemico_velocità

    elif agi_nemico == -1: #svantaggiata la schivata
        percentuale = (nemico_velocità * 30)/100
        nemico_velocità = nemico_velocità - percentuale
    nemico_velocità_opposto = 100 - nemico_velocità
    
    flip = True,False
    nemico_preso = random.choices(flip,weights=[nemico_velocità_opposto,nemico_velocità],k=1)
    nemico_crit = False
    nemico_atterrato = nemico_["atterrato"]

    if tipo_magia == "slash" and nemico_preso:

        crit = True,False
        possibilità_crit = giocatore_vivo_["possibilit\u00c3\u00a0_crit"]
        possibilità_crit_opposto = 100 - possibilità_crit

        if nemico_atterrato == False and nemico_preso == [True]:

            nemico_crit = random.choices(crit,weights=[possibilità_crit,possibilità_crit_opposto],k=1)
            if nemico_crit == [True]:
                nemico_.update({"crit":True})
                nemico_.update({"atterrato":True})
                
    return nemico_preso


def stampa_cure(giocatore_vivo_,lista_giocatori_v,vita_recuperata):

    os.system(clear)
    print(colored("\\" * 69,"green"))
    i = -1
    print()
    for giocatore in lista_giocatori_v:

        colore_nome = giocatore["colore_nome"]
        i = i+1
        if i > 0:
            print(" " * i,end="")
        nome_giocatore = giocatore["name"]
        vita_giocatore = giocatore["health"]
        max_vita_giocatore = giocatore["max_health"]
        nome_giocatore_c = colored(nome_giocatore,colore_nome)
        print(nome_giocatore_c,end=" ")
        print(colored(f"|{vita_giocatore}","light_green"),end="/")
        if giocatore_vivo_["posizione"] == giocatore["posizione"]:
            print(colored(f"{max_vita_giocatore}|","green"),end=" ")
            print(colored(f"+{vita_recuperata}HP","green"))
        else:
            print(colored(f"{max_vita_giocatore}|","green"))
                

    aspetta_input()

def difendersi(giocatore_vivo):

    os.system(clear)
    giocatore_vivo.update({"guard":True})

    nome = giocatore_vivo["name"]
    colore = giocatore_vivo["colore_nome"]

    giocatore_c = colored(nome,colore)

    print(f"il {giocatore_c} si sta difendendo")
    aspetta_input()
    os.system(clear)

def rimuovi_cura(lista_oggetti_zaino,cura_scelta):
    posizione_oggetto_scelto = cura_scelta["numero_nella_lista"]
    for oggetto in lista_oggetti_zaino:
        posizione_oggetto = oggetto["numero_nella_lista"]
        if posizione_oggetto == posizione_oggetto_scelto:
            lista_oggetti_zaino.remove(oggetto)
            break
    with open(p_zaino,"w") as zaino:
        json.dump(lista_oggetti_zaino,zaino,indent=4)


def curarsi(lista_giocatori_v,lista_giocatori_m):
    with open(p_zaino,"r") as lista_oggetti_zaino:
        lista_oggetti_zaino = json.load(lista_oggetti_zaino)
    rifai_input = False
    os.system(clear)
    rifai = True
    cura_scelta = None
    while cura_scelta == None:
        cura_scelta = menù_oggetti()
    
    while rifai == True:
        rifai = False
        tipo_oggetto = cura_scelta["type"]
        
        if tipo_oggetto == "hp":
            i = 0
            for giocatore in lista_giocatori_v:
                i = i+1
                if i > 1:
                    print("",end = " " * i) #crea una scaletta di spazi

                posizione_giocatore = giocatore["posizione"]
                print(colored(posizione_giocatore,"grey"),end="  ")

                nome_giocatore = giocatore["name"]
                colore_nome = giocatore["colore_nome"]
                nome_giocatore_c = colored(nome_giocatore,colore_nome)
                print(nome_giocatore_c,end=" ")

                vita_giocatore = giocatore["health"]
                print(colored(f"|{vita_giocatore}","light_green"),end="/")

                vita_max_giocatore = giocatore["max_health"]
                print(colored(f"{vita_max_giocatore}|","green"))

            rifai_input = True
            while rifai_input == True:
                rifai_input = False
                chi_curare = input("chi si vuole curare?")
                try:
                    chi_curare = int(chi_curare)
                except:
                    print(colored("rifare inserendo un valore numerico...","grey"))
                    aspetta_input()
                    os.system(clear)
                    rifai_input = True

                vita_recuperata = cura_scelta["effetto"] 
                nome_trovato = False

                for persona in lista_giocatori_v:
                    posizione_alleato = persona["posizione"]
                    if chi_curare == posizione_alleato:
                    
                        vita_persona = persona["health"]
                        vita_max = persona["max_health"]
                        vita_finale = vita_persona + vita_recuperata
                        if vita_finale > vita_max:
                            vita_finale = vita_max
                            vita_info = vita_finale
                        elif vita_finale < vita_max:
                            vita_info = vita_finale
                        persona.update({"health":vita_finale})

                        nome_giocatore = persona["name"]
                        colore_nome = persona["colore_nome"]
                        nome_persona = colored(nome_giocatore,colore_nome)
                        vita_recuperata = colored(vita_info,"green")
                        os.system(clear)
                        print(f"{nome_persona} si è curato... {vita_recuperata}/",end="")
                        print(colored(f"{vita_max} hp","light_green"))
                        aspetta_input()
                        nome_trovato = True
                        rimuovi_cura(lista_oggetti_zaino,cura_scelta)
                        break
                if nome_trovato == False:
                    print(colored("persona non trovata...\nriprovare scrivendo lettera per lettera (e maiuscole) il nome della cura\n","grey"))
                    aspetta_input()
                    rifai = True          

        elif tipo_oggetto == "sp":
            rifai = True
            while rifai == True:
                rifai = False
                tipo_oggetto = cura_scelta["type"]
                i = 0
                for giocatore in lista_giocatori_v:
                    i = i+1
                    if i > 1:
                        print("",end = " " * i) #crea una scaletta di spazi

                    posizione_giocatore = giocatore["posizione"]
                    print(colored(posizione_giocatore,"grey"),end="  ")

                    nome_giocatore = giocatore["name"]
                    colore_nome = giocatore["colore_nome"]
                    nome_giocatore_c = colored(nome_giocatore,colore_nome)
                    print(nome_giocatore_c,end=" ")

                    sp_giocatore = giocatore["sp"]
                    print(colored(f"|{sp_giocatore}","light_magenta"),end="/")

                    sp_max_giocatore = giocatore["max_sp"]
                    print(colored(f"{sp_max_giocatore}|","magenta"))

                rifai_input = True
                while rifai_input == True:
                    rifai_input = False
                    chi_curare = input("chi si vuole curare?")
                    try:
                        chi_curare = int(chi_curare)
                    except:
                        print(colored("rifare inserendo un valore numerico...","grey"))
                        aspetta_input()
                        os.system(clear)
                        rifai_input = True

                    sp_recuperata = cura_scelta["effetto"] 
                    nome_trovato = False

                    for persona in lista_giocatori_v:
                        posizione_alleato = persona["posizione"]
                        if chi_curare == posizione_alleato:
                        
                            sp_persona = persona["sp"]
                            sp_max = persona["max_sp"]
                            sp_finale = sp_persona + sp_recuperata
                            if sp_finale > sp_max:
                                sp_finale = sp_max
                                sp_info = sp_finale
                            elif sp_finale < sp_max:
                                sp_info = sp_finale
                            persona.update({"sp":sp_finale})
                            nome_giocatore = persona["name"]
                            colore_nome = persona["colore_nome"]
                            nome_persona = colored(nome_giocatore,colore_nome)
                            sp_recuperata = colored(sp_info,"magenta")
                            os.system(clear)
                            print(f"{nome_persona} ha recuperato: {sp_recuperata}/",end="")
                            print(colored(f"{sp_max} sp","light_magenta"))
                            aspetta_input()
                            nome_trovato = True
                            rimuovi_cura(lista_oggetti_zaino,cura_scelta)
                            break
                    if nome_trovato == False:
                        print(colored("persona non trovata...\nriprovare scrivendo lettera per lettera (e maiuscole) il nome della cura\n","grey"))
                        aspetta_input()
                        rifai = True          

        elif tipo_oggetto == "revive" and not lista_giocatori_m == []:
            
            i = 0
            for giocatore in lista_giocatori_m:
                i = i+1
                if i > 1:
                    print("",end = " " * i) #crea una scaletta di spazi

                posizione_giocatore = giocatore["posizione"]
                print(colored(posizione_giocatore,"grey"),end="  ")

                nome_giocatore = giocatore["name"]
                colore_nome = "red"
                nome_giocatore_c = colored(nome_giocatore,colore_nome)
                print(nome_giocatore_c,end=" ")

            rifai_input = True
            while rifai_input == True:
                
                rifai_input = False

                chi_curare = input("chi si vuole resuscitare?")
                try:
                    chi_curare = int(chi_curare)
                except:
                    print(colored("rifare inserendo un valore numerico...","grey"))
                    aspetta_input()
                    os.system(clear)
                    rifai_input = True

            vita_recuperata = cura_scelta["effetto"] 
            nome_trovato = False
            for persona in lista_giocatori_m:
                posizione_persona = persona["posizione"]
                if chi_curare == posizione_persona:
                    vita_max = persona["max_health"]

                    if vita_recuperata == "met\u00e0":
                        vita_finale = vita_max / 2
                        vita_finale = int(vita_finale)

                    elif vita_recuperata == "max":
                        vita_finale = vita_max

                    persona.update({"health":vita_finale})

                    colore_nome = persona["colore_nome"]
                    nome_persona = persona["name"]

                    nome_giocatore_c = colored(nome_persona,colore_nome)
                    vita_recuperata = colored(vita_finale,"green")

                    print(f"{nome_giocatore_c} è ora vivo... {vita_recuperata}/",end="")
                    print(colored(f"{vita_max} hp","light_green"))
                    aspetta_input()
                    nome_trovato = True
                    lista_giocatori_v.append(persona)
                    lista_giocatori_m.remove(persona)
                    rimuovi_cura(lista_oggetti_zaino,cura_scelta)

                    riordina_lista_giocatori_in_battaglia(lista_giocatori_v)
                    break
            if nome_trovato == False:
                print(colored("numero inserito non valido...\n","grey"))
                aspetta_input()
                rifai = True

        elif tipo_oggetto == "revive" and lista_giocatori_m == []:
            print(colored("tutti i giocatori sono vivi, cura non usata...","grey"))
            aspetta_input()
            rifai_input = True
            
        if rifai_input == False:
            i = 1
            for oggetto in lista_oggetti_zaino:
                oggetto.update({"numero_nella_lista":i})
                i = i + 1
            with open(p_zaino,"w") as zaino_json:
                json.dump(lista_oggetti_zaino,zaino_json,indent=4)
    return rifai_input
def name_item(lista_oggetti_zaino):
    return lista_oggetti_zaino["name"]
def menù_oggetti():
    with open(p_zaino,"r") as lista_oggetti_zaino:
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
        os.system(clear)
        finito = False

        if len(lista_oggetti_cure) > 9 and finito == False: # menù
            fare_if = True
            try:
                for i in range(9): #TODO come capire se è più lungo di 9 (se no crash programma)
                    n_attuale = i + numero_min
                    cura_attuale = lista_oggetti_cure[n_attuale]
                    if i > 1:
                        print("",end = " " * i)

                    print(colored(cura_attuale["numero_nella_lista"],"grey"),end=" ")
                    print(cura_attuale["name"],end=" ")
                    
                    effetto = cura_attuale["effetto"] 
                    type = cura_attuale["type"]
                    if type == "hp":
                        print(colored(f"+{effetto}HP","green"))
                    elif type == "sp":
                        print(colored(f"+{effetto}SP","magenta"))
                    elif type == "revive":
                        print(colored(f"resuscita un alleto con |{effetto} hp|","grey"))

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
                    if j > 0:
                        print("",end = " " * j)

                    print(colored(cura_attuale["numero_nella_lista"],"grey"),end=" ")
                    print(cura_attuale["name"],end=" ")
                    
                    effetto = cura_attuale["effetto"] 
                    type = cura_attuale["type"]
                    if type == "hp":
                        print(colored(f"+{effetto}HP","green"))
                    elif type == "sp":
                        print(colored(f"+{effetto}SP","magenta"))
                    elif type == "revive":
                        print(colored(f"resuscita un alleto con |{effetto} hp|","grey"))

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

                if a > 0:
                    print("",end = " " * a)
                print(colored(cura_attuale["numero_nella_lista"],"grey"),end=" ")
                print(cura_attuale["name"],end=" ")
                

                effetto = cura_attuale["effetto"] 
                type = cura_attuale["type"]
                if type == "hp":
                    print(colored(f"+{effetto}HP","green"))
                elif type == "sp":
                    print(colored(f"+{effetto}SP","magenta"))
                elif type == "revive":
                    print(colored(f"resuscita un alleto con |{effetto} hp|","grey"))
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

def nemico_attacco(nemico,lista_giocatori_v,nemico_nome):
    danno_nemico = nemico["damage"]
    chi_attaccare_player = random.choice(lista_giocatori_v)
    chi_attaccare_player_nome = chi_attaccare_player["name"]
    chi_attaccare_player
    tipo_magia = "melee"
    chi_attaccare_player

    atk_ = nemico["ATK"]    
    if atk_ == 1:

        danno_nemico = danno_nemico * 1.2
    if atk_ == -1:

        danno_nemico = danno_nemico / 1.2
        danno_nemico = int(danno_nemico)

    giocatore_preso = preso_o_mancato(chi_attaccare_player,tipo_magia,nemico)
    if giocatore_preso == [True]:
        for giocatore in lista_giocatori_v:
            nome_giocatore = giocatore["name"]

            if nome_giocatore == chi_attaccare_player_nome:
                tipo_magia_player = "slash"
                status = debolezze(tipo_magia_player,giocatore)
                if status == "resiste":
                    danno_nemico = danno_nemico / 1.3
                elif status == "debole":
                    atterrato = chi_attaccare_player["atterrato"]
                    danno_nemico = danno_nemico * 1.3

                    if atterrato == False:
                        chi_attaccare_player.update({"one_more":True})
                        chi_attaccare_player.update({"atterrato":True})

                vita_player = giocatore["health"]
                parata_attiva = giocatore["guard"]

                if parata_attiva == True:
                    danno_nemico = int(danno_nemico / 2.1)

                armatura = giocatore["armatura"]
                def_ = giocatore["DEF"]

                if def_ == 1:
                    armatura = giocatore["armatura"]

                    percentuale = (armatura * 20)/100
                    armatura = armatura + percentuale
                if def_ == -1:
                    armatura = giocatore["armatura"]

                    percentuale = (armatura * 20)/100
                    armatura = armatura - percentuale
                        
                danno_tot = danno_nemico / armatura
                danno_tot = int(danno_tot)
                vita_player = vita_player - danno_tot

                vita_player = int(vita_player)
                for giocatore_ in lista_giocatori_v:
                    def_ = giocatore_["DEF"]

                nome = giocatore["name"]
                colore_nome = giocatore["colore_nome"]
                nemico_nome_c = colored(nemico_nome,"red") 
                player_vivo_nome_c = colored(nome,colore_nome)
                danno_tot_c = colored(danno_tot,"red")
                os.system(clear)
                print(colored("/" * 69,"red"))
                print(colored(f"il nemico {nemico_nome_c}","grey"),end=" ") 
                print(colored(f"ha inflitto -{danno_tot_c}HP","grey"),end=" ")
                print(colored(f"al {player_vivo_nome_c}","grey"))
                giocatore.update({"health":vita_player})
                aspetta_input()

                break
    elif giocatore_preso == [False]:
        nome = chi_attaccare_player["name"]
        colore_nome = chi_attaccare_player["colore_nome"]
        nemico_nome_c = colored(nemico_nome,"red") 
        player_vivo_nome_c = colored(nome,colore_nome)

        os.system(clear)
        print(colored("/" * 69,"red"))
        print(colored(f"il nemico {nemico_nome_c}","grey"),end=" ") 
        print(colored(f"ha mancato {player_vivo_nome_c}","grey"),end=" ")
        aspetta_input()

def posizione(lista_giocatori):
    return lista_giocatori["posizione"]

def riordina_lista_giocatori_in_battaglia(lista_giocatori_v):
    lista_giocatori_v.sort(key=posizione)
    return lista_giocatori_v

def riordina_lista_giocatori_fuori_battaglia(lista_giocatori):
    lista_giocatori.sort(key=posizione)
    return lista_giocatori

def AI_nemico(nemico,lista_nemici,lista_giocatori_v,numero_piano,lista_giocatori_m):

    
    giocatori_morti = False

    nemico.update({"atterrato":False})
    nemico.update({"one_more":False})

    if lista_giocatori_v == []:
        giocatori_morti = True
        
    if giocatori_morti == False:
        nemico_nome = colored(nemico["name"],"light_red")

        numero_piano = 5
        if numero_piano <= 2: #se i nemici si trovano al piano 2 o inferiore attaccheranno e basta
            nemico_attacco(nemico,lista_giocatori_v,nemico_nome)

        elif numero_piano == 2 or numero_piano == 3 or numero_piano == 4:
            scelta_magia = "attacco","magie","buff_stats"
            nemico_nome = nemico["name"]
            scelta_magia = random.choices(scelta_magia,weights=[50,40,10],k=1)
            giocatore_da_attaccare = random.choice(lista_giocatori_v)

            rifai_random = True
            fai_magie = False
            while rifai_random == True:
                rifai_random = False
                
                if fai_magie == True:
                    scelta_magia = "magie"
                    fai_magie = False

                if scelta_magia == ["magie"]:
                    #magie
                    lista_magie_nemico = nemico["magie"]
                    lista_magie_nemico_magia = []
                    for magie in lista_magie_nemico:
                        if magie["effetto"] == ["magia"]:
                            lista_magie_nemico_magia.append(magie)
                        rifai = False
                    random.shuffle(lista_magie_nemico_magia)
                    che_magia_usare = random.choice(lista_magie_nemico_magia)

                    percentuale_boost_potenza_magie = nemico["danno_magie"]
                    tipo_magia_nemico = che_magia_usare["type"]
                    danno_inflitto = magie_funzionamento(percentuale_boost_potenza_magie,che_magia_usare,giocatore_da_attaccare)

                    status = debolezze(tipo_magia_nemico,giocatore_da_attaccare)

                    if giocatore_da_attaccare["DEF"] == 1:
                        danno_inflitto = danno_inflitto / 1.2
                        
                    elif giocatore_da_attaccare["DEF"] == -1:
                        danno_inflitto = danno_inflitto * 1.2

                    if nemico["ATK"] == 1:
                        danno_inflitto = danno_inflitto * 1.2
                    elif nemico["ATK"] == -1:
                        danno_inflitto = danno_inflitto / 1.2

                    if status == "debole":
                        giocatore_da_attaccare.update({"one_more":True})
                        giocatore_da_attaccare.update({"atterrato":True})
                        danno_inflitto = danno_inflitto * 1.2
                    elif status == "resiste":
                        danno_inflitto = danno_inflitto / 1.2

                    danno_inflitto = int(danno_inflitto)

                    vita_giocatore = giocatore_da_attaccare["health"]
                    tot = vita_giocatore - danno_inflitto
                    danno_inflitto_c = colored(danno_inflitto,"red")
                    nome_giocatore_scelto = giocatore_da_attaccare["name"]
                    colore_nome = giocatore_da_attaccare["colore_nome"]
                    che_magia_usare_nome = che_magia_usare["nome"]

                    nemico_nome_c = colored(nemico_nome,"red")
                    nome_giocatore_scelto_c = colored(nome_giocatore_scelto,colore_nome)
                    che_magia_usare_nome_c = colored(che_magia_usare_nome,"cyan")
                    os.system(clear)
                    print(colored("/" * 69,"light_red"))
                    print(colored(f"il nemico {nemico_nome_c},","grey"),end=" ")
                    print(colored(f"ha usato: |{che_magia_usare_nome_c}|","grey"),end="")
                    print(colored(f"\n\ninfliggendo -{danno_inflitto_c}HP","grey"),end=" ")
                    print(colored(f"al {nome_giocatore_scelto_c}","grey"))
                    aspetta_input()
                    giocatore_da_attaccare.update({"health":tot})

                elif scelta_magia == ["attacco"]:
                    nemico_attacco(nemico,lista_giocatori_v,nemico_nome)

                elif scelta_magia == ["buff_stats"]:
                    lista_magie_nemico = nemico["magie"]
                    lista_magie_nemico_buff = []
                    for magie in lista_magie_nemico:
                        print(magie["effetto"])
                        if magie["effetto"] == "stats":
                            lista_magie_nemico_buff.append(magie)
                    aspetta_input()
                    cosa_buffare = random.choice(lista_magie_nemico_buff)
                    tipo_magia = cosa_buffare["type"]
                    for nemico_ in lista_nemici:
                        stat_buff_funzionamento(nemico_,tipo_magia,None)

        elif numero_piano == 5:
            nemico_nome = nemico["name"]

            rifai_random = True
            
            while rifai_random == True:
                rifai_random = False
                fai_magie = False
                scelta_magia = "magie","buff_stats","cura"
                scelta_magia = random.choices(scelta_magia,weights=[50,30,20],k=1)
                giocatore_da_attaccare = random.choice(lista_giocatori_v)
                if fai_magie == True:
                    scelta_magia = "magie"

                if scelta_magia == ["magie"]:
                    #magie
                    lista_magie_nemico_magia = []

                    lista_magie__ = nemico["magie"]
                    for magia in lista_magie__:
                        if magia["effetto"] == "magia":
                            lista_magie_nemico_magia.append(magia)
                    random.shuffle(lista_magie_nemico_magia)
                    che_magia_usare = random.choice(lista_magie_nemico_magia)
                    percentuale_boost_potenza_magie = nemico["danno_magie"]
                    tipo_magia_nemico = che_magia_usare["type"]

                    danno_inflitto = magie_funzionamento(percentuale_boost_potenza_magie,che_magia_usare,giocatore_da_attaccare)
                    nemico_preso = preso_o_mancato(giocatore_da_attaccare,tipo_magia_nemico,nemico)
                    status = debolezze(tipo_magia_nemico,giocatore_da_attaccare)
                    if nemico_preso == [True]:
                        if giocatore_da_attaccare["DEF"] == 1:
                            danno_inflitto = danno_inflitto / 1.2
                            danno_inflitto = int(danno_inflitto)

                        elif giocatore_da_attaccare["DEF"] == -1:
                            danno_inflitto = danno_inflitto * 1.2
                            danno_inflitto = int(danno_inflitto)

                        if nemico["ATK"] == 1:
                            danno_inflitto = danno_inflitto * 1.2
                            danno_inflitto = int(danno_inflitto)
                        elif nemico["ATK"] == -1:
                            danno_inflitto = danno_inflitto / 1.2
                            danno_inflitto = int(danno_inflitto)

                        if status == "debole":
                            giocatore_da_attaccare.update({"one_more":True})
                            giocatore_da_attaccare.update({"atterrato":True})
                            danno_inflitto = danno_inflitto * 1.2
                        elif status == "resiste":
                            danno_inflitto = danno_inflitto / 1.2

                        danno_inflitto = int(danno_inflitto)

                        vita_giocatore = giocatore_da_attaccare["health"]
                        tot = vita_giocatore - danno_inflitto
                        danno_inflitto_c = colored(danno_inflitto,"red")
                        nome_giocatore_scelto = giocatore_da_attaccare["name"]
                        colore_nome = giocatore_da_attaccare["colore_nome"]
                        che_magia_usare_nome = magia["nome"]

                        nemico_nome_c = colored(nemico_nome,"red")
                        nome_giocatore_scelto_c = colored(nome_giocatore_scelto,colore_nome)
                        che_magia_usare_nome_c = colored(che_magia_usare_nome,"cyan")

                        os.system(clear)
                        print(colored("/" * 69,"light_red"))
                        print(colored(f"il nemico {nemico_nome_c},","grey"),end=" ")
                        print(colored(f"ha usato: |{che_magia_usare_nome_c}|","grey"),end="")
                        print(colored(f"\n\ninfliggendo -{danno_inflitto_c}HP","grey"),end=" ")
                        print(colored(f"al {nome_giocatore_scelto_c}","grey"))
                        aspetta_input()
                        giocatore_da_attaccare.update({"health":tot})
                    else:
                        nome_giocatore_scelto = giocatore_da_attaccare["name"]
                        colore_nome = giocatore_da_attaccare["colore_nome"]
                        nemico_nome_c = colored(nemico_nome,"red")
                        nome_giocatore_scelto_c = colored(nome_giocatore_scelto,colore_nome)
                        os.system(clear)
                        print(colored("/" * 69,"light_red"))
                        print(colored(f"il nemico {nemico_nome_c},","grey"),end=" ")
                        print(colored(f"ha mancato {nome_giocatore_scelto_c}","grey"))
                        aspetta_input()

                elif scelta_magia == ["buff_stats"]:
                    lista_magie_nemico_buff = []
                    lista_magie = nemico["magie"]
                    for magia in lista_magie:
                        if magia["effetto"] == "stats":
                            lista_magie_nemico_buff.append(magia)
                    try:
                        cosa_buffare = random.choice(lista_magie_nemico_buff)
                    except:
                        fai_magie = True
                    if fai_magie == False:
                        tipo_magia_ = cosa_buffare["type"]
                        for nemico_ in lista_nemici:
                            stat_buff_funzionamento(nemico_,tipo_magia_,lista_giocatori_v)

                elif scelta_magia == ["cura"]:
                    lista_magie_nemico = nemico["magie"]
                    lista_magie_nemico_cura = []
                    for magie in lista_magie_nemico:
                        if magie["effetto"] == "cura":
                            lista_magie_nemico_cura.append(magie)
                        try:
                            fai_magie = False
                            magia = random.choice(lista_magie_nemico_cura)
                        except:
                            rifai_random = True
                            fai_magie = True
                        if fai_magie == False:
                            _ = 0
                            j = 0
                            i = -1
                            for nemico__ in lista_nemici:
                                _ = _ +1 
                                nemico.update({"posizione":_})

                                vita_nemico = nemico["health"]
                                vita_nemico_max = nemico["max_health"]
                                percentuale_boost_potenza_magie = 1
                                vita_curata = magie_funzionamento(percentuale_boost_potenza_magie,magia,nemico)

                                tot = vita_nemico + vita_curata
                                if tot > vita_nemico_max:
                                    tot = vita_nemico

                                os.system(clear)
                                print(colored("/" * 69,"red"))
                                print()
                                j = j+1
                                vita_nemico_ = nemico__["health"]
                                vita_nemico_max_ = nemico__["max_health"]
                                i = i+1
                                if i > 0:
                                    print(" " * i,end="")
                                nome_nemico = nemico__["name"]
                                nome_nemico_c = colored(nome_nemico,"red")
                                print(nome_nemico_c,end=" ")

                                print(colored(f"|{vita_nemico_}","light_green"),end="/")

                                if nemico["posizione"] == j:
                                    vita_curata_c = colored(vita_curata,"green")
                                    print(colored(f"{vita_nemico_max_}|","green"),end=f" +{vita_curata_c}HP\n")
                                else:
                                    print(colored(f"{vita_nemico_max_}|","green"),end="\n")
                                nemico.update({"health":tot})
                                aspetta_input()

    for giocatore in lista_giocatori_v:
        vita_player = giocatore["health"]
        if vita_player <= 0:
            
            lista_giocatori_m.append(giocatore)
            lista_giocatori_v.remove(giocatore)

            print(colored("il","red"),end=" ")
            print(colored(giocatore["name"],"cyan"),end=" ")
            print(colored("è morto","red"),end="\n")
            aspetta_input()

    return lista_giocatori_v,lista_giocatori_m

def stat_buff_funzionamento(giocatore_vivo_,tipo_magia,lista_giocatori_v):

    if tipo_magia == "ATK UP":
        
        atk_ = giocatore_vivo_["ATK"]
        if atk_ == 1:
            atk_ = 1
            
        elif atk_ != 1:
            atk_ =+ 1
            
        s_ATK = 3
        giocatore_vivo_.update({"s_ATK":s_ATK})
        giocatore_vivo_.update({"ATK":atk_})

    elif tipo_magia == "DEF UP":
        def_ = giocatore_vivo_["DEF"]
        if def_ == 1:
            def_ = 1
        elif def_ != 1:
            def_ =+ 1
        s_DEF = 3
        giocatore_vivo_.update({"s_DEF":s_DEF})
        giocatore_vivo_.update({"DEF":def_})

    elif tipo_magia == "AGI UP":
        agi_ = giocatore_vivo_["AGI"]
        if agi_ == 1:
            agi_ = 1
        elif agi_ != 1:
            agi_ =+ 1
        s_AGI = 3
        giocatore_vivo_.update({"s_AGI":s_AGI})
        giocatore_vivo_.update({"AGI":agi_})

    elif tipo_magia == "CRIT UP":
        crit_ = giocatore_vivo_["CRIT"]
        if crit_ == 1:
            crit_ = 1
        elif crit_ != 1:
            crit_ =+ 1
        s_CRIT = 3
        giocatore_vivo_.update({"s_CRIT":s_CRIT})
        giocatore_vivo_.update({"CRIT":crit_})
    if tipo_magia == "ATK DOWN" or tipo_magia == "DEF DOWN" or tipo_magia == "AGI DOWN" or tipo_magia == "ccrit DOWN":
        for giocatore in lista_giocatori_v:
            if tipo_magia == "ATK DOWN":
                atk_ = giocatore["ATK"]
                if atk_ == -1:
                    atk_ = -1

                elif atk_ != -1:
                    atk_ =+ -1

                s_ATK = 3
                giocatore.update({"s_ATK":s_ATK})
                giocatore.update({"ATK":atk_})

            elif tipo_magia == "DEF DOWN":
                def_ = giocatore["DEF"]
                if def_ == -1:
                    def_ = -1
                elif def_ != -1:
                    def_ =+ -1
                s_DEF = 3
                giocatore.update({"s_DEF":s_DEF})
                giocatore.update({"DEF":def_})

            elif tipo_magia == "AGI DOWN":
                agi_ = giocatore["AGI"]
                if agi_ == -1:
                    agi_ = -1
                elif agi_ != -1:
                    agi_ =+ -1
                s_AGI = 3
                giocatore.update({"s_AGI":s_AGI})
                giocatore.update({"AGI":agi_})

            if tipo_magia == "CRIT DOWN":
                crit_ = giocatore["CRIT"]
                if crit_ == -1:
                    crit_ = -1
                elif crit_ != -1:
                    crit_ =+ -1
                s_CRIT = 3
                giocatore.update({"s_CRIT":s_CRIT})
                giocatore.update({"CRIT":crit_})


def statistiche_buff_debuff(tipo_magia,raggio,lista_giocatori_v,lista_nemici,fonte):
    if fonte == "giocatore":
        if raggio == "singolo":
            i = 0
            for giocatore in lista_giocatori_v:
                i = i+1
                if i > 1:
                    print("",end = " " * i) #crea una scaletta di spazi

                posizione_giocatore = giocatore["posizione"]
                print(colored(posizione_giocatore,"grey"),end="  ")

                nome_giocatore = giocatore["name"]
                colore_nome = giocatore["colore_nome"]

                nome_giocatore_c = colored(nome_giocatore,colore_nome)
                print(nome_giocatore_c,end=" ")

                vita_giocatore = giocatore["health"]
                print(colored(f"|{vita_giocatore}","light_green"),end="/")

                vita_max_giocatore = giocatore["max_health"]
                print(colored(f"{vita_max_giocatore}|","green"))

            rifai = True
            while rifai == True:

                rifai = False
                chi_curare = input("chi potenziare?")
                try:
                    chi_curare = int(chi_curare)
                except:
                    print(colored("rifare inserendo un valore numerico...","grey"))
                    aspetta_input()
                    os.system(clear)
                    rifai = True

            for giocatore_vivo_ in lista_giocatori_v:
                posizione_giocatore = giocatore_vivo_["posizione"]

                if chi_curare == posizione_giocatore:
                    stat_buff_funzionamento(giocatore_vivo_,tipo_magia,None)
                    break
                
        elif raggio == "gruppo":
            for giocatore in lista_giocatori_v:
                stat_buff_funzionamento(giocatore,tipo_magia,None)


    elif fonte == "nemici":
        if raggio == "singolo":
            i = 0
            for giocatore in lista_giocatori_v:
                i = i+1
                if i > 1:
                    print("",end = " " * i) #crea una scaletta di spazi

                posizione_giocatore = giocatore["posizione"]
                print(colored(posizione_giocatore,"grey"),end="  ")

                nome_giocatore = giocatore["name"]
                colore_nome = giocatore["colore_nome"]

                nome_giocatore_c = colored(nome_giocatore,colore_nome)
                print(nome_giocatore_c,end=" ")

                vita_giocatore = giocatore["health"]
                print(colored(f"|{vita_giocatore}","light_green"),end="/")

                vita_max_giocatore = giocatore["max_health"]
                print(colored(f"{vita_max_giocatore}|","green"))

            rifai = True
            while rifai == True:
            
                rifai = False
                chi_curare = input("chi potenziare?")
                try:
                    chi_curare = int(chi_curare)
                except:
                    print(colored("rifare inserendo un valore numerico...","grey"))
                    os.system(clear)
                    rifai = True

            for giocatore_vivo_ in lista_giocatori_v:
                posizione_giocatore = giocatore_vivo_["posizione"]

                if chi_curare == posizione_giocatore:
                

                    break
                
        elif raggio == "gruppo":
            pass



def magie_che_tipo(fonte,tipo_magia,raggio,lista_nemici,magia,lista_giocatori_v,giocatore_vivo_):
    if fonte == "giocatore":
        danno_magie = giocatore_vivo_["danno_magie"]
        danno_magie = int(danno_magie)
        danno_inflitto = int(danno_magie)
        if not tipo_magia == "cura":

            if raggio == "singolo":
                rifai = True
                os.system(clear)
                if len(lista_nemici) == 1:
                    chi_attaccare = 1
                    rifai = False
                while rifai == True:
                    colore_nome = giocatore_vivo_["colore_nome"]
                    print(colored("\\" * 69,colore_nome))
                    i = 0
                    for nemico in lista_nemici:
                        i = i+1
                        if i > 1:
                            print("",end = " " * i) #crea una scaletta di spazi

                        nome_nemico = nemico["name"]
                        posizione_nemico = nemico["posizione"]
                        posizione_nemico_c = colored(f"|{posizione_nemico}|","grey")
                        print(posizione_nemico_c,end=" ")
                        nome_nemico_c = colored(nome_nemico,"red")
                        print(nome_nemico_c,end=" ")

                        vita_nemico = nemico["health"]
                        print(colored(f"|{vita_nemico}","light_green"),end="/")

                        vita_max_nemico = nemico["max_health"]
                        print(colored(f"{vita_max_nemico}|","green"))


                    rifai = False
                    chi_attaccare = input("che nemico attaccare?") #id/nome da prendere
                    try:
                        chi_attaccare = int(chi_attaccare)
                    except:
                        print(colored("rifare inserendo un valore numerico...","grey"))
                        aspetta_input()
                        os.system(clear)
                        rifai = True

                for nemico_ in lista_nemici:
                    id_nemico = nemico_["posizione"]
                    nome_nemico = nemico_["name"]

                    if chi_attaccare == id_nemico: #serve nome_,damage_tot
                            nemico_preso = preso_o_mancato(nemico_,tipo_magia,giocatore_vivo_)
                            nome_nemico = colored(nome_nemico,"yellow")
                            if nemico_preso == [True]:
                                tipo_magia = magia["type"]
                                status = debolezze(tipo_magia,nemico_)
                                if nemico_["DEF"] == 1:
                                    danno_inflitto = danno_inflitto / 1.2
                                elif nemico_["DEF"] == -1:
                                    danno_inflitto = danno_inflitto * 1.2

                                if nemico_["ATK"] == 1:
                                    danno_inflitto = danno_inflitto * 1.2
                                elif nemico_["ATK"] == -1:
                                    danno_inflitto = danno_inflitto / 1.2

                                if status == "debole":
                                    nemico_.update({"one_more":True})
                                    nemico_.update({"atterrato":True})
                                    danno_inflitto = danno_inflitto * 1.2
                                elif status == "resiste":
                                    danno_inflitto = danno_inflitto / 1.2

                                danno_inflitto = int(danno_inflitto)
                                percentuale_boost_potenza_magie = giocatore_vivo_["danno_magie"]

                                atk_ = giocatore_vivo_["ATK"]
                                if atk_ == 1:
                                    percentuale_boost_potenza_magie = percentuale_boost_potenza_magie * 1.2
                                    percentuale_boost_potenza_magie = int(percentuale_boost_potenza_magie)
                                elif atk_ == -1:
                                    percentuale_boost_potenza_magie = percentuale_boost_potenza_magie / 1.2
                                    percentuale_boost_potenza_magie = int(percentuale_boost_potenza_magie)

                                danno_inflitto = magie_funzionamento(percentuale_boost_potenza_magie,magia,nemico_)
                                vita_nemico = nemico_["health"]
                                vita_rimasta_nemico = vita_nemico - danno_inflitto
                                nemico_.update({"health":vita_rimasta_nemico})

                            elif nemico_preso == [False]:
                                danno_inflitto = None
                                status = None
                            break
                if chi_attaccare != id_nemico:
                    rifai = True
                if danno_inflitto != None:
                    danno_inflitto = int(danno_inflitto)
                stampa_danno(lista_nemici,lista_giocatori_v,nemico_preso,nome_nemico,chi_attaccare,danno_inflitto,status,giocatore_vivo_)
            elif raggio == "gruppo":

                i = 0

                for nemico in lista_nemici:
                    danno_magie = giocatore_vivo_["danno_magie"]
                    danno_magie = int(danno_magie)
                    danno_inflitto = int(danno_magie)
                    i = i + 1
                    nome_nemico = nemico["name"]
                    nemico_preso = preso_o_mancato(nemico,tipo_magia,giocatore_vivo_)
                    if nemico_preso == [True]:
                        status = debolezze(tipo_magia,nemico)
                        danno_inflitto = int(danno_inflitto)
                        if nemico["DEF"] == 1:
                            danno_inflitto = danno_inflitto / 1.2
                            danno_inflitto = int(danno_inflitto)
                        elif nemico["DEF"] == -1:
                            danno_inflitto = danno_inflitto * 1.2
                            danno_inflitto = int(danno_inflitto)
    
                        if nemico["ATK"] == 1:
                            danno_inflitto = danno_inflitto * 1.2
                            danno_inflitto = int(danno_inflitto)
                        elif nemico["ATK"] == -1:
                            danno_inflitto = danno_inflitto / 1.2
                            danno_inflitto = int(danno_inflitto)
    
                        if status == "debole":
                            danno_inflitto = int(danno_inflitto)
                            danno_inflitto = danno_inflitto * 1.2
                            danno_inflitto = int(danno_inflitto)
                        elif status == "resiste":
                            danno_inflitto = danno_inflitto / 1.2
                            danno_inflitto = int(danno_inflitto)
    
                        percentuale_boost_potenza_magie = giocatore_vivo_["danno_magie"]
                        
                        atk_ = giocatore_vivo_["ATK"]
                        if atk_ == 1:
                            percentuale_boost_potenza_magie = percentuale_boost_potenza_magie * 1.2
                            percentuale_boost_potenza_magie = int(percentuale_boost_potenza_magie)
                        elif atk_ == -1:
                            percentuale_boost_potenza_magie = percentuale_boost_potenza_magie / 1.2
                            percentuale_boost_potenza_magie = int(percentuale_boost_potenza_magie)
    
                        danno_inflitto = magie_funzionamento(percentuale_boost_potenza_magie,magia,nemico)
                        vita_nemico = nemico["health"]
                        vita_rimasta_nemico = vita_nemico - danno_inflitto
                        nemico.update({"health":vita_rimasta_nemico})
    
                    elif nemico_preso == [False]:
                        danno_inflitto = None
                        status = None
                    if danno_inflitto != None:
                        danno_inflitto = int(danno_inflitto)
                    stampa_danno(lista_nemici,lista_giocatori_v,nemico_preso,nome_nemico,i,danno_inflitto,status,giocatore_vivo_)
        elif tipo_magia == "cura":
            if raggio == "singolo":
                i = 0
                for giocatore in lista_giocatori_v:
                    i = i+1
                    if i > 1:
                        print("",end = " " * i) #crea una scaletta di spazi

                    posizione_giocatore = giocatore["posizione"]
                    print(colored(posizione_giocatore,"grey"),end="  ")

                    nome_giocatore = giocatore["name"]
                    colore_nome = giocatore["colore_nome"]

                    nome_giocatore_c = colored(nome_giocatore,colore_nome)
                    print(nome_giocatore_c,end=" ")

                    vita_giocatore = giocatore["health"]
                    print(colored(f"|{vita_giocatore}","light_green"),end="/")

                    vita_max_giocatore = giocatore["max_health"]
                    print(colored(f"{vita_max_giocatore}|","green"))

                rifai = True
                while rifai == True:
                    
                    rifai = False
                    chi_curare = input("chi si vuole curare?")
                    try:
                        chi_curare = int(chi_curare)
                    except:
                        print(colored("rifare inserendo un valore numerico...","grey"))
                        aspetta_input()
                        os.system(clear)
                        rifai = True

                for giocatore_vivo_ in lista_giocatori_v:
                    posizione_giocatore = giocatore_vivo_["posizione"]

                    if chi_curare == posizione_giocatore:
                        percentuale_boost_potenza_magie = 1
                        nemico = None
                        danno_inflitto = magie_funzionamento(percentuale_boost_potenza_magie,magia,nemico)

                        vita_giocatore = giocatore_vivo_["health"]
                        vita_max_giocatore = giocatore_vivo_["max_health"]

                        vita_curata = danno_inflitto
                        vita_curata_ = vita_curata + vita_giocatore
                        if vita_curata_ > vita_max_giocatore:
                            vita_curata_ = vita_max_giocatore
                        stampa_cure(giocatore_vivo_,lista_giocatori_v,vita_curata)
                        giocatore_vivo_.update({"health":vita_curata_})
                        break
                        
            elif raggio == "gruppo":

                for giocatore_vivo_ in lista_giocatori_v:
                
                    percentuale_boost_potenza_magie = 1
                    nemico = None
                    danno_inflitto = magie_funzionamento(percentuale_boost_potenza_magie,magia,nemico)

                    vita_giocatore = giocatore_vivo_["health"]
                    vita_max_giocatore = giocatore_vivo_["max_health"]

                    vita_curata = danno_inflitto
                    vita_curata_ = vita_curata + vita_giocatore
                    if vita_curata_ > vita_max_giocatore:
                        vita_curata_ = vita_max_giocatore
                    colore_nome = giocatore_vivo_["colore_nome"]
                    stampa_cure(giocatore_vivo_,lista_giocatori_v,vita_curata)
                    giocatore_vivo_.update({"health":vita_curata_})
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
    for giocatore_ in lista_giocatori_v:
        atk_ = giocatore_["ATK"]
        if atk_ == 1:
            giocatore_vivo_.update({"danno_magie":danno_magie})
    return lista_nemici

def tutorial():
    os.system(clear)
    lista_nemici = [
        {
        "name": "SHADOW",
        "max_health": 220,
        "health": 220,
        "schivata": 10.0,
        "one_more": False,
        "atterrato": False,
        "crit": False,
        "possibilit\u00c3\u00a0_crit":20,
        "danno_magie": 3.2,
        "debole": [
            "fire",
            "elettric"
        ],
        "resiste": [
            "ice"
        ],
        "magie": [
            {
                "nome": "ghiaccio SINGOLO",
                "potenza": "scarsa",
                "type": "ice",
                "raggio": "singolo",
                "effetto": "magia",
                "costo": 2
            }
        ],
        "exp_drop": 3,
        "damage": 180,
        "quanti_tab": 11,
        "ATK": 0,
        "DEF": 0,
        "AGI": 0,
        "s_ATK": 0,
        "s_DEF": 0,
        "s_AGI": 0
        },
        {
        "name": "SHADOW",
        "max_health": 220,
        "health": 220,
        "schivata": 10.0,
        "one_more": False,
        "atterrato": False,
        "crit": False,
        "possibilit\u00c3\u00a0_crit":20,
        "danno_magie": 3.2,
        "debole": [
            "fire",
            "elettric"
        ],
        "resiste": [
            "ice"
        ],
        "magie": [
            {
                "nome": "ghiaccio SINGOLO",
                "potenza": "scarsa",
                "type": "ice",
                "raggio": "singolo",
                "effetto": "magia",
                "costo": 2
            }
        ],
        "exp_drop": 3,
        "damage": 180,
        "quanti_tab": 11,
        "ATK": 0,
        "DEF": 0,
        "AGI": 0,
        "s_ATK": 0,
        "s_DEF": 0,
        "s_AGI": 0
    }]
    print("benvenuto nel tutorial...\nqui verranno spiegate brevemente le basi per il funzionamento del gioco.")
    aspetta_input()
    os.system(clear)
    print("|",end="")
    print(colored("ATK ","red"),end="")
    print(colored("DEF ","blue"),end="")
    print(colored("AGI","green"),end="")
    print("|",end="\n\n")
    atk_ = colored("ATK","red")
    def_ = colored("DEF","blue")
    agi_ = colored("AGI","green")
    print("queste statistiche indicano lo stato della squadra,\n")
    print(f"{atk_} questa statistica influisce sulla quantità di danni inflitti (attacco)")
    print(f"{def_} questa statistica influisce sui danni ricevuti dai nemici (difesa)")
    print(f"{agi_} questa statistica influisce sulla possibilità di mandare a segno un colpo/schivare un attacco nemico (agilità)\n\n se le statistiche avranno il simbolo \"^\" si avrà la suddetta statistica migliorata\n\nesempio:")
    print(colored("|^ATK|","red"))
    aspetta_input()
    os.system(clear)
    SP = colored("SP","magenta")
    print(f"giocatore ... |22/22|{SP}\n")
    CURA = colored("CURA","cyan",'on_black', ['bold', 'blink'])
    print(f"l'{SP} viene usato per fare le magie, più una magia è potente più {SP} costerà.\nper usare magie in caso di {SP} troppo basso, basta andare nel menù {CURA} e scegliere il denterminato giocatore scegliendo una cura per gli {SP}")
    aspetta_input()
    os.system(clear)
    Art = text2art("o n e  m o r e",font="sub-zero")
    print(colored(Art,"blue"))
    print("l'effetto ONE MORE si applica quando si colpisce un nemico con la sua debolezza,\nse il nemico è atterrato (in tale caso il nome del nemico sarà in grigio)\nnon sarà possibile fare one more.\n\nl'effetto di ONE MORE farà fare un turno BONUS in più al giocatore/nemico che lo ha causato")
    aspetta_input()
    os.system(clear)
    Art = text2art("o n e  m o r e",font="sub-zero")
    print(colored(Art,"red"))
    print("se il ONE MORE è ROSSO significa che il nemico ha causato un one more quindi attaccherà una volta in più")
    aspetta_input()
    os.system(clear)
    print("per selezione qualcosa nei vari menù basta scrivere il numero (in grigio)\nper eseguire l'azione che si vuole compiere e poi premere invio")
    
    
