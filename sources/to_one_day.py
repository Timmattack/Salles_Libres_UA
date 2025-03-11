from ics import Calendar
from ics.timeline import Timeline
from os import walk

def filtre_ICS(fic: str):
    
    # Charger le fichier ICS
    with open(fic, "r", encoding="utf-8") as fichier:
        contenu = fichier.read()
    
    cal = Calendar(contenu)
    
    # Créer une Timeline à partir des événements du calendrier
    timeline = Timeline(cal)
    
    
    # Filtrer les événements d'aujourd'hui
    evenements_du_jour = { event for event in timeline.today() }
    
    
    # Créer un nouveau calendrier avec ces événements
    nouveau_cal = Calendar(events=evenements_du_jour)
    
    # On ajoute un autre évènement, afin de ne pas rester vide (les évènements contiennent des infos importantes, notamment lien vers son calendrier)
    premier_event = next(iter(cal.events), None)
    nouveau_cal.events.add(premier_event)
    
    # Sauvegarder dans un nouveau fichier ICS
    with open(fic, "w", encoding="utf-8") as fichier:
        fichier.writelines(nouveau_cal.serialize())


def filtre_tous_ICS(dossier: str):
    
    filenames = next(walk(dossier), (None, None, []))[2]
    
    filenames = [dossier+file for file in filenames]
    
    for file in filenames:
        filtre_ICS(file)


if __name__ == "__main__":
    
    filtre_tous_ICS("../salles_edt/")