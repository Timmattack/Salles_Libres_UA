import json

myData = {"Bat A":[
                {"nom": "Amphi A", "lien": "https://edt.univ-angers.fr/edt/ressource?type=s9FDC055BB1C34F92E0530100007F467B&id=9F8A5BD6A61E88EDE0530100007FD17D"}, 
                {"nom": "Amphi B", "lien": "https://edt.univ-angers.fr/edt/ressource?type=s9FDC055BB1C34F92E0530100007F467B&id=9F8A5BD6A62088EDE0530100007FD17D"}, 
                {"nom": "A117", "lien": "https://edt.univ-angers.fr/edt/ressource?type=s9FDC055BB1C34F92E0530100007F467B&id=9F8A5BD6A60B88EDE0530100007FD17D"}
        ] ,
        "Bat L":[
                {"nom": "Amphi L005", "lien": "https://edt.univ-angers.fr/edt/ressource?type=s9FDC055BB1C34F92E0530100007F467B&id=9F8A5BD6A63A88EDE0530100007FD17D"}, 
                {"nom": "L101", "lien": "https://edt.univ-angers.fr/edt/ressource?type=s9FDC055BB1C34F92E0530100007F467B&id=9F8A5BD6A6B288EDE0530100007FD17D"}, 
                {"nom": "L210", "lien": "https://edt.univ-angers.fr/edt/ressource?type=s9FDC055BB1C34F92E0530100007F467B&id=9F8A5BD6A6C388EDE0530100007FD17D"}, 
                {"nom": "L201", "lien": "https://edt.univ-angers.fr/edt/ressource?type=s9FDC055BB1C34F92E0530100007F467B&id=9F8A5BD6A6BA88EDE0530100007FD17D"}
        ], 
        "Bat Feur":[
        ]
    }

with open("salles_libres.json", "w", encoding="utf-8") as f:
    json.dump(myData, f, ensure_ascii=False);