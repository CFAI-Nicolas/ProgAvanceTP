import math
import random

def determiner_seuil_mortel(nombre_max_assiettes, nombre_etudiants, max_morts):
    """
    Détermine le nombre d'assiettes à partir duquel un repas devient mortel.
    Utilise la meilleure stratégie en fonction du nombre d'étudiants disponibles.
    """
    # Chaque étudiant a une tolérance différente (entre 5 et 20 assiettes)
    seuils_tolerance = [random.randint(5, 20) for _ in range(nombre_etudiants)]
    nombre_de_morts = 0
    etudiants_morts = []

    # Choix de l'algorithme optimal en fonction de `k` et `log2(n)`
    if nombre_etudiants >= math.log2(nombre_max_assiettes):
        return recherche_binaire(nombre_max_assiettes, seuils_tolerance, max_morts, nombre_de_morts, etudiants_morts)
    elif nombre_etudiants == 2:
        return recherche_racine(nombre_max_assiettes, seuils_tolerance, max_morts, nombre_de_morts, etudiants_morts)
    else:
        return recherche_optimisee(nombre_max_assiettes, nombre_etudiants, seuils_tolerance, max_morts, nombre_de_morts, etudiants_morts)

def recherche_binaire(max_assiettes, seuils_tolerance, max_morts, nombre_de_morts, etudiants_morts):
    """
    Recherche du seuil mortel en utilisant la recherche binaire (O(log2(n))).
    Permet de trouver rapidement la valeur critique où les étudiants commencent à mourir.
    """
    gauche, droite = 1, max_assiettes + 1
    while gauche < droite:
        milieu = (gauche + droite) // 2
        survit, nombre_de_morts, etudiants_morts = tester_resistance(milieu, seuils_tolerance, nombre_de_morts, etudiants_morts)

        if nombre_de_morts >= max_morts:
            return milieu, etudiants_morts
        if survit:
            gauche = milieu + 1
        else:
            droite = milieu

    return gauche, etudiants_morts

def recherche_racine(max_assiettes, seuils_tolerance, max_morts, nombre_de_morts, etudiants_morts):
    """
    Recherche du seuil mortel avec une approche progressive par incréments de sqrt(n) (O(√n)).
    Efficace lorsque `k = 2` et que le nombre d'étudiants est faible.
    """
    pas = int(math.sqrt(max_assiettes))
    actuel = pas

    while actuel <= max_assiettes:
        survit, nombre_de_morts, etudiants_morts = tester_resistance(actuel, seuils_tolerance, nombre_de_morts, etudiants_morts)
        if nombre_de_morts >= max_morts:
            return actuel, etudiants_morts
        if not survit:
            break
        actuel += pas

    # Recherche plus fine en descendant et en testant un par un
    actuel -= pas
    while actuel <= max_assiettes:
        survit, nombre_de_morts, etudiants_morts = tester_resistance(actuel, seuils_tolerance, nombre_de_morts, etudiants_morts)
        if nombre_de_morts >= max_morts:
            return actuel, etudiants_morts
        if not survit:
            break
        actuel += 1

    return actuel, etudiants_morts

def recherche_optimisee(max_assiettes, nombre_etudiants, seuils_tolerance, max_morts, nombre_de_morts, etudiants_morts):
    """
    Recherche optimisée en O(k + n / (2k - 1)), utilisée lorsque `k < log2(n)`.
    On teste d'abord par grands paliers, puis on affine.
    """
    pas = max_assiettes // (2 * nombre_etudiants - 1)
    actuel = pas

    while actuel <= max_assiettes:
        survit, nombre_de_morts, etudiants_morts = tester_resistance(actuel, seuils_tolerance, nombre_de_morts, etudiants_morts)
        if nombre_de_morts >= max_morts:
            return actuel, etudiants_morts
        if not survit:
            break
        actuel += pas

    # Recherche fine autour du dernier seuil connu
    actuel -= pas
    while actuel <= max_assiettes:
        survit, nombre_de_morts, etudiants_morts = tester_resistance(actuel, seuils_tolerance, nombre_de_morts, etudiants_morts)
        if nombre_de_morts >= max_morts:
            return actuel, etudiants_morts
        if not survit:
            break
        actuel += 1

    return actuel, etudiants_morts

def tester_resistance(nombre_assiettes, seuils_tolerance, nombre_de_morts, etudiants_morts):
    """
    Simule un test : on donne `nombre_assiettes` à chaque étudiant.
    Si un étudiant dépasse sa tolérance, il meurt et n'est plus utilisable.
    """
    for i, seuil in enumerate(seuils_tolerance):
        if nombre_assiettes > seuil:
            nombre_de_morts += 1
            etudiants_morts.append((i, nombre_assiettes))  # Sauvegarde l'index de l'étudiant et le nombre d'assiettes fatales
            seuils_tolerance[i] = float('inf')  # Marque cet étudiant comme inutilisable
            return False, nombre_de_morts, etudiants_morts

    return True, nombre_de_morts, etudiants_morts

# 📌 Exemple d'utilisation
nombre_max_assiettes = 20  # Seuil général
nombre_etudiants = 300     # Nombre total d'étudiants
max_morts = 2              # Nombre maximum d'étudiants pouvant mourir avant d'arrêter

seuil_mortel, liste_morts = determiner_seuil_mortel(nombre_max_assiettes, nombre_etudiants, max_morts)

# 🔥 Affichage des résultats
print(f"\n🍽️ Seuil mortel d'assiettes détecté : {seuil_mortel}")
if liste_morts:
    print("\n☠️ Étudiants morts (index, assiettes fatales) :")
    for index, assiettes in liste_morts:
        print(f"   - Étudiant {index + 1} : {assiettes} assiettes")
