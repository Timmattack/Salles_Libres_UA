from ics import Calendar
from ics.timeline import Timeline
import arrow
from os import walk
import json

from API import est_bat_A, est_bat_G, est_bat_I, est_bat_H, est_bat_L, make_name_simple

"""
Objectif:
    Récolter les moments où lesest_bat_L salles sont libres (pas d'évènement à X moment)
    
on se limitera à vérifier les horaires sur une journée

1- charger le .ics
2- vérifier si la salle n'a pas d'évènement entre maintenant + 5min et maintenant + 20min
3- créer un json des salles libres
"""

def filesWithFreeRoom(dossier, start, end):
    filenames = next(walk(dossier), (None, None, []))[2]
    
    filenames = [dossier+file for file in filenames]
    
    salles_libres = []
    
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
    
    
    return salles_libres


def extraitNomSalle(fic: str, dossier: str):
    return fic[len(dossier):len(fic)-len(".ics")]


def extraitID(fic: str):
    with open(fic, "r", encoding="utf-8") as fichier:
        contenu = fichier.read()

    cal = Calendar(contenu)

    premier_event = next(iter(cal.events), None)

    premier_event.uid[1:33]


def InitDicSalle(nom: str, lien: str, prochain_occupe: str):
    TheDict = {
    "nom": "",
    "lien": "",
    "prochain_occupe": ""
    }
    
    TheDict["nom"] = nom
    TheDict["lien"] = lien
    TheDict["prochain_occupe"] = prochain_occupe
    
    return TheDict


def sallesBat_X(est_bat_X, fic_salles_libres: str, nom_salles_libres, end: arrow, RACINE: str = "https://edt.univ-angers.fr/edt/ressource?type=s9FDC055BB1C34F92E0530100007F467B&id="):
    
    sallesBX = []
    for fic, nom_salle in zip(fic_salles_libres, nom_salles_libres):
        if est_bat_X(make_name_simple(nom_salle)):
            
            # On extrait l'id du calendrier
            with open(fic, "r", encoding="utf-8") as fichier:
                contenu = fichier.read()

            cal = Calendar(contenu)

            premier_event = next(iter(cal.events), None)

            id = premier_event.uid[1:33]
            
            # Puis l'heure de son prochain event ('demain' sinon)
            timeline = Timeline(cal)
            
            next_event = next(timeline.start_after(end), None)
            
            if(next_event):
                prochain_occupe = next_event.begin
                                            .to('local')
                                            .format('HH [h] mm')
            else:
                prochain_occupe = None
            
            
            sallesBX.append(InitDicSalle(make_name_simple(nom_salle), RACINE+id, prochain_occupe))
    
    return sallesBX



def main() -> None:
    dossier = "../salles_edt/"
    
    start = arrow.utcnow().replace(minute=+5)
    end = arrow.utcnow().replace(minute=+20)
    
    fic_salles_libres = filesWithFreeRoom(dossier, start, end)
    nom_salles_libres = [extraitNomSalle(fic, dossier) for fic in fic_salles_libres]
    
    JSON_Result = {
    "Batiment A": [],
    "Batiment G": [],
    "Batiment H": [],
    "Batiment I": [],
    "Batiment L": []
    }
    
    JSON_Result["Batiment A"] = sallesBat_X(est_bat_A, fic_salles_libres, nom_salles_libres, end)
    JSON_Result["Batiment G"] = sallesBat_X(est_bat_G, fic_salles_libres, nom_salles_libres, end)
    JSON_Result["Batiment H"] = sallesBat_X(est_bat_H, fic_salles_libres, nom_salles_libres, end)
    JSON_Result["Batiment I"] = sallesBat_X(est_bat_I, fic_salles_libres, nom_salles_libres, end)
    JSON_Result["Batiment L"] = sallesBat_X(est_bat_L, fic_salles_libres, nom_salles_libres, end)
    
    with open("../salles_libres/salles_libres.json", 'w') as f:
        json.dump(JSON_Result, f)
    

if __name__ == "__main__":
    main()
