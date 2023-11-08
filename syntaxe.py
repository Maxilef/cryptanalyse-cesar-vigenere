import os
import matplotlib.pyplot as plt


def affiche_ascci_MAJ():
    """
    # Affiche le code ASCII des majuscules

    les majuscules selon la table ASCII vont de 65 a 91
    on vas donc parcourir ces valeurs et afficher leurs char correspondant
    """
    print("Code ASCII des majuscules:")
    for lettre in range(ord('A'), ord('Z')):
        print(f"{chr(lettre)} : {lettre}")


def affiche_ascii_table():
    """
    Affiche la table des 128 codes ASCII
    on parcour simplement les 128 premier ASCII
    """
    print("\nTable des 128 codes ASCII:")
    for code in range(128):
        print(f"{code} : {chr(code)}")

def ecrire_dans_fichier(texte, nom_fichier_sortie):
    try:
        with open(nom_fichier_sortie, 'w') as fichier:
            fichier.write(texte)
        print(f"Le texte a été écrit dans le fichier {nom_fichier_sortie}.")
    except IOError as e:
        print(f"Erreur lors de l'écriture dans le fichier {nom_fichier_sortie}: {e}")


def traitementChaine(chaine):
    """
    Cnvertion d'une chaine de caractere en une chaine en majuscule, sans accent et sans espace
    """
    # Convertir la chaîne en minuscules
    chaine = chaine.lower()

    # Créer un dictionnaire de correspondance des caractères accentués
    dico_accent = {
        'à': 'a',       'â': 'a',       'ä': 'a',
        'é': 'e',       'è': 'e',       'ê': 'e',       'ë': 'e',
        'î': 'i',       'ï': 'i',
        'ô': 'o',       'ö': 'o',
        'ù': 'u',       'û': 'u',       'ü': 'u',
        'ç': 'c',
    }

    # Remplacer les caractères accentués par leurs équivalents non accentués
    for accentue, non_accentue in dico_accent.items():
        chaine = chaine.replace(accentue, non_accentue)

    # Éliminer les caractères non alphanumériques (espaces, ponctuation, chiffres, etc.)
    chaine = ''.join(caractere for caractere in chaine if caractere.isalpha())

    # Convertir la chaîne en majuscules
    chaine = chaine.upper()

    return chaine

def traitementChaine_input():
    """
    demande entré d'une chaine de caractere
    """
    chaine = input("entrer une chaine de caractere")
    res_traitement_chaine = traitementChaine(chaine)
    return res_traitement_chaine

def open_write_file_forTraitement(name_file,name_file_out):
    """
     lit un fichier txt et le convertit en une chaine de caractere special avec fonction
     traitementChaine et retourne un fichier txt en sorit avec la convertion

     Q1.2.4 : wc -m 93Out.txt = 532873
     """

    # ouvrir et lire le fichier d'entrée
    nom_fichier_entree = str(name_file)

    with open(nom_fichier_entree, 'r') as fichier_entree:
        contenu = fichier_entree.read()

    # appliquer le traitement à la chaîne lue
    contenu_traite = traitementChaine(contenu)

    # nom du fichier de sortie par default
    nom_dossier_sortie = "OUT"
    nom_fichier_sortie = os.path.join(nom_dossier_sortie, name_file_out)

    # verifier si le fichier de sortie existe, sinon le créer
    if not os.path.exists(nom_fichier_sortie):
        open(nom_fichier_sortie, 'w').close()

    # Save le résultat dans 93Out.txt
    with open(nom_fichier_sortie, 'w') as fichier_sortie:
        fichier_sortie.write(contenu_traite)

    print("Traitement terminé. Résultat sauvegardé dans", nom_fichier_sortie)

def nb_apparitions(chaine):
    """
    compte le nombre d'occurance de chaque lettre dans une chaine de caractere
    """

    dico_apparitions = {}
    for lettre in chaine :
        if 'A' <= lettre <= 'Z' :
            if lettre in dico_apparitions :
                dico_apparitions[lettre] += 1
            else :
                dico_apparitions[lettre] = 1

    # tri du dico par ordre alphabetique
    dico_apparitions_tri = {lettre: dico_apparitions[lettre] for lettre in sorted(dico_apparitions.keys())}

    return dico_apparitions_tri

def frequences(dico):
    """
    Retounre les frequences d'apparition de chaques lettres contenue dans un dico
    """

    total_occurrences = sum(dico.values())
    # calcule des frequences
    for cle in dico:
        if dico[cle] != 0:
            dico[cle] = (dico[cle] / total_occurrences) * 100

    return dico

def lire_fichier_apparition(name_file):
    """
    Lire un fichier en entrer est compter le chaque occurence d'un caractere dans le texte
    """

    # ouvrir et lire le fichier d'entrée
    nom_fichier_entree = str(name_file)

    with open("./OUT/"+nom_fichier_entree, 'r') as fichier_entree:
        contenu = fichier_entree.read()

    return nb_apparitions(contenu)

