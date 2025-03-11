from ics import Calendar, Event
import arrow
from datetime import datetime, date, timedelta
from pytz import timezone
from zoneinfo import ZoneInfo
from os import walk
import json

"""
Objectif:
    Récolter les moments où les salles sont libres (pas d'évènement à X moment)
    
on se limitera à vérifier les horaires entre 7h30 et 19h00 (pour une journée)

1- charger le .ics
2- récupérer les dates des évènements (la paire début et fin)
3- ?? créer un ics de salles libre ??
"""

''' tzdata names:
TIMEZONE LIST EXEMPLES
UTC +1: "Europe/Paris"
UTC +0: "Zulu"
UTC -5: "America/New_York"
'''

def debut_fin_event(event):
    if(event):
        return event.begin, event.end
    else:
        return None


def Get_first_event(file: str):
    with open(file, 'r', encoding='utf-8') as f:
        ics_content = f.read()
    
    calendar = Calendar(ics_content)
    
    first_event = next(iter(calendar.events), None)
    
    return first_event
    

def cool_print_date(date: arrow.arrow.Arrow) -> None:
    print(date.year, "/", date.month, "/", date.day, "j", 
    date.hour, ":", date.minute)


def print_evenement_today(calendar: Calendar) -> None:

    for element in calendar.events:

        elementDate = element.begin.date()

        if elementDate == date.today():
            print("TODAY : ", element.begin, " WITH ", element.name)

    
def afficher_evenement_heure_locale(event: Event, tz: timezone) -> None:
    begin = event.begin.astimezone(tz)
    end = event.end.astimezone(tz)
    print("- - -")
    print("[DEBUT]>", begin, " [FIN]>", end, " [NOM]>", event.name)


def temps_entre_deux_event( begin: datetime, time_check: datetime, end: datetime) -> bool:
    if begin < time_check and time_check < end:
        return True
    
    return False


def est_salle_libre(salle_file_path: str, time_check: datetime) -> bool:

    # on ouvre le fichier ics de la salle :
    with open(salle_file_path, 'r') as file:
        calendar = Calendar(file.read())

    for element in calendar.events: # on regarde tout les evenements d'une salle, si aucun d'eux ne pose problème, alors elle est libre
        if temps_entre_deux_event(element.begin ,time_check, element.end):
            #afficher_evenement_heure_locale(element, timezone("Europe/Paris"))
            return False
        
    return True


def iterations_event(file_path: str) -> None:
    # Open the ics file 
    with open(file_path, 'r', encoding='utf-8') as file:
        calendar = Calendar(file.read())

    for element in calendar.walk():
        if element.name == "VEVENT":
            date_start = element.get('dtstart').dt
            if isinstance(date_start, datetime):
                date = date_start.date()
            else:
                date = date_start
            if date == datetime.now():
                print(date, " / ",element.get("summary"))



def print_salles_libre_at():

    chemin_salles = "../salles_edt/"
    paris_tz = timezone("Europe/Paris")
    customTime = datetime.now()
    customTime = customTime.replace(tzinfo=paris_tz)

    filenames = next(walk(chemin_salles), (None, None, []))[2]

    filenames = [chemin_salles+file for file in filenames]

    exportJson = {}

    for file in filenames:
        #print(file)
        if est_salle_libre(file, customTime):
            #print(file, "est libre")
            #print(file, " LIEN SALLE", )
            

            
            exportJson[file] = "est libre"
        else:
            print(file, "est pas libre")

    print(exportJson)
    print(len(exportJson))

    with open("../salles_libres/salles_libres_beta.json", "w", encoding="utf-8") as f:
        json.dump(exportJson, f, ensure_ascii=False);



def main() -> None:



    print_salles_libre_at()
    #print(datetime.now())


if __name__ == "__main__":
    main()
