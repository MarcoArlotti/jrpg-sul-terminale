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
    with open("json_data/oggetti_curativi.json","r") as lista_oggetti_curativi:
        lista_oggetti_curativi = json.load(lista_oggetti_curativi)
        rifai = True
        while rifai == True:
            rifai = False
            cura_scelta = str(input(colored("scelgiere scrivendo il nome dell'oggetto... ","grey")))
            cura_trovata = False
            for cura in lista_oggetti_curativi:
                cura_ = cura["name"]

                if cura_scelta == cura_:
                
                    print(cura_)
                    info = colored("inserire il nome...","grey")
                    chi_curare = str(input(f"chi si vuole curare?\n{info} "))
                    vita_recuperata = cura["effetto"] 
                    nome_trovato = False
                    cura_trovata = False
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
                        
                    cura_trovata = True

            if cura_trovata == False:
                print(colored("cura non trovata...\nriprovare scrivendo lettera per lettera (e maiuscole) il nome della cura\n","grey"))
                rifai = True
    #return lista_oggetti(- cura_scelta)


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