import json
import random
from termcolor import colored
def aspetta_input():
    a = input(colored("press return to continuee...","grey"))

def fuoco(potenza,persona_v): #fuoco ad attacco debole,medio,pesante,area
    pass
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
def difendersi(giocatore_vivo):
    giocatore_vivo.update({"guard":True})
    guard = giocatore_vivo["guard"]
    giocatore = giocatore_vivo["name"]
    giocatore = colored(giocatore,"light_cyan")
    print(f"il giocatore {giocatore} si sta difendendo")
    aspetta_input()
def curarsi(cura_scelta,lista_giocatori_v):
    with open("json_data/oggetti_curativi.json","r") as lista_oggetti_curativi:
        lista_oggetti_curativi = json.load(lista_oggetti_curativi)

    for cura in lista_oggetti_curativi:
        cura_ = cura["name"]

        if cura_scelta == cura_:

            print(cura_)
            info = colored("inserire il nome...","grey")
            chi_curare = str(input(f"chi si vuole curare?\n{info} "))
            vita_recuperata = cura["effetto"] 
            for persona in lista_giocatori_v:
                nome_persona = persona["name"]
                if chi_curare == nome_persona:
                    vita = persona["health"]
                    vita_finale = vita + vita_recuperata
                    persona.update({"health":vita_finale})
                    nome_persona = colored(nome_persona,"cyan")
                    vita_recuperata = colored(vita_recuperata,"green")
                    print(f"{nome_persona} si è curato di {vita_recuperata} hp") #TODO fare in modo di non aggiungere vita massima in più curandosi
                    break

