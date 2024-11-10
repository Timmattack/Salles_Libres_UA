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
    def __init__(self, nom: str, id: str, racine: str = "webcal://edt.univ-angers.fr/edt/ics?id="):
        self.nom = nom
        self.id = id
        
        self.link = racine + id



def est_calendrier_sauvable(cal: CalendarXLink) -> bool:
    
    http_url = cal.link.replace('webcal://', 'https://')
    
    response = requests.get(http_url)

    print(response.status_code)

    if(response.status_code != 200):
        return False
    else:
        
        ics_content: str = response.text
        
        with open(f'{cal.nom}.ics', 'w', encoding='utf-8') as f:
            f.write(ics_content)
        
        return True

def test_est_calendrier_sauvable(webcall_url: str):
    if(est_calendrier_sauvable(webcal_url)):
        print("Calendrier enregistré")
    else:
        print("Calendarlendrier pas enregistré")


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
            
            print(f"{tag_a.text = }, {link = }")




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
    
    prototype_recherche_liens_edt_salles_univ_angers()
    
    



if __name__ == "__main__":
    main()