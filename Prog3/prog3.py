import random

cpt = 0  # Compteur d'appels récursifs
memo = {}  # Dictionnaire pour stocker les résultats intermédiaires

def trouveExpr(v, valeurs, chemin=""):
    """
    Trouve une expression permettant d'obtenir v en utilisant les nombres de valeurs.
    Retourne une solution détaillée avec toutes les étapes du calcul.
    """
    global cpt
    cpt += 1
    
    # Vérification si on a déjà calculé cette combinaison
    key = (v, tuple(sorted(valeurs)))  
    if key in memo:
        return memo[key]

    # Cas de base : un seul nombre restant
    if len(valeurs) == 1:
        if v == valeurs[0]:
            return (True, str(v), f"{chemin} => {v}")
        else:
            return (False, "", chemin)

    # Si la cible est déjà présente dans la liste
    if v in valeurs:
        return (True, str(v), f"{chemin} => {v}")

    # Test des opérations possibles
    for i, x in enumerate(valeurs):
        valeurs2 = valeurs[:i] + valeurs[i+1:]  # Liste des valeurs restantes

        # Addition
        if (t := trouveExpr(v - x, valeurs2, chemin + f"({v - x} + {x})"))[0]:
            memo[key] = (t[0], f"({t[1]} + {x})", t[2])
            return memo[key]

        # Soustraction (uniquement si v >= x pour éviter les négatifs inutiles)
        if v >= x and (t := trouveExpr(v + x, valeurs2, chemin + f"({x} - ({v - x}))"))[0]:
            memo[key] = (t[0], f"({x} - {t[1]})", t[2])
            return memo[key]

        # Multiplication (uniquement si v est divisible par x)
        if v % x == 0 and (t := trouveExpr(v // x, valeurs2, chemin + f"({v // x} * {x})"))[0]:
            memo[key] = (t[0], f"({t[1]} * {x})", t[2])
            return memo[key]

        # Division (évite les divisions inutiles)
        if x % v == 0 and (t := trouveExpr(x // v, valeurs2, chemin + f"({x} / ({x // v}))"))[0]:
            memo[key] = (t[0], f"({x} / {t[1]})", t[2])
            return memo[key]

    # Aucun résultat trouvé, on stocke l'échec pour éviter de recalculer
    memo[key] = (False, "", chemin)
    return memo[key]

# ⚙️ Génération des valeurs pour le jeu
NBNOMBRES = 6
nombres = random.sample([1,2,3,4,5,6,7,8,9,10,25,50,75,100], NBNOMBRES)
cible = random.randint(100, 999)

# 🔍 Résolution du problème
res = trouveExpr(cible, nombres)

# 📌 Affichage des résultats détaillés
print(f"\n🎯 Cible : {cible}")
print(f"🔢 Nombres disponibles : {nombres}")
if res[0]:
    print(f"✅ Solution trouvée : {res[1]}")
    print(f"📜 Détail des calculs : {res[2]}")
else:
    print("❌ Aucune solution exacte trouvée.")
print(f"🔄 Nombre total d'appels récursifs : {cpt}")
