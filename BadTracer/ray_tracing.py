## Ray Tracing: IPT Centrale 2021 ##

import math
import numpy as np
import matplotlib.pyplot as plt
import random

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

#print(color.BOLD + 'Hello World !' + color.END)

COMPTEUR_TEST = 0

# Géométrie

def vec(A, B):
    # retourne le vecteur AB
    return np.array([B[0]-A[0], B[1]-A[1], B[2]-A[2]])

def ps(v1, v2):
    return np.vdot(v1, v2)

def norme(u):
    # return np.sqrt(np.sum(u**2))
    return np.linalg.norm(u)


def unitaire(v):
    return (1/norme(v))*v


def pt(r, t):
    # prend en argument un rayon r et un réel t et calcule les cordonnées du point situé à la distance t du point S dans le direction de u
    # assert (t>=0) # trop précis ?
    epsilon = 10**-12
    assert t >= -epsilon
    (S, u) = r
    return S + t * u

def dir(A, B):
    # prend en argument 2 points et retourne le vecteur unitaire qui a même sens et direction que le vecteur AB
    return unitaire(vec(A, B))

def ra(A, B):
    # prend en argument 2 points en renvoie le rayon qui a pour origine A et comme direction AB
    return (A, dir(A, B))

def sp(A, B):
    # prend en arguments 2 points et renvoie le couple (centre, rayon) décrivant la sphère de centre A passant par B
    r = norme(vec(A, B))
    return (A, r)

def intersection(r, sphere):
    # prend en argument un rayon et une sphère et renvoie le premier point de la sphère frappé par le rayon lumineux ainsi que la distance entre ce point et l'origine du rayon. Renvoie (np.array([0.,0.,1]), -1) si le rayon ne coupe pas la shpère.
    A, u = r
    C, p = sphere
    vect = vec(C, A)
    b = 2*ps(u, vect)
    c = (norme(vect))**2 - p**2
    delta = b**2 - 4*c
    print("\nDELTA = ", delta)
    if delta<0:
        print("\nPas d'intersection avec: ", sphere)
        return (np.array([0.,0.,1.]), -1) # point du côté spectateur et "distance" négative !
    t1 = ( -b - np.sqrt(delta) ) /2
    t2 = ( -b + np.sqrt(delta) ) /2
    print("\nSolution de l'eq: ",t1, t2)
    # t = min(t1, t2) # ?
    if t1<0 and t2<0: # On élimine le cas où les deux sol sont négatives...pk? a voir test
        print("\nPas d'intersection avec: ", sphere)
        return (np.array([0.,0.,1.]), -1) # point du côté spectateur et "distance" négative !
    elif abs(t1) < abs(t2):
        t = t1
    else:
        t = t2 # ne pas prendre abs
    print("\nIntersection avec: ", sphere, "\nAu point ", pt(r, t))
    return (pt(r, t), t)

# Optique

noir = np.array([0.,0.,0.])
blanc = np.array([1.,1.,1.])

def au_dessus(sphere, P, src):
    # prend en argument une sphere, un point de la sphere et une source (un point) pour déterminer si la source est au-dessus de l'horizon du point P (ie: si elle est visible du point P)
    C, p = sphere
    u = vec(C, P)
    v = vec(P, src)
    if ps(u,v)<0: # visualiser les ps sur un schéma...
        return True
    else:
        return False

def visible(spheres, j, P, src):
    # prend en argument une liste de sphères, un entier j, un point P et une source de lumière et détermine si la source est visible depuis le point P, appartenant à la sphère spheres[j]
    sphere = spheres[j]
    vect = vec(src, P)
    distance = norme(vect)
    rayon = (src, unitaire(vect))
    if au_dessus(sphere, P, src):
        print("Au dessus de sphère ", j)
        for i in range(len(spheres)):
            if (i != j) :
                P, t = intersection(rayon, spheres[i])
                if P[2]<=0 and t<distance :
                    print("Pas visible")
                    return False
    else:
        print("\nPas visible (pas au dessus)")
        return False
    print("Visible")
    global COMPTEUR_TEST
    COMPTEUR_TEST += 1
    return True # Cassé !!! Toujours et encore !!!

