# Projet-comondo

PARTIE 2 DU PROJET - étude de la percolation en fonctionde p pour N fixé 

# on va coder une fonction qui estime la proba de percolation pour un p donné
#pour cela on va créer : une liste de valeurs de p à tester, on calcule proba de perc pour chaque p et on fait un grafique puis une estimation numérique approx de p_c


#fonction qui estime la proba de percolation 

def proba_percolation(N,p,nb_repetitions):
    compteur_percolation = 0 

    for k in range(nb_repetitions):
        grille = generation_grille(N,p) #creations de grilles NxN à proba p aléatoires

        if percole(grille): #voir si les grilles percoles si oui on augmente le compteur
            compteur_percolation += 1

    proba = compteur_percolation/nb_repetitions
    return proba



    #Test de la fonction proba_percolation

N=100
repets = 150

print("p=0.2 :", proba_percolation(N,0.2,repets))
print("p=0.7 :", proba_percolation(N,0.7,repets))


#calcul de la proba de percolation pour plusieurs valeurs de p 

N = 100
repets = 150
valeurs_p = np.linspace(0,1,100)

probabilites = []


for p in valeurs_p:
    proba = proba_percolation(N,p,repets)
    probabilites.append(proba)
    print("p=",round(p,4),"probabilité de percolation=", proba)




#tracer la courbe proba percolation en fonction de p 

plt.plot(valeurs_p, probabilites)
plt.axvline(0.592746, linestyle = "--", label = "seuil critique théorique")
plt.xlabel("Probabilité d'occupation p")
plt.ylabel("Probabilité de percolation")
plt.title(f"Probabilité de percolation pour un réseau {N} x {N}, {repets} répétitions")
plt.legend()
plt.show()



#On affine la courbe pour voir mieux

N = 100
repets = 300
valeurs_p_affine = np.linspace(0.54,0.46,101)

probas_affines = []

for p in valeurs_p_affine:
    proba = proba_percolation(N,p,repets)
    probas_affines.append(proba)

plt.plot(valeurs_p_affine, probas_affines)
plt.axvline(0.592746,linestyle = "--",label = "seuil critique théorique")
plt.xlabel("Probabilité d'occupation p")
plt.ylabel("Probabilité de percolation")
plt.title(f"Transition de percolation autour de pc pour un réseau {N}x{N}, {repets} répétitions")
plt.legend()
plt.grid()
plt.show()


#On voit bien sur le graphique que la proba de percolation est nulle jusqu'à pas loin avant pc puis au seuil critique la proba augmente drastiquement et "saute" vers proba = 1 où elle se stabilise.


#on voit déjà sur la courbe que le seuil critique pc colle bien, on souhaite désormais estimer ce seuil critique à N fixé

probabilites_array = np.array(probabilites) #on transforme la liste en tableau np pour pouvoir faire des opérations mathématiques directs sur les elements 
indice_pc = np.argmin(np.abs(probabilites_array - 0.5)) #On cherche la valeur critique de p cad la valeur où environ 50% des grilles percolent donc on mesure l'écart entre chaque proba de perc et 0.5 puis avec argmin on trouve l'indice de probabilite de perc la plus proche de 0.5
estimation_pc = valeurs_p[indice_pc] #récupération de la valeur p correspondante

print("Estimation de pc pour N =", N, ":", estimation_pc)
print("Valeur théorique pour le réseau carré :", 0.592746)






