import math
import random

def determiner_seuil_mortel(max_assiettes, nb_etudiants, max_morts):
    # Génération aléatoire des seuils de tolérance pour chaque étudiant
    seuils_tolerance = [random.randint(5, 20) for _ in range(nb_etudiants)]
    nb_morts = 0
    etudiants_morts = []

    # Sélection de la meilleure méthode de recherche selon le nombre d'étudiants
    if nb_etudiants >= math.log2(max_assiettes):
        return recherche_binaire(max_assiettes, seuils_tolerance, max_morts, nb_morts, etudiants_morts)
    elif nb_etudiants == 2:
        return recherche_racine(max_assiettes, seuils_tolerance, max_morts, nb_morts, etudiants_morts)
    else:
        return recherche_optimisee(max_assiettes, nb_etudiants, seuils_tolerance, max_morts, nb_morts, etudiants_morts)

def recherche_binaire(max_assiettes, seuils_tolerance, max_morts, nb_morts, etudiants_morts):

    gauche, droite = 1, max_assiettes + 1
    while gauche < droite:
        milieu = (gauche + droite) // 2
        survit, nb_morts, etudiants_morts = tester_resistance(milieu, seuils_tolerance, nb_morts, etudiants_morts)

        if nb_morts >= max_morts:
            return milieu, etudiants_morts
        if survit:
            gauche = milieu + 1
        else:
            droite = milieu

    return gauche, etudiants_morts

def recherche_racine(max_assiettes, seuils_tolerance, max_morts, nb_morts, etudiants_morts):

    pas = int(math.sqrt(max_assiettes))
    actuel = pas

    while actuel <= max_assiettes:
        survit, nb_morts, etudiants_morts = tester_resistance(actuel, seuils_tolerance, nb_morts, etudiants_morts)
        if nb_morts >= max_morts:
            return actuel, etudiants_morts
        if not survit:
            break
        actuel += pas

    # Affinage du seuil mortel
    actuel -= pas
    while actuel <= max_assiettes:
        survit, nb_morts, etudiants_morts = tester_resistance(actuel, seuils_tolerance, nb_morts, etudiants_morts)
        if nb_morts >= max_morts:
            return actuel, etudiants_morts
        if not survit:
            break
        actuel += 1

    return actuel, etudiants_morts

def recherche_optimisee(max_assiettes, nb_etudiants, seuils_tolerance, max_morts, nb_morts, etudiants_morts):

    pas = max_assiettes // (2 * nb_etudiants - 1)
    actuel = pas

    while actuel <= max_assiettes:
        survit, nb_morts, etudiants_morts = tester_resistance(actuel, seuils_tolerance, nb_morts, etudiants_morts)
        if nb_morts >= max_morts:
            return actuel, etudiants_morts
        if not survit:
            break
        actuel += pas

    # Recherche fine autour du dernier seuil connu
    actuel -= pas
    while actuel <= max_assiettes:
        survit, nb_morts, etudiants_morts = tester_resistance(actuel, seuils_tolerance, nb_morts, etudiants_morts)
        if nb_morts >= max_morts:
            return actuel, etudiants_morts
        if not survit:
            break
        actuel += 1

    return actuel, etudiants_morts

def tester_resistance(nb_assiettes, seuils_tolerance, nb_morts, etudiants_morts):

    for i, seuil in enumerate(seuils_tolerance):
        if nb_assiettes > seuil:
            nb_morts += 1
            etudiants_morts.append((i, nb_assiettes))  # Sauvegarde l'étudiant mort et son seuil
            seuils_tolerance[i] = float('inf')  # L'étudiant ne peut plus être utilisé
            return False, nb_morts, etudiants_morts

    return True, nb_morts, etudiants_morts

# Paramètres de l'expérience
max_assiettes = 20  
nb_etudiants = 300  
max_morts = 2      

# Exécution de la simulation
seuil_mortel, liste_morts = determiner_seuil_mortel(max_assiettes, nb_etudiants, max_morts)

# Affichage des résultats
print(f"\nSeuil mortel détecté : {seuil_mortel} assiettes")
if liste_morts:
    print("\nÉtudiants morts (index, assiettes fatales) :")
    for index, assiettes in liste_morts:
        print(f"   - Étudiant {index + 1} : {assiettes} assiettes")
