'''
pip install requests ics bs4
'''

import requests
from ics import Calendar
from bs4 import BeautifulSoup


# edt salles univ angers (fac science): https://edt.univ-angers.fr/edt/ressources?id=s9FDC055BB1C34F92E0530100007F467B

# racine des ICS: webcal://edt.univ-angers.fr/edt/ics?id= ...
# exemple d'un lien ics (Amphi A): webcal://edt.univ-angers.fr/edt/ics?id=S9F8A5BD6A61E88EDE0530100007FD17D

# Cet identifiant est retrouvable sur la page "edt salles univ angers", 
# exemple (case Amphi A): https://edt.univ-angers.fr/edt/ressource?type=s9FDC055BB1C34F92E0530100007F467B&id=9F8A5BD6A61E88EDE0530100007FD17D
#                                                                           La partie intéressante est ici   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


class CalendarXLink:
    def __init__(self, nom: str, id: str, racine: str = "webcal://edt.univ-angers.fr/edt/ics?id=S"):
        self.nom = nom
        self.id = id
        
        self.link = racine + id
    
    def __str__(self):
        return f"nom: {self.nom}, id: {self.id} (lien webcall {self.link})"
    

def make_doc_name_ok(doc_name):
    unacceptable = ['\\', '/', '*', ':', '?', '"', '<', '>', '|', '\n']
    new_name = ""
    for letter in doc_name:
        if letter not in unacceptable:
            new_name += letter
    
    return new_name


# Renvoie Bool, + sauvegarde en local le fichier ics associé
def est_calendrier_sauvable(cal: CalendarXLink, dossier: str = "../salles") -> bool:
    
    http_url = cal.link.replace('webcal://', 'https://')
    
    response = requests.get(http_url)

    if(response.status_code != 200):
        return False
    else:
        
        ics_content: str = response.text
        
        with open(f'{dossier}/{make_doc_name_ok(cal.nom)}.ics', 'w', encoding='utf-8') as f:
            f.write(ics_content)
        
        return True


def test_est_calendrier_sauvable(webcall_url: str) -> bool:
    if(est_calendrier_sauvable(webcal_url)):
        print("Calendrier enregistré")
    else:
        print("Calendarlendrier pas enregistré")


"""
On dira que les salles intéressantes sont:
- les amphis du bat A
- les salles A1XX

- les salles G
- les salles H
- les salles i (attention, i ***minuscule***)
- les amphis du bat L
- les salles L
- Rez de jardin (:
"""

def est_dans_bat_etage_1_2(cal: CalendarXLink, bat: chr) -> bool:
    #On récupère les 2 premiers charactères du nom
    pref = cal.nom[:2]
    
    return (pref == bat+"1") or (pref == bat+"2")


def est_bat_A(cal: CalendarXLink) -> bool:
    return est_dans_bat_etage_1_2(cal, 'A') or (cal.nom in ("AMPHI A Sciences", "AMPHI B Sciences", "AMPHI D Sciences", "AMPHI E Sciences"))

def est_bat_G(cal: CalendarXLink) -> bool:
    return est_dans_bat_etage_1_2(cal, "G")

def est_bat_H(cal: CalendarXLink) -> bool:
    return est_dans_bat_etage_1_2(cal, "H")

def est_bat_i(cal: CalendarXLink) -> bool:
    pref = cal.nom[:2]
    return (pref == "i0")

def est_bat_L(cal: CalendarXLink) -> bool:
    # les espaces en plus aux noms d'amphis sont fait exprès :D (le fichier html est fait comme ça)
    return est_dans_bat_etage_1_2(cal, "L") or (cal.nom in ("AMPHI L001", "AMPHI L002  ", "AMPHI L003 ", "AMPHI L004 ", "AMPHI L005", "AMPHI L006", "Rez-de-Jardin"))

def est_salles_importante(cal: CalendarXLink) -> bool:
    return est_bat_A(cal) or est_bat_G(cal) or est_bat_H(cal) or est_bat_i(cal) or est_bat_L(cal)

# un premier essai de récupération des liens utiles
def prototype_recherche_liens_edt_salles_univ_angers():
    response = requests.get("https://edt.univ-angers.fr/edt/ressources?id=s9FDC055BB1C34F92E0530100007F467B")
    if(response.status_code != 200):
        print("code différent de 200:", response.status_code)
    else:
        print("soupage en cours")
        
        # On transforme le fichier texte html en objet parsable
        soup = BeautifulSoup(response.text, "html.parser")
        
        # liste de tout les <td> contenant l'attribut scope="row"
        filtre_td = soup.find_all("td", attrs={"scope": "row"})
        
        #On passe dans la liste
        for tag_td in filtre_td:
            
            # On ne s'occupe que de <a> dans le <td>
            tag_a = tag_td.a
            
            # On récupère le lien
            link = tag_a.get('href')
            # Et son texte
            nom = tag_a.text
            
            print(f"{nom = }, {link = }")


