import heapq
from copy import deepcopy

TROU = '0'  # Représente l'espace vide dans le Taquin
Taquin_TXT = "taquin3.txt"
def afficher_taquin(taquin):
    for ligne in taquin:
        print(' '.join(ligne))
    print()

def charger_taquin(fichier):
    with open(fichier, "r") as f:
        lignes = f.readlines()
    
    # Divise les lignes en état initial et état cible
    taille = len(lignes) // 2  
    taquin_initial = [l.split() for l in lignes[:taille]]
    taquin_cible = [l.split() for l in lignes[taille:]]
    
    return taquin_initial, taquin_cible, taille

def trouver_position(valeur, taquin):
    for i, ligne in enumerate(taquin):
        if valeur in ligne:
            return i, ligne.index(valeur)

def heuristique_manhattan(taquin, taquin_cible):
    distance_totale = 0
    for y in range(len(taquin)):
        for x in range(len(taquin[y])):
            if taquin[y][x] != TROU:  # Ignorer la case vide
                y_cible, x_cible = trouver_position(taquin[y][x], taquin_cible)
                distance_totale += abs(y_cible - y) + abs(x_cible - x)
    return distance_totale

def generer_voisins(taquin, taille):
    voisins = []
    y_trou, x_trou = trouver_position(TROU, taquin)
    
    # Déplacements possibles : haut, bas, gauche, droite
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dy, dx in directions:
        y_voisin, x_voisin = y_trou + dy, x_trou + dx
        
        if 0 <= y_voisin < taille and 0 <= x_voisin < taille:
            # Créer une nouvelle configuration en échangeant le trou
            nouveau_taquin = deepcopy(taquin)
            valeur_deplacee = nouveau_taquin[y_voisin][x_voisin]
            nouveau_taquin[y_trou][x_trou], nouveau_taquin[y_voisin][x_voisin] = valeur_deplacee, TROU
            
            mouvement = f"{valeur_deplacee} -> {TROU}"
            voisins.append((nouveau_taquin, mouvement))
    
    return voisins

def resoudre_taquin(taquin_initial, taquin_cible, taille):    
    # File de priorité pour explorer les états les plus prometteurs en premier
    file_priorite = []
    heapq.heappush(file_priorite, (heuristique_manhattan(taquin_initial, taquin_cible), 0, taquin_initial, []))
    # (score heuristique, coût actuel, état actuel, chemin des mouvements)
    
    etats_visites = set()

    while file_priorite:
        _, cout, etat_actuel, chemin = heapq.heappop(file_priorite)
        
        # Vérifie si l'état actuel est la solution
        if etat_actuel == taquin_cible:
            print(f"Solution trouvée en {cout} mouvements.\n")
            for mouvement, etape in chemin:
                print(f"Déplacement : {mouvement}")
                afficher_taquin(etape)
            return
        
        # Marquer l'état comme visité pour éviter les boucles
        etat_fige = tuple(map(tuple, etat_actuel))
        if etat_fige in etats_visites:
            continue
        etats_visites.add(etat_fige)
        
        # Génère les voisins et ajoute les nouveaux états à explorer
        for voisin, mouvement in generer_voisins(etat_actuel, taille):
            nouveau_cout = cout + 1  # Chaque mouvement a un coût de 1
            score = nouveau_cout + heuristique_manhattan(voisin, taquin_cible)
            heapq.heappush(file_priorite, (score, nouveau_cout, voisin, chemin + [(mouvement, voisin)]))
    
    print("Pas de solution trouvée.")

# Charger et résoudre le puzzle
taquin_initial, taquin_cible, taille_taquin = charger_taquin(Taquin_TXT)

print("État initial du Taquin :")
afficher_taquin(taquin_initial)

print("État cible du Taquin :")
afficher_taquin(taquin_cible)

resoudre_taquin(taquin_initial, taquin_cible, taille_taquin)