def couleur_diffusee(rayon, Cs, N, kd):
    # prend en arguments un rayon, la couleur de la source, le vecteur unitaire normal à l'objet au point P et les coefficients de diffusion de l'objet et renvoie la couleur de la lumière diffusée par le point P
    S, u = rayon
    c_theta = ps(unitaire(u), unitaire(N)) # cos(theta)
    print("Cs = ", Cs)
    print("kd = ", kd)
    print("c_theta = ", c_theta)
    #Cd = (kd*Cs)*abs(c_theta) # abs pour éviter les c_theta négatifs qui font du noir sur l'image
    Cd = (kd*Cs)*c_theta
    print("Cd = ", Cd)
    return Cd

def rayon_reflechi(sphere, P, src):
    # prend en arguments une sphere, un point de la sphère et une source lumineuse et retourne le rayon réfléchi par le point P (on suppose que la source est visible depuis P)
    # http://gregory.corgie.free.fr/currentDotclear/index.php?post/2007/01/02/7--raytracing-lecon-4-les-lois-de-descartes
    C,p = sphere
    N = unitaire(vec(C, P)) # optimisation -> enlever les unitaires?
    u = unitaire(vec(src, P))
    w = unitaire(u-2*ps(u,N)*N)
    print("\nRayon incident: ", u )
    print("Rayon réflechi: ", w )
    return (P,w)

# Lancer de Rayons

Objet = [(np.array([0,10,-10]),4), (np.array([0,-10,-10]),4), (np.array([-10,0,-10]),6), (np.array([8,0,-5]),4)] # Liste de sphères

KdObj = [np.array([0.9,0.1,0.1]), np.array([0.1,0.9,0.1]), np.array([0.1,0.1,0.9]), np.array([0.9,0.1,0.1])] # Liste des coef. de diffusion des sphères

Source = [np.array([10,10,-1]), np.array([-10,10,-1])] # Liste des sources de lumière

ColSrc = [np.array([0.99,0.99,0.99]), np.array([0.99,0.99,0.99])] # Liste des couleurs des sources

Delta = 20 # Largeur de l'écran

N = 80 # Nbr de pixel ( écran considéré -> (NxN) )

def grille(i, j):
    # prend en argument deux entiers et renvoie les coord. cartésiennes du point E (centre de la case repérée par (i,j) )
    pixelSize = Delta / N
    unit = pixelSize / 2
    milieu = N / 2
    x = (j - milieu + 0.5)*pixelSize
    y = -(i - milieu + 0.5)*pixelSize
    return (x,y,0)

def rayon_ecran(omega, i, j):
    # prend en argument un point omega et deux entiers i et j et renvoie le rayon issu du point omega passant par (i,j)
    E = grille(i, j)
    return (omega, dir(omega, E))

def interception(rayon):
    # prend en argument un rayon et renvoie le premier point matériel de la scène atteint par ce rayon ainsi que l'indice de la sphère concernée dans la liste Objet. Si le rayon n'intercepte aucune sphère, renvoie ([0,0,1], -1).
    if len(Objet) > 0 :
        #print("\nIl y a au moins une sphère")
        fP, ft = intersection(rayon, Objet[0])
        print(ft)
        print(fP[2], fP[2])
        indice = 0
        if fP[2]>0:
            indice = -1 # pour mieux repérer les non interceptions
        for i in range(1, len(Objet)):
            P, t = intersection(rayon, Objet[i])
            print(t)
            print(P[2], fP[2])
            if P[2]<=0: # ie: si il y a une réelle intersection
                if fP[2]>0:
                    fP = P
                    indice = i
                elif P[2]>fP[2]:
                    fP = P
                    indice = i
        if indice == -1:
            print("\nAucune sphère sur le trajet du rayon")
        else:
            print("\nPremier point matériel rencontré: ", fP, " sur la sphère d'indice ",indice)
        return (fP, indice)
    else:
        print("\nAucune sphère dans la scène\n")

