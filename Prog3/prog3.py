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

        operations = [
            (x + y, f"({x} + {y})"),
            (x - y, f"({x} - {y})") if x > y else None,
            (y - x, f"({y} - {x})") if y > x else None,
            (x * y, f"({x} * {y})"),
            (x // y, f"({x} / {y})") if y != 0 and x % y == 0 else None,
            (y // x, f"({y} / {x})") if x != 0 and y % x == 0 else None,
        ]

        operations = [op for op in operations if op is not None]

        # Pruning : on teste d'abord les additions et multiplications avant divisions
        for resultat, expression in operations:
            if resultat < 0 or resultat > 1000:  # Évite les nombres inutiles
                continue
            tentative = nouvelle_trouveExpr(v, nouveaux_nombres + [resultat])
            if tentative[0]:
                memo_nouvelle[key] = (True, tentative[1].replace(str(resultat), expression, 1))
                return memo_nouvelle[key]

    memo_nouvelle[key] = (False, "")
    return memo_nouvelle[key]


# ---------------------------- TEST DES DEUX VERSIONS ----------------------------

# Exécution de l'ancienne version
nb_appels_ancienne, nb_redondances_ancienne = 0, 0
memo_ancienne = {}
start_time = time.time()
res_ancienne = ancienne_trouveExpr(cible, nombres)
time_ancienne = time.time() - start_time

# Exécution de la nouvelle version
nb_appels_nouvelle, nb_redondances_nouvelle = 0, 0
memo_nouvelle = {}
start_time = time.time()
res_nouvelle = nouvelle_trouveExpr(cible, nombres)
time_nouvelle = time.time() - start_time

# ---------------------------- AFFICHAGE DES RÉSULTATS ----------------------------

print("\nComparaison des deux versions :")
print("--------------------------------------------------------")
print(f"Cible : {cible}")
print(f"Nombres disponibles : {nombres}\n")

print("🔴 Ancienne version :")
print(f"Solution trouvée : {res_ancienne[1]}")
print(f"Nombre total d'appels récursifs : {nb_appels_ancienne}")
print(f"Nombre de redondances constatées : {nb_redondances_ancienne}")
print(f"Temps d'exécution : {time_ancienne:.5f} secondes")

print("\n🟢 Nouvelle version :")
print(f"Solution trouvée : {res_nouvelle[1]}")
print(f"Nombre total d'appels récursifs : {nb_appels_nouvelle}")
print(f"Nombre de redondances constatées : {nb_redondances_nouvelle}")
print(f"Temps d'exécution : {time_nouvelle:.5f} secondes")

print("\n--------------------------------------------------------")

