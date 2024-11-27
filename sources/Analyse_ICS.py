from ics import Calendar, Event
import arrow
from datetime import datetime, date, timedelta
from pytz import timezone
from zoneinfo import ZoneInfo
from os import walk

"""
Objectif:
    Récolter les moments où les salles sont libres (pas d'évènement à X moment)
    
on se limitera à vérifier les horaires entre 7h30 et 19h00 (pour une journée)

1- charger le .ics
2- récupérer les dates des évènements (la paire début et fin)
3- ?? créer un ics de salles libre ??
"""

# pip install tzdata
# TIMEZONE LIST EXEMPLES
# UTC +1: "Europe/Paris"
# UTC +0: "Zulu"
# UTC -5: "America/New_York"

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






def printEvenementToday(calendar: Calendar) -> None:

    for element in calendar.events:

        elementDate = element.begin.date()

        if elementDate == date.today():
            print("TODAY : ", element.begin, " WITH ", element.name)

    
def printEvenementAtTime(calendar: Calendar, timeToCheck: datetime) -> None:

    for element in calendar.events:

        elementTime = element.begin

        if elementTime == timeToCheck:
            print(elementTime, " / " ,element.name)

def afficher_evenement_heure_locale(event: Event, tz: timezone) -> None:
    begin = event.begin.astimezone(tz)
    end = event.end.astimezone(tz)
    print("- - -")
    print("[DEBUT]>", begin, " [FIN]>", end, " [NOM]>", event.name)


def timeIsInEvent( begin: datetime, end: datetime, timeToCheck: datetime) -> bool:

    
    
    if ( begin < timeToCheck and timeToCheck < end):
        return True
    return False


def estSalleLibre(salle_file_path: str, timeToCheck: datetime) -> bool:

    # on ouvre le fichier ics de la salle :
    with open(salle_file_path, 'r') as file:
        calendar = Calendar(file.read())

    #Si la salle a un evenement à "TimeToCheck" alors est n'est pas libre -> return false, sinon -> true
    #printEvenementToday(calendar)
    for element in calendar.events: # on regarde tout les evenements d'une salle, si aucun d'eux ne pose problème, alors elle est libre
        #eventTime: datetime = element.begin.datetime
        begin_lt = element.begin.astimezone(timezone("Europe/Paris")) # Begin local time
        end_lt = element.end.astimezone(timezone("Europe/Paris")) # Begin local time

        if timeIsInEvent( element.begin , element.end, timeToCheck):
            
            afficher_evenement_heure_locale(element, timezone("Europe/Paris"))
            return False
    print(" ")
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


def main() -> None:

    paris_tz = timezone("Europe/Paris")



    customTime = datetime( 2024, 12, 6, 15, 55, 0)
    customTime = customTime.replace(tzinfo=paris_tz)


    if estSalleLibre("salles/L101 Multimédia.ics", customTime):
        print(" L101 est libre ! :", customTime)
    else:
        print(" L101 prise à :", customTime)
    print(" ")



if __name__ == "__main__":
    main()
