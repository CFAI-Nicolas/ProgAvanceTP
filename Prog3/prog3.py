import itertools
import time

# Valeurs fixes pour le test
cible = 813
nombres = [6, 5, 10, 9, 8, 3]

# ---------------------------- ANCIENNE VERSION ----------------------------

def ancienne_trouveExpr(v, valeurs):
    """
    Ancienne version basée sur la méthodologie d'origine, sans optimisation.
    """
    global nb_appels_ancienne, nb_redondances_ancienne
    nb_appels_ancienne += 1
    
    key = (v, tuple(sorted(valeurs)))  
    if key in memo_ancienne:
        nb_redondances_ancienne += 1
        return memo_ancienne[key]

    if len(valeurs) == 1:
        if v == valeurs[0]:
            return (True, str(v))
        else:
            return (False, "")

    if v in valeurs:
        return (True, str(v))

    for x in valeurs:
        valeurs2 = valeurs[:]
        valeurs2.remove(x)

        t, ch = ancienne_trouveExpr(v + x, valeurs2)
        if t:
            memo_ancienne[key] = (t, ch + " - " + str(x))
            return memo_ancienne[key]

        if v >= x:
            t, ch = ancienne_trouveExpr(v - x, valeurs2)
            if t:
                memo_ancienne[key] = (t, str(x) + " + (" + ch + ") ")
                return memo_ancienne[key]

        if v <= x:
            t, ch = ancienne_trouveExpr(x - v, valeurs2)
            if t:
                memo_ancienne[key] = (t, str(x) + " + (" + ch + ") ")
                return memo_ancienne[key]

        if v >= x and v % x == 0:
            t, ch = ancienne_trouveExpr(v // x, valeurs2)
            if t:
                memo_ancienne[key] = (t, "(" + ch + ") * " + str(x))
                return memo_ancienne[key]

        if v <= x and x % v == 0:
            t, ch = ancienne_trouveExpr(x // v, valeurs2)
            if t:
                memo_ancienne[key] = (t, str(x) + " / (" + ch + ") ")
                return memo_ancienne[key]

        t, ch = ancienne_trouveExpr(v * x, valeurs2)
        if t:
            memo_ancienne[key] = (t, "(" + ch + ") / " + str(x))
            return memo_ancienne[key]

    memo_ancienne[key] = (False, "")
    return memo_ancienne[key]


# ---------------------------- NOUVELLE VERSION ----------------------------

def nouvelle_trouveExpr(v, valeurs):
    """
    Version ultra-optimisée avec pruning, programmation dynamique et priorisation des calculs.
    """
    global nb_appels_nouvelle, nb_redondances_nouvelle
    nb_appels_nouvelle += 1
    
    key = (v, tuple(sorted(valeurs)))  
    if key in memo_nouvelle:
        nb_redondances_nouvelle += 1
        return memo_nouvelle[key]

    if len(valeurs) == 1:
        return (True, str(v)) if v == valeurs[0] else (False, "")

    if v in valeurs:
        return (True, str(v))

    # Trie les valeurs pour tester les plus grandes d'abord (plus efficace)
    valeurs = sorted(valeurs, reverse=True)

    # Génération optimisée des paires possibles
    for x, y in itertools.combinations(valeurs, 2):
        nouveaux_nombres = [n for n in valeurs if n != x and n != y]

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

# Génération des valeurs pour le jeu
NBNOMBRES = 6
nombres = random.sample([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 25, 50, 75, 100], NBNOMBRES)
cible = random.randint(100, 999)

# Résolution du problème
res = trouveExpr(cible, nombres)

# Affichage des résultats détaillés
print(f"\nCible : {cible}")
print(f"Nombres disponibles : {nombres}")
if res[0]:
    print(f"Solution trouvée : {res[1]}")
    print(f"Détail des calculs : {res[2]}")
else:
    print("Aucune solution exacte trouvée.")
print(f"Nombre total d'appels récursifs : {cpt}")
