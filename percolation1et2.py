import numpy as np
import matplotlib.pyplot as plt 

#Création d'une matrice NxN avec des nombres aléatoires entre 0 et 1 
#puis transformation de la matrice en matrice de booléens grace à p. 

def generation_grille(N,p):
    grille = np.random.random((N,N)) < p
    return grille 

#test de la fonction generation de la grille avec N = 5, p = 0.6 

grille_test = generation_grille(5,0.6)
print(grille_test)

#verification de la proportion des sites occupés

print(np.mean(generation_grille(100,0.6)))

#Creation d'une fonction pour afficher la grille avec matplotlib

def afficher_grille(grille):
    plt.imshow(grille, cmap = "gray_r")
    plt.axis("off")
    plt.show()

#tester la génération de grille N = 100, p = 0.6

grille06 = generation_grille(100,0.6)
afficher_grille(grille06)

# génération de grille N = 100, p = 0.2

grille02 = generation_grille(100,0.2)
afficher_grille(grille02)

# génération de grille N = 100, p = 0.01

grille001 = generation_grille(100,0.01)
afficher_grille(grille001)

# génération de grille N = 20, p = 0.5

grille20_05 = generation_grille(20,0.5)
afficher_grille(grille20_05)

#fonction permettant de donner les voisins valides cad les voisins qui existent vraiment car aux frontieres de la grille on a pas forcement 4 voisins donc il faut que les voisins restent dans les coordonnes de la grille pour pouvoir etre comptes comme voisins. 
#Remarque : Je ne compte pas les voisins diagonaux car pas précisé dans l'énoncé

def voisins(i,j,N):
    candidats = [(i-1,j), (i+1,j), (i, j-1), (i,j+1)]
    voisins_valides = []

    for a, b in candidats:
        if 0 <= a < N and 0 <= b < N:
            voisins_valides.append((a,b))
    return voisins_valides

#Test de la fonction voisins sur un site à la frontière de la grille

print(voisins(0,0,5))

#sur une coordonnee aleatoire 

print(voisins(2,3,10))

#Coder une fonction pour explorer un amas

def exploration_amas(grille,depart,visites):
    N = grille.shape[0] #taille de la grille

    pile = [depart] #site de départ
    amas = [] #coordonnées des sites qui créent un amas avec le site depart

    visites.add(depart) #liste avec les sites déjà controlés pour ne pas les recontroler une seconde fois

    while pile: 
        i,j = pile.pop() 
        amas.append((i,j))

        for a,b in voisins(i,j,N): #controle des voisins du site observé
            if grille[a,b] and (a,b) not in visites: #test si le site voisin considéré et vide ou pas et si on l'a pas déjà controlé
                visites.add((a,b)) 
                pile.append((a,b))

    return amas
    

#Nous souhaitons maintenant détecter TOUS les amas présents dans la grille.

def trouver_amas(grille):
    N = grille.shape[0]
    visites = set() #creation d'un ensemble des sites déjà visités (ne contient pas de doublons, car set)
    liste_amas = [] #liste pour stocker les amas trouvés

    for i in range(N):
        for j in range(N): #pour chaque ligne i on parcourt toutes les colonnes j 
            if grille[i,j] and (i,j) not in visites: #vérifie si le site i,j est occupé ou non et s'il a déjà été visité ou non
                amas = exploration_amas(grille, (i,j),visites) #si c'est le cas, i,j et le début d'un nouvel amas et on utilise la fonction exploration_amas pour cartographier l'amas
                liste_amas.append(amas) #on ajoute l'amas cartographié de départ i,j à la liste qui repère les amas

    return liste_amas
  
#Test simple de la fonction trouver_amas

grille_test = np.array([[1,1,0,0],
                        [0,1,0,1],
                        [0,0,0,1],
                        [1,0,0,0]], dtype = bool)

amas = trouver_amas(grille_test)

for a in amas: 
    print(a, "taille de l'amas =", len(a))


#On souhaite désormais tester la percolation verticale (donc s'il existe un amas qui touche la ligne du haut et du bas), la percolation horizontale (donc si un amas touche la colonne de gauche et la colonne de droite), puis tester si la grille percole (donc soit on a percolation horizontale ou percolation verticale)

def amas_percole_verticalement(amas, N):
    touche_haut = False
    touche_bas = False

    for i, j in amas: 
        if i == 0:
            touche_haut = True
        if i == N-1:
            touche_bas = True
    
    return touche_haut and touche_bas

def amas_percole_horizontalement(amas, N):
    touche_gauche = False
    touche_droite = False

    for i, j in amas: 
        if j == 0:
            touche_gauche = True
        if j == N-1:
            touche_droite = True
    
    return touche_gauche and touche_droite


def percole(grille):
    N = grille.shape[0]
    liste_amas  = trouver_amas(grille)

    for amas in liste_amas:
        if amas_percole_verticalement(amas,N) or amas_percole_horizontalement(amas,N):
            return True
    
    return False


#Test d'une percolation evidente 

grille_vert = np.array([[0,1,0,0,0],
                        [0,1,0,0,0],
                        [0,1,0,0,0],
                        [0,1,0,0,0],
                        [0,1,0,0,0]], dtype=bool)

print(percole(grille_vert))

#Test d'une non percolation evidente 

grille_non = np.array([[0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0],
                        [0,0,0,0,0]], dtype=bool)

print(percole(grille_non))

#Test sur une diagonale (donc non percolante)

grille_diag = np.array([[1,0,0,0,0],
                        [0,1,0,0,0],
                        [0,0,1,0,0],
                        [0,0,0,1,0],
                        [0,0,0,0,1]], dtype = bool)

print(percole(grille_diag))


#On teste notre algorithme de détection de percolation sur des valeurs p différentes

pc = 0.592746

for p in [0.2,0.6,pc, 0.8]:
    grille = generation_grille(50,p)
    afficher_grille(grille)
    print("p=", p, "Est ce qu'elle percole ?", percole(grille))
  

#PARTIE 2 DU PROJET - étude de la percolation en fonctionde p pour N fixé 

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

#On voit bien sur le graphique que la proba de percolation est nulle jusqu'à pas loin avant pc puis au seuil critique la proba augmente drastiquement et "saute" vers proba = 1 où elle se stabilise.


#on voit déjà sur la courbe que le seuil critique pc colle bien, on souhaite désormais estimer ce seuil critique à N fixé