def couleur_diffusion(P, j):
    # prend en argument un point P appartenant à la sphère Objets[j] et renvoie la couleur diffusée par le point P. Si aucune source n'éclaire P, la fonction renvoie du noir.
    couleurs = []
    C, p = Objet[j]
    for i in range(len(Source)):
        couleurDiff = noir
        source = Source[i]
        if visible(Objet, j, P, source):
            rayon_source = (source, dir(source, P))
            N = dir(C, P)
            couleurDiff = couleur_diffusee(rayon_source, ColSrc[i], N, KdObj[j] )
            print("1",couleurDiff)
        """
        print("LALA")
        rayon_source = (source, dir(source, P))
        N = dir(C, P)
        couleurDiff = couleur_diffusee(rayon_source, ColSrc[i], N, KdObj[j] )
        """
        couleurs.append(couleurDiff) # attention quand il y a plusieurs sources lumineuses

    #couleurDiff = noir
    couleurDiff = np.array([0.,0.,0.])
    print("2",couleurDiff)
    print("Liste -> ", couleurs)
    for k in range(len(couleurs)):
        couleurDiff += couleurs[k]
        print(k, couleurDiff)
    print(couleurDiff)
    return couleurDiff

omega = np.array([0,0,10])
fond = np.array([0.85,0.85,0.85])

##

def lancer(omega, fond):
    # prend en argument un point et une couleur et renvoie l'image associée à la scène dans un tableau de dimension NxNx3. Si un rayon n'intercepte aucun objet, le pixel correspondant est de la couleur du fond.
    im = np.empty((N,N,3))
    for i in range(N):
        for j in range(N):
            print(color.BOLD + "\n======================================" + color.END)
            print(color.BOLD + "\nLancer de rayon: " + color.END, i,"x",j)
            rayon = rayon_ecran(omega, i, j)
            print("\nRayon lancé: ", rayon)
            P, indice = interception(rayon)
            if P[2]>0:
                couleur = fond
                print("\nCouleur pixel: ", couleur, "(FOND)")
            else:
                print(color.BOLD + "\nCalcul de la couleur:" + color.END)
                couleur = couleur_diffusion(P, indice)
                print("\nCouleur pixel: ", couleur,color.RED + "[PAS FOND]" + color.END)
            im[i, j] = couleur
    return im

image = lancer(omega, fond)

## AFFICHAGE ##

RT=plt.figure("RAY TRACING",figsize = (9, 9))
plt.gcf().subplots_adjust(left = 0.1, bottom = 0.1,right = 0.98, top = 0.9, wspace = 0.4, hspace = 0.4)


ax = RT.add_subplot(1, 2, 1)

plt.imshow(image)

#imageT = np.array(image,np.int32)
#plt.imshow(imageT)

#plt.imshow((image * 255).astype(np.uint8))

#plt.imshow(image.astype('uint8'))

plt.title("Image Générée")
plt.axis("off")

ax = RT.add_subplot(1,2,2)
def couleur_de_fond(fond):
    nbr_lin, nbr_col = 3, 1
    im = np.empty((nbr_lin,nbr_col,3))
    for i in range(nbr_lin):
        for j in range(nbr_col):
            im[i, j] = fond
    return im
plt.imshow(couleur_de_fond(fond))
plt.title("Couleur de Fond")
plt.axis("off")

plt.show()

##

# Améliorations

KrObj = [0.5, 0.5, 0.25, 0.5]

rmax = 3

def interception_pro(rayon, ind):
    # prend en argument un rayon et renvoie le premier point matériel de la scène atteint par ce rayon ainsi que l'indice de la sphère concernée dans la liste Objet. Si le rayon n'intercepte aucune sphère, renvoie ([0,0,1], -1).
    # ne prend pas en compte les collision avec la sphère d'origine d'un rayon réfléchi.
    if len(Objet) > 0 :
        if ind != 0:
            fP, ft = intersection(rayon, Objet[0])
            print(ft)
            print(fP[2], fP[2])
            indice = 0
        else:
            fP, ft = intersection(rayon, Objet[1])
            print(ft)
            print(fP[2], fP[2])
            indice = 1
        if fP[2]>0:
            indice = -1 # pour mieux repérer les non interceptions
        for i in range(1, len(Objet)):
            if i != ind:
                P, t = intersection(rayon, Objet[i])
                print(t)
                print(P[2], fP[2])
                if P[2]<=0: # ie: si il y a une réelle intersection
                    if fP[2]>0:
                        fP = P
                        indice = i
                    elif P[2]>fP[2]:
                        fP = P
                        indice = i
        if indice == -1:
            print("\nAucune sphère sur le trajet du rayon")
        else:
            print("\nPremier point matériel rencontré: ", fP, " sur la sphère d'indice ",indice)
        return (fP, indice)
    else:
        print("\nAucune sphère dans la scène\n")