# Récupère l'id, en partant du lien de racine "./ressource?type=s9FDC055BB1C34F92E0530100007F467B"
def link_to_id(link: str) -> str:
    # L'id, c'est les 32 derniers caractères du lien :)
    return link[-32::]


def sauve_tous_calendrier(page_principale: str = "https://edt.univ-angers.fr/edt/ressources?id=s9FDC055BB1C34F92E0530100007F467B"):
    
    # Récupération de la page web
    response = requests.get(page_principale)
    
    if(response.status_code != 200):
        print("Code différent de 200:", response.status_code)
    else:
        print("soupage en cours")
        
        # On transforme le fichier texte html en objet parsable
        soup = BeautifulSoup(response.text, "html.parser")
        
        # liste de tout les <td> contenant l'attribut scope="row"
        filtre_td = soup.find_all("td", attrs={"scope": "row"})
        
        print("enregistrement des calendriers")
        
        print("Il y a", len(filtre_td), "salles")
        # On passe dans la liste
        
        nb_enregistrées = 0
        for tag_td in filtre_td:
            
            # On ne s'occupe que de <a> dans le <td>
            tag_a = tag_td.a
            
            # On récupère le lien
            link = tag_a.get('href')
            
            # Et son texte
            nom = tag_a.text
            
            cal = CalendarXLink(nom, link_to_id(link))
            
            if est_salles_importante(cal):
                nb_enregistrées += 1
                if(not est_calendrier_sauvable(cal)):
                    print(f"{cal.nom} important, mais pas sauvegardé (ERREUR)")
                else:
                    print(f"{cal.nom} OK")
            else:
                print(f"{cal.nom} pas important")
        
        print(f"Il y a {nb_enregistrées} salles importantes")


# exemple avec amphi A: "https://edt.univ-angers.fr/edt/ressource?type=s9FDC055BB1C34F92E0530100007F467B&id=9F8A5BD6A61E88EDE0530100007FD17D"
# lien d'une salle:  type='id_page_principale'&id='id_de_la_salle'     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
def proto_affiche_une_semaine(cal: CalendarXLink, racine: str = "https://edt.univ-angers.fr/edt/ressource?type=s9FDC055BB1C34F92E0530100007F467B"):
    
    page_une_salle = racine + "&id=" + cal.id
    
    response = requests.get(page_une_salle)
    
    if(response.status_code != 200):
        print("code diff de 200 ("+response.status_code+"), fin de", cal.nom)
    else:
        print("soupage de", cal.nom)
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        print(soup.prettify)
        
        # liste tous les th de class = "fc-day-header" (ils contiennent les infos sur la date)
        filtre_th = soup.find_all("th", attrs={"class": "fc-day-header"})
        
        print(filtre_th)
        
        # trouve les div de class = "fc-content-col" (contient les évènements pour une journée donnée)
        filtre_div = soup.find_all("div", attrs={"class": "fc-event-container"})
        # on ne prend que ceux contenant uniquement l'attribut "fc-event-container"
        filtre_div = [div for div in filtre_div if div.get("class") == ["fc-event-container"]]
        
        for i, date in enumerate(filtre_th):
            print("------", date.text, "------")
            
            events = filtre_div[i].find_all("a")
            
            for event in events:
                event = event.div
                event("div")
                print(event[0].text)
                print(event[1].text)
                print("-")


"""
# Analyser le fichier ICS
calendar = Calendar(ics_content)

# Parcourir les événements
for event in calendar.events:
    print(f"Titre : {event.name}")
    print(f"Début : {event.begin}")
    print(f"Fin : {event.end}")
    print(f"Description : {event.description}")
    print("-" * 20)
"""


def main():
    # URL du fichier ICS (avec un schéma webcal://)
    
    # A116:     webcal://edt.univ-angers.fr/edt/ics?id=S9F8A5BD6A60A88EDE0530100007FD17D
    # L106 :    webcal://edt.univ-angers.fr/edt/ics?id=S9F8A5BD6A6B788EDE0530100007FD17D
    #                       bel et bien des liens différents ---> ^^
    '''
    webcall = "webcal://edt.univ-angers.fr/edt/ics?id=S9F8A5BD6A6B788EDE0530100007FD17D"
    test_est_calendrier_sauvable(webcall)
    '''
    
    '''
    prototype_recherche_liens_edt_salles_univ_angers()
    '''
    
    sauve_tous_calendrier()
    
    """
    cal = CalendarXLink("Amphi A", "9F8A5BD6A61E88EDE0530100007FD17D")
    
    proto_affiche_une_semaine(cal)
    """

if __name__ == "__main__":
    main()