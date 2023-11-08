from syntaxe import *
from cesar import *
from math import sqrt


def fractionne(chaine, pas):
    """
    prend une chaine en entré et fractionne celle ci selon le pas en entrée
    """

    chaine = traitementChaine(chaine)
    sous_chaines = []

    for i in range(pas):
        sous_chaine = chaine[i::pas]
        sous_chaines.append(sous_chaine)

    print(sous_chaines)
    return sous_chaines




def recolle(sous_chaines):
    """
    permet de recolé aprés un fractionnement des sous chaine
    """

    # on prend la longeur de la sous chaine la plus grande
    longueur_max = 0
    for sous_chaine in sous_chaines:
        longueur_max = max(longueur_max, len(sous_chaine))

    chaine_recollee = ""
    for i in range(longueur_max):
        for chaine in sous_chaines:
            if i < len(chaine):
                chaine_recollee += chaine[i]

    return chaine_recollee




def chiffrement(chaine,cle) :
    """
    chiffrement de vigenaire
    """

    chaine = traitementChaine(chaine)

    taille_cle = len(cle)
    sous_chaines = fractionne(chaine,taille_cle)

    sous_chaines_cesar = []
    for i in range(len(sous_chaines)) :

        sous_chaines_cesar += [new_cesar(sous_chaines[i],cle[i])]

    chaine_recollee = recolle(sous_chaines_cesar)

    return chaine_recollee


def dechiffrement(chaine,cle) :
    """
    dechiffrement de vegenere avec une clé donner en entrée
    """

    chaine = traitementChaine(chaine)

    taille_cle = len(cle)

    sous_chaines = fractionne(chaine,taille_cle)

    sous_chaines_cesar = []
    for i in range(len(sous_chaines)) :
        sous_chaines_cesar += [decesar(sous_chaines[i],ord(cle[i])-65)]

    chaine_recollee = recolle(sous_chaines_cesar)

    return chaine_recollee


def calculIC(chaine, pas):
    """
    calcule et renvoie la moyenne des indices de coïncidence de toutes ces sous-chaînes.
    """

    # les sous-chaînes avec fractionne
    sous_chaines = fractionne(chaine, pas)

    # calcule l'IC moyen pour toutes les sous-chaînes
    ic_total = 0
    for sous_chaine in sous_chaines :
        ic_total += coincidence(sous_chaine)

    ic_moyen = ic_total / pas

    return ic_moyen



def tailleCle(chaine_chiffree, seuil=0.065):
    """
    Détermine la longueur de la clé en se basant sur l'indice de coïncidence global.
    """

    meilleure_hypothese = 1
    meilleur_ic_global = 0

    # parcours les longueurs de clé possibles
    for longueur_cle in range(1, len(chaine_chiffree) + 1):

        ic_moyen = calculIC(chaine_chiffree, longueur_cle)

        # si l'IC global dépasse le seuil actuel MAJ
        if ic_moyen > meilleur_ic_global:
            meilleur_ic_global = ic_moyen
            meilleure_hypothese = longueur_cle

        # si l'IC global > seuil on l'arrête
        if ic_moyen > seuil:
            break

    return meilleure_hypothese


def positions_des_sequences_repetees(texte, longueur_sequence):
    """
    Recherche les séquences répétées dans un texte donné et retourne leurs positions.
    """

    positions_sequences = {}

    for i, caractere in enumerate(texte):
        sequence_suivante = texte[i:i+longueur_sequence]

        # Vérifier si la séquence existe déjà dans le dictionnaire
        if sequence_suivante in positions_sequences.keys():
            positions_sequences[sequence_suivante].append(i)
        else:
            positions_sequences[sequence_suivante] = [i]

    sequences_repetees = list(filter(lambda x: len(positions_sequences[x]) >= 2, positions_sequences))
    sequences_positions_repetees = [(sequence, positions_sequences[sequence]) for sequence in sequences_repetees]

    return sequences_positions_repetees

def obtenir_ecarts(positions):
    """
    Cette fonction calcule les écarts entre les positions dans une liste de positions.
    """
    ecarts = []
    for i in range(len(positions) - 1):

        # calculer écart entre la position suivante et la position actuelle
        ecart = positions[i + 1] - positions[i]
        ecarts.append(ecart)

    return ecarts

