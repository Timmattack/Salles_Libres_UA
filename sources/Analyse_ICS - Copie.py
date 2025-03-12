from ics import Calendar
from ics.timeline import Timeline
import arrow
from os import walk
import json

"""
Objectif:
    Récolter les moments où les salles sont libres (pas d'évènement à X moment)
    
on se limitera à vérifier les horaires sur une journée

1- charger le .ics
2- vérifier si la salle n'a pas d'évènement entre maintenant + 5min et maintenant + 20min
3- créer un json des salles libres
"""




def main() -> None:
    dossier = "../salles_edt/"
    
    filenames = next(walk(dossier), (None, None, []))[2]
    
    filenames = [dossier+file for file in filenames]
    
    salles_libres = []
    start = arrow.utcnow().replace(minute=+5)
    end = arrow.utcnow().replace(minute=+20)
    
    
    for file in filenames:
        with open(file, "r", encoding="utf-8") as fichier:
            contenu = fichier.read()
    
        cal = Calendar(contenu)
        
        timeline = Timeline(cal)
        
        overlap = list(timeline.overlapping(start, end))
        
        """
        for event in overlap:
            print(event.description)
        print("---------------")
        """
        
        if(not overlap):
            salles_libres.append(file)
    
    print("les salles libres sont : ")
    for file in salles_libres:
        print(file)
    
    

if __name__ == "__main__":
    main()