def reflexion(rayon, remaining_ref, rmax, ind):
    # prend en argument un rayon et un entier rmax et renvoie la liste des couples (P, i) correspondants aux points successivement rencontrés par la rayon au fur et à mesure de ses réflexions (au plus rmax réflexions). ( P désignant le point où à lieu la réflexion et i l'indice de l'objet)
    print("\nRéflexions restantes: ", rmax )
    print("\nOn suit désormais le rayon: ", rayon)
    src, u = rayon
    res = []
    if remaining_ref == rmax:
        P, i = interception(rayon)
        res.append( (P, i) )
        res += reflexion(rayon_reflechi(Objet[i], P, src), remaining_ref-1, rmax, i)
    elif remaining_ref > 0 :
        P, i = interception_pro(rayon, ind)
        res.append( (P, i) )
        res += reflexion(rayon_reflechi(Objet[i], P, src), remaining_ref-1, rmax, i)
    return res


"""
def reflexion(rayon, rmax):
    # prend en argument un rayon et un entier rmax et renvoie la liste des couples (P, i) correspondants aux points successivement rencontrés par la rayon au fur et à mesure de ses réflexions (au plus rmax réflexions). ( P désignant le point où à lieu la réflexion et i l'indice de l'objet)
    print("\nRéflexions restantes: ", rmax )
    print("\nOn suit désormais le rayon: ", rayon)
    src, u = rayon
    res = []
    if rmax > 0 :
        P, i = interception(rayon)
        res.append( (P, i) )
        res += reflexion(rayon_reflechi(Objet[i], P, src), rmax-1)
    return res
"""

def couleur_percue(rayon, rmax, fond):
    print("\nCalcul des points de réflexions:")
    liste = reflexion(rayon, rmax, rmax, -1)
    print("\nPoints de réflexions: ", liste)
    couleur = np.array([0.,0.,0.])
    for j in range(len(liste)-1,-1,-1):
        P, i = liste[j]
        couleur = couleur_diffusion(P, i) + KrObj[i] * couleur
    return couleur

def lancer_complet(omega, fond):
    # prend en argument un point et une couleur et renvoie l'image associée à la scène dans un tableau de dimension NxNx3 en prenant en compte les diffusions et les réflexions. Si un rayon n'intercepte aucun objet, le pixel correspondant est de la couleur du fond.
    im = np.empty((N,N,3))
    for i in range(N):
        for j in range(N):
            print(color.BOLD + "\n======================================" + color.END)
            print(color.BOLD + "\nLancer de rayon: " + color.END, i,"x",j)
            rayon = rayon_ecran(omega, i, j)
            print("\nRayon lancé: ", rayon)
            P, indice = interception(rayon)
            if P[2]>0:
                couleur = fond
                print("\nCouleur pixel: ", couleur, "(FOND)")
            else:
                print(color.BOLD + "\nCalcul de la couleur:" + color.END)
                couleur = couleur_percue(rayon, rmax, fond)
                print("\nCouleur pixel: ", couleur,color.RED + "[PAS FOND]" + color.END)
            im[i, j] = couleur
    return im


image = lancer_complet(omega, fond)

## AFFICHAGE ##

RT=plt.figure("RAY TRACING",figsize = (9, 9))
plt.gcf().subplots_adjust(left = 0.1, bottom = 0.1,right = 0.98, top = 0.9, wspace = 0.4, hspace = 0.4)


ax = RT.add_subplot(1, 2, 1)

plt.imshow(image)

#imageT = np.array(image,np.int32)
#plt.imshow(imageT)

#plt.imshow((image * 255).astype(np.uint8))

#plt.imshow(image.astype('uint8'))

plt.title("Image Générée")
plt.axis("off")

ax = RT.add_subplot(1,2,2)
def couleur_de_fond(fond):
    nbr_lin, nbr_col = 3, 1
    im = np.empty((nbr_lin,nbr_col,3))
    for i in range(nbr_lin):
        for j in range(nbr_col):
            im[i, j] = fond
    return im
plt.imshow(couleur_de_fond(fond))
plt.title("Couleur de Fond")
plt.axis("off")

plt.show()