def write_frequences_in_file(dico, name_file_out) :
    """
    ecrie dans un fichier les frequences recupérer en entré d'un dictionnaire pour ensuite les ecrire dans un
    fichier texte donné en entré
    """

    nom_dossier_sortie = "OUT"
    # nom du fichier de sortie par defaut
    nom_fichier_sortie = os.path.join(nom_dossier_sortie, name_file_out)

    dico = frequences(dico)
    # verifier si le fichier de sortie existe, sinon le créer
    if not os.path.exists(nom_fichier_sortie):
        open(nom_fichier_sortie, 'w').close()

    # save le résultat dans freq93.txt
    with open(nom_fichier_sortie, 'w') as fichier_sortie:
        # Parcourir le dictionnaire
        for cle, valeur in dico.items():
            ecriture = f"{cle} {valeur:.2f} %\n"
            fichier_sortie.write(ecriture)

    print("Traitement terminé. Résultat sauvegardé dans", nom_fichier_sortie)

def lire_fichier_frequences(nom_fichier):
    """
    lit un fichier qui contient les frequences entré sous la forme specifique a la fonction write_frequences_in_file()
    """
    lettres = []
    frequences = []

    with open("./OUT/"+nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()

        # on lit chaque ligne une a une
        for ligne in lignes:
            lettre, frequence = ligne.split()[0], ligne.split()[1]
            lettres.append(lettre)
            frequences.append(float(frequence))

    return lettres, frequences

def histogrammes(name_file,fichier_de_sortit):
    """
    Créeation d'un histogramme représenatant les do
    """

    lettres = lire_fichier_frequences(name_file)[0]
    frequences = lire_fichier_frequences(name_file)[1]

    res = lire_fichier_apparition(fichier_de_sortit)

    # Récupérer les valeurs du dictionnaire pour les ocurences
    valeurs = res.values()
    liste_de_valeurs = list(valeurs)


    # Créer histogrammes occurence
    fig,histo_freq = plt.subplots(1, 1, figsize=(10, 6))

    histo_freq.bar(lettres, liste_de_valeurs, color="blue")
    histo_freq.set_ylabel("nb d'ocurence")
    histo_freq.set_title("Histogramme du nombres d'apparition")

    # Sauvegarder l'histogramme occurence
    fig.savefig("Image/hist_app93.png")

    print("histogramme terminé. Résultat sauvegardé dans", 'Image/hist_app93.png')

    # Créer histogrammes frequence
    fig, (ax2) = plt.subplots(1, 1, figsize=(10, 6))

    ax2.bar(lettres, frequences, color="red")
    ax2.set_ylabel("Fréquences (%)")
    ax2.set_title("Histogramme des Fréquences")

    fig.savefig("Image/hist_freq93.png")

    print("histogramme terminé. Résultat sauvegardé dans", 'Image/hist_freq93.png')

    # Afficher les histogrammes
    plt.show()

def lire_fichier_to_chaine(name_file) :
    """
    lit un fichier et retourne la chaine de caractere du fichier
    """

    with open("./OUT/"+name_file, 'r') as fichier:
        lignes = fichier.read()

    return lignes

def nb_digrammes(chaine) :
    """
    compte le nombre d'apparitions d'un bigramme donné dans une chaîne de caractères arbitraire.
    """

    dico_digrammes = {
        'ES' : 0,'DE' : 0,'LE' : 0,
        'EN' : 0,'RE' : 0,'NT' : 0,
        'ON' : 0,'ER' : 0,'TE' : 0,
        'EL' : 0,'AN' : 0,'SE' : 0,
        'ET' : 0,'LA' : 0,'AI' : 0,
        'IT' : 0,'ME' : 0,'OU' : 0,
        'EM' : 0,'IE' : 0
    }

    for i in range(len(chaine) - 1):
        bigramme = chaine[i:i+2]
        if bigramme in dico_digrammes:
            dico_digrammes[bigramme] += 1

    return dico_digrammes

def histogrammes_ord_bigrammes(dico) :
    # fichier ou on savegarde le fichier
    fichier_save = 'Image/histo_bigramme.png'

    # Trie le dictionnaire par les valeurs
    res = list(dico.items())
    res = sorted(res,key=lambda x:x[1],reverse=True)
    res = dict(res)

    liste_bigrammes = list(res.keys())
    liste_nombres = list(res.values())

    fig, (fig1) = plt.subplots(1, 1, figsize=(10, 6))

    fig1.bar(liste_bigrammes, liste_nombres, color='blue')
    fig1.set_ylabel("nb d'ocurence")
    fig1.set_title('Histogramme des digrammes')

    fig.savefig(fichier_save)

    # Afficher l'histogramme
    plt.show()

    print("histogramme terminé. Résultat sauvegardé dans", fichier_save)



if __name__ == "__main__":
    """ 
    name_file_out = "93Out.txt"
    open_write_file_forTraitement("93.txt",name_file_out)
    
    
    
    fichier = lire_fichier_apparition(fichier_de_sortit)
    print(fichier)
    
    #calcule des frequences
    frequence = frequences(fichier)
    print(frequence)
    
    #écrire les freq dans un fichier
    write_frequences_in_file(frequence, "freq_Out.txt")
    
    #Créeation histogrammes
    histogrammes("freq_Out.txt")
    """

    # Apparitions de digrammes
    fichier_de_sortit = "93Out.txt"

    chaine = lire_fichier_to_chaine(fichier_de_sortit)
    res_nb_digrammes = nb_digrammes(chaine)
    print(res_nb_digrammes)

    histogrammes_ord_bigrammes(res_nb_digrammes)



