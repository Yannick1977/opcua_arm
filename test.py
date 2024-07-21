import os
import json

def creer_arborescence_dossier_json(chemin_dossier):
    arborescence = {}

    for racine, dossiers, fichiers in os.walk(chemin_dossier):
        chemin_relatif = os.path.relpath(racine, chemin_dossier)
        noeud = arborescence
        if chemin_relatif != '.':
            for partie in chemin_relatif.split(os.sep):
                noeud = noeud.setdefault(partie, {})
        noeud.update({dossier: {} for dossier in dossiers})
        noeud.update({fichier: None for fichier in fichiers})

    return json.dumps(arborescence, indent=4)

# Exemple d'utilisation
chemin_dossier = './test'
json_arborescence = creer_arborescence_dossier_json(chemin_dossier)
print(json_arborescence)