def obtenir_facteurs(nombre):
    """
    Trouve les facteurs d'un nombre donné.
    """

    facteurs = set()
    for i in range(1, int(sqrt(nombre)) + 1):
        if nombre % i == 0:
            facteurs.add(i)
            facteurs.add(nombre // i)

    #print("obtenir facteur :",sorted(facteurs))
    return sorted(facteurs)

def longueurs_cle_candidates(listes_facteurs, longueur_max):
    """
    Cette fonction identifie les longueurs de clé candidates à partir de listes de facteurs.
    """

    tous_les_facteurs = []

    for lst in listes_facteurs:
        for fac in lst:
            tous_les_facteurs.append(fac)

    # exlcure les facteurs plus grands que la longueur de clé maximale
    longueurs_candidates = list(filter(lambda x: x <= longueur_max, tous_les_facteurs))

    # trier les longueurs candidates par probabilité (descendante)
    longueurs_triees = sorted(set(longueurs_candidates), key=lambda x: tous_les_facteurs.count(x), reverse=True)

    return longueurs_triees

def kasiski(texte_chiffre, longueur_sequence, longueur_max):
    """
    Applique la méthode de Kasiski pour estimer la longueur de la clé utilisée pour chiffrer un texte.
    """

    # trouver les séquences répétées et leurs positions
    p_s_r = positions_des_sequences_repetees(texte_chiffre,longueur_sequence)

    sequences_espacements = {}
    for sequence, positions in p_s_r:
      sequences_espacements[sequence] = obtenir_ecarts(positions)

    # calculer les espacements entre les positions de chaque séquence répétée
    # et factoriser les espacements
    listes_facteurs = []
    for espacements in sequences_espacements.values():
      for espace in espacements:
          listes_facteurs.append(obtenir_facteurs(espace))

    # obtenir les facteurs communs par fréquence décroissante,
    # qui constituent les longueurs de clé candidates
    #print(listes_facteurs)
    longueurs_cle_candidats = longueurs_cle_candidates(listes_facteurs, longueur_max)
    return longueurs_cle_candidats

def convertir_en_ascii(liste_entiers):
    # Utilisation de la fonction chr() pour convertir chaque entier en caractère ASCII
    caracteres_ascii = [chr(entier + ord('A')) for entier in liste_entiers]
    return ''.join(caracteres_ascii)


def decrypter(texte_chiffre):
    cle_ic = tailleCle(texte_chiffre, 0.065)

    sous_chaines = fractionne(texte_chiffre,cle_ic)

    # recup des frequence des lettre d'apres victor hugo
    freq_lettres_francais = frequences(nb_apparitions(lire_fichier_to_chaineV2("./OUT/93Out.txt")))

    cle_trouver = []
    for sous_chaine in sous_chaines :

        # on trouve la clé et l'ajoute a la liste des cles trouver
        cle_trouver += [cryptanalyseCesar(sous_chaine,freq_lettres_francais)]

    # on converti les int en lettre/mot
    cle_final = convertir_en_ascii(cle_trouver)
    # dechiffrement vigenere
    texte_claire = dechiffrement(texte_chiffre,cle_final)
    return texte_claire

def ecrire_dans_fichier(texte, nom_fichier_sortie):
    try:
        with open(nom_fichier_sortie, 'w') as fichier:
            fichier.write(texte)
        print(f"Le texte a été écrit dans le fichier {nom_fichier_sortie}.")
    except IOError as e:
        print(f"Erreur lors de l'écriture dans le fichier {nom_fichier_sortie}: {e}")



if __name__ == "__main__":


    fichier_de_sortit = "93Out.txt"

    chaine = "abcdefghijklmnop"

    print("\nchiffrement du texte 93.txt\n")

    cle = "azerty"
    chiffre_93 = chiffrement(chaine,cle)
    print(f"chiffrement avec {cle}: {chiffre_93}\n")

    ecrire_dans_fichier(chiffre_93,"OUT/chiffreOutvi.txt")


    #écrire texte chiffre dans un fichier

    print("histogramme\n")

    fichier_de_sortit_crypted = "chiffreOutvi.txt"

    #calcul nb apparition crypte
    fichier = lire_fichier_apparition(fichier_de_sortit_crypted)

    #calcule des frequences crypté
    frequence = frequences(fichier)

    #écrire les freq dans un fichier
    write_frequences_in_file(frequence, "freq_Outvi.txt")

    #Créeation histogrammes
    histogrammes("freq_Outvi.txt",fichier_de_sortit_crypted)

    #création histogramme digramme
    res_nb_digrammes = nb_digrammes(chiffre_93)

    histogrammes_ord_bigrammes(res_nb_digrammes)
