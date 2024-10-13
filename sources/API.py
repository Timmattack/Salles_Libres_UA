import requests
from ics import Calendar


def est_calendrier_sauvable(Webcall: str, ) -> bool:
    
    http_url = Webcall.replace('webcal://', 'https://')
    
    response = requests.get(http_url)

    print(response.status_code)

    if(response.status_code != 200):
        return False
    else:
        ics_content = response.text
        calendar = Calendar(ics_content)
        
        first_event = next(iter(calendar.events))
        
        salle = first_event.location
        
        with open(f'{salle}.ics', 'w', encoding='utf-8') as f:
            f.write(ics_content)
        
        return True
    

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
    webcal_url = 'webcal://edt.univ-angers.fr/edt/ics?id=S9F8A5BD6A60A88EDE0530100007FD17D'
    
    if(est_calendrier_sauvable(webcal_url)):
        print("Calendrier enregistré")
    else:
        print("Calendarlendrier pas enregistré")


if __name__ == "__main__":
    main()