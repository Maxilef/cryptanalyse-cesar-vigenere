import os
from random import randint

from syntaxe import *



def cesar(chaine):
    """
    chiffrement cesar avec une demande de cle
    """

    cle = int(input("entrer une clé pour chiffrement cesar :"))

    if cle < 0 :
        cle = randint(1,25)
        print("la cle est ",cle)

    chaine = traitementChaine(chaine)
    resultat = ""
    for caractere in chaine:
        decalage = 65
        caractere_chiffre = chr((ord(caractere) - decalage + cle) % 26 + decalage)
        resultat += caractere_chiffre
    return resultat

def new_cesar(chaine,cle):
    """
    chiffrement cesar avec cle en parametre
    la fonction cesar n'a pas était mis a jour voici donc une nouvelle version
    """
    if isinstance(cle,str):
        cle = traitementChaine(cle)
        cle = ord(cle)-65

    chaine = traitementChaine(chaine)
    resultat = ""
    for caractere in chaine:
        decalage = 65
        caractere_chiffre = chr((ord(caractere) - decalage + cle) % 26 + decalage)
        resultat += caractere_chiffre
    return resultat

def decesar(chaine,cle):
    """
    dechiffrement cesar
    """

    chaine = traitementChaine(chaine)
    resultat = ""
    for caractere in chaine:
        decalage = 65
        caractere_chiffre = chr((ord(caractere) - decalage - cle) % 26 + decalage)
        resultat += caractere_chiffre
    return resultat

def lire_fichier_to_chaineV2(name_file) :
    """
    lit un fichier dans le repertoire courant et retourne chaine
    """

    with open(name_file, 'r') as fichier:
        lignes = fichier.read()

    return lignes

def write_cesar_file():
    """
    lit un fichier In.txt et applique le chiffrement cesar et écrie le resultat dans un
    """

    # fichier d'entrée/sortie
    file_in = "In.txt"
    file_out = "Out.txt"
    nom_dossier_sortie = "cesar"

    # fichier de sortie par defaut
    nom_fichier_entree = os.path.join(nom_dossier_sortie, file_in)
    nom_fichier_sortie = os.path.join(nom_dossier_sortie, file_out)

    # verifier si le fichier de sortie existe, sinon le créer
    if not os.path.exists(nom_fichier_sortie):
        open(nom_fichier_sortie, 'w').close()

    # save le résultat dans Out.txt
    with open(nom_fichier_sortie, 'w') as fichier_sortie:
        res_cesar = cesar(lire_fichier_to_chaineV2(nom_fichier_entree))
        fichier_sortie.write(res_cesar)

    print("Traitement terminé. Résultat sauvegardé dans", nom_fichier_sortie)

def coincidence(chaine):
    """
    effectue le test de l'indice de coïncidence sur une chaine en entrée
    """

    chaine = traitementChaine(chaine)

    total = len(chaine)
    ic = 0.0
    for lettre in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        ni = chaine.count(lettre)
        ic += (ni * (ni - 1)) / (total * (total - 1))
    return ic

def cryptanalyseCesar(texte_chiffre,freq_lettres_francais):
    """
    renvoie la clé de chiffrement de César en application la cryptanalyse du chiffrement cesar
    """

    texte_chiffre = traitementChaine(texte_chiffre)
    longueur_texte = len(texte_chiffre)

    meilleure_cle = 0
    meilleur_score = float('inf')

    for cle in range(26):
        score = 0
        texte_dechiffre = decesar(texte_chiffre,cle)

        # Calculer le score en comparant les fréquences avec les fréquences théoriques
        # parcour de tous le dico des lettes fr
        for lettre in freq_lettres_francais :
            freq_obs = texte_dechiffre.count(lettre) / longueur_texte
            freq_attendue = freq_lettres_francais[lettre]
            score += (freq_obs - freq_attendue) ** 2 #on met au care pour eviter les écart avec les negatifs
            # la freq la plus petite gagne

        if score < meilleur_score:
            meilleur_score = score
            meilleure_cle = cle

    return meilleure_cle


if __name__ == "__main__":

    # on chiffre un message
    write_cesar_file()

    # recup des freqde lettre d'apres victor hugo
    freq_lettres_francais = frequences(nb_apparitions(lire_fichier_to_chaineV2("./OUT/93Out.txt")))

    # on recupere le texte qu l'on veut dechiffrer
    ciphertext = lire_fichier_to_chaineV2("./cesar/Out.txt")

    # on trouve la clé
    cle = cryptanalyseCesar(ciphertext,freq_lettres_francais)

    # le texte chiffer
    print("le texte a dechiffrer : ", ciphertext)

    # afficher la clé trouvée
    print("Clé de chiffrement de César : ", cle)

    # déchiffrer le texte avec la clé trouvée
    texte_dechiffre = decesar(ciphertext, cle)
    print("Texte déchiffré : ", texte_dechiffre)



