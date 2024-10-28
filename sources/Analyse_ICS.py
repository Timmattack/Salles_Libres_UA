from ics import Calendar, Event
import arrow

"""
Objectif:
    Récolter les moments où les salles sont libres (pas d'évènement à X moment)
    
on se limitera à vérifier les horaires entre 7h30 et 19h00 (pour une journée)

1- charger le .ics
2- récupérer les dates des évènements (la paire début et fin)
3- ?? créer un ics de salles libre ??
"""

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





def main() -> None:
    
    first_event = Get_first_event("../salles/L101 Multimédia.ics")
    
    dates = debut_fin_event(first_event)
    
    if(dates):
        d1 = dates[0]
        d2 = dates[1]
        
        print(f"{type(d1) = }")
        print(f"{type(d1.hour) = }")
        
        cool_print_date(d1)
        cool_print_date(d2)
    else:
        print("Pas de dates")


if __name__ == "__main__":
    main()