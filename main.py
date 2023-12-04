import os
import math

#Extraire les noms des présidents à partir des noms des fichiers texte fournis
president_names = []
speeches = os.listdir('speeches')
for texte in speeches:
    # Vérifier si le fichier est un fichier texte
    if texte.endswith('txt'):
        # Extraire le nom du président du nom du fichier en supprimant 'Nomination_' et l'extension '.txt'
        president_names.append(texte[len('Nomination_'):len(texte)-4])
for texte in range(len(president_names)):
 print(president_names[texte])

def prenom_president():
    #Associer à chaque président un prénom
    presidents = {
        "Macron": "Emmanuel",
        "Hollande": "François",
        "Sarkozy": "Nicolas",
        "Chirac": "Jacques",
        "Mitterrand": "François"
    }

    # Demander à l'utilisateur de saisir un prénom
    nom_saisi = input("Entrez le nom du président : ")

    # Trouver et afficher le prénom correspondant au nom
    prenom = presidents.get(nom_saisi)
    if prenom:
        print(f"Le prénom du président {nom_saisi} est {prenom}.")
    else:
        print(f"Aucun président trouvé avec le nom {nom_saisi}.")


# Définir les chemins globaux des dossiers source et destination pour un accès facile lors des traitements
source_directory = "C:/Users/samya/PycharmProjects/pythonProject/speeches"
destination_directory = "C:/Users/samya/PycharmProjects/pythonProject/cleaned"

def texte_modifié(texte):
    # Fonction qui permet de convertir les textes donnés
    texte_miniscule = ""
    for char in texte:
        # Convertir les majuscules en minuscules
        if ord("A") <= ord(char) <= ord("Z"):
            texte_miniscule += chr(ord(char) + ord("a")-ord("A"))
        # Ignorer les virgules, points, points-virgules et guillemets
        elif char == "," or char == "." or char == ";" or char == '"':
            texte_miniscule += ""
        # Remplacer les tirets par des espaces
        elif char == "-" or char == "_" :
            texte_miniscule += " "
        # Remplacer les apostrophes par "e "
        elif char == "'":
            texte_miniscule += "e "
        # Conserver les autres caractères
        else:
            texte_miniscule += char
    return texte_miniscule

# Parcourir chaque fichier dans le dossier source
for fichier in os.listdir(source_directory):
    # Traiter uniquement les fichiers texte
    if fichier.endswith(".txt"):
        # Construire les chemins complets vers les fichiers source et destination
        source_chemin_fichier = os.path.join(source_directory, fichier)
        destination_chemin_fichier = os.path.join(destination_directory, fichier)

        # Lire le contenu du fichier source
        with open(source_chemin_fichier, 'r') as f:
            texte = f.read()

        # Convertir le texte
        texte_converti = texte_modifié(texte)

        # Écrire le texte converti dans le fichier de destination
        with open(destination_chemin_fichier, 'w') as f:
            f.write(texte_converti)

        # Afficher un message pour chaque fichier traité
        print(f"Fichier modifié pour: {fichier}")

print("\n")


def score_tf(texte):
    # Fonction pour calculer la fréquence de chaque mot dans un texte
    compteur = {}
    mots = texte.split()
    for mot in mots:
        # Si le mot est déjà dans le compteur, incrémenter sa valeur
        if mot in compteur:
            compteur[mot] += 1
        # Sinon, initialiser sa valeur à 1
        else:
            compteur[mot] = 1
    return compteur

# Parcourir tous les fichiers dans le dossier de destination
for fichier in os.listdir(destination_directory):
    # Traiter uniquement les fichiers texte
    if fichier.endswith(".txt"):
        chemin_fichier = os.path.join(destination_directory, fichier)
        # Ouvrir et lire le contenu du fichier
        with open(chemin_fichier, 'r') as f:
            texte = f.read()

        # Calculer la fréquence de chaque mot dans le texte
        comptage = score_tf(texte)
        print(f"Voici l'occurences de chaque mots dans '{fichier}':")
        # Afficher les fréquences des mots pour chaque fichier
        for mot, occurence in comptage.items():
            print(f"{mot}: {occurence}", end=", ")
        print("\n")

def score_idf(destination_directory):
    # Fonction pour calculer le score IDF de chaque mot dans l'ensemble du corpus
    nombres_documents = 0
    mots_dans_documents = {}

    for fichier in os.listdir(destination_directory): #Parcouir tous les fichiers puis appliquer la fonction
        if fichier.endswith(".txt"):
            nombres_documents += 1
            chemin_fichier = os.path.join(destination_directory, fichier)
            with open(chemin_fichier, 'r') as f:
                texte = f.read()
                # Créer un ensemble de mots uniques dans le document
                mots_uniques = set(texte.split())
                for mot in mots_uniques:
                    # Compter dans combien de documents chaque mot apparaît
                    if mot in mots_dans_documents:
                        mots_dans_documents[mot] += 1
                    else:
                        mots_dans_documents[mot] = 1

    idf_scores = {}
    # Calculer le score IDF pour chaque mot
    for mot, nombres_docs in mots_dans_documents.items():
        # Utiliser la formule IDF
        idf_scores[mot] = math.log((nombres_documents / nombres_docs) + 1)

    return idf_scores

# Calculer et afficher les scores IDF pour chaque mot dans le corpus
idf_resultats = score_idf(destination_directory)
print(f"Voici le score idf pour chaque mot : {idf_resultats}", end=', ')
print("\n")

def matrice_tf_idf(destination_directory):
    # Fonction pour créer une matrice TF-IDF
    tf_idf_matrice = {}
    # Récupérer la liste des fichiers texte dans le dossier de destination
    fichiers = [filename for filename in os.listdir(destination_directory) if filename.endswith(".txt")]

    # Calculer les scores TF pour chaque mot dans chaque fichier
    for fichier in fichiers:
        chemin_fichier = os.path.join(destination_directory, fichier)
        with open(chemin_fichier, 'r') as f:
            tf_scores = score_tf(f.read())
            for mot in tf_scores:
                # Initialiser la matrice pour chaque mot
                if mot not in tf_idf_matrice:
                    tf_idf_matrice[mot] = [0] * len(fichiers)
                # Calculer le score TF-IDF pour chaque mot dans chaque fichier
                indice_fichier = fichiers.index(fichier)
                tf_idf_matrice[mot][indice_fichier] = tf_scores[mot] * idf_resultats.get(mot,0)

    return tf_idf_matrice, fichiers

def transposer_matrice(tf_idf_matrice, fichiers):
    # Fonction pour transposer la matrice TF-IDF
    transposée = []
    for i in range(len(fichiers)):
        # Créer une ligne de la matrice transposée pour chaque document
        ligne = [tf_idf_matrice[mot][i] for mot in tf_idf_matrice]
        transposée.append(ligne)

    return transposée

# Appel de la fonction pour créer la matrice TF-IDF
tf_idf, fichiers = matrice_tf_idf(destination_directory)

# Affichage de la matrice TF-IDF
largeur_mot = 30
largeur_colonne = 40

# Créer l'en-tête avec les noms des fichiers
en_tetes = "|".join(f"{nom_fichier:{largeur_colonne}}" for nom_fichier in fichiers)
print(f"{'Mot':{largeur_mot}}" + en_tetes)

# Afficher les scores TF-IDF pour chaque mot
for mot, scores in tf_idf.items():
    mot_matrice = f"{mot:<{largeur_mot}}"
    scores_matrice = "|".join(f"{score:<{largeur_colonne}.2f}" for score in scores)
    print(mot_matrice + scores_matrice)

print("\n")


def mots_moins_importants(tf_idf):
    # Fonction pour trouver les mots avec un score TF_IDF = 0
    mots_score_zero = []

    # Parcourir chaque mot et ses scores dans la matrice TF-IDF
    for mot, scores in tf_idf.items():
        # Vérifier si le score est 0 dans tous les documents
        if all(score == 0 for score in scores):
            mots_score_zero.append(mot)

    # Affichage des mots les moins importants
    print("Mots les moins importants:", mots_score_zero)



def mot_plus_haut_score(tf_idf):
    # Fonction qui trouve le mot avec le plus haut score TF_IDF
    max_score = 0
    mots_max_score = []

    # Parcourir chaque mot et ses scores dans la matrice TF-IDF
    for mot, scores in tf_idf.items():
        for score in scores:
            # Mettre à jour le score maximal et le mot correspondant
            if score > max_score:
                max_score = score
                mots_max_score = [mot]
            elif score == max_score:
                mots_max_score.append(mot)

    # Affichage du mot avec le plus haut score TF-IDF
    print("Mot avec le plus haut score TF-IDF:", mots_max_score, "Score:", max_score)
    print("\n")


def mot_chirac(textes_chirac):
    # Fonction qui trouve le mot le plus répété par Chirac
    mots_chirac = {}

    # Parcourir les textes associés à Chirac
    for fichier in textes_chirac:
        chemin_fichier = os.path.join(destination_directory, fichier)
        with open(chemin_fichier, 'r') as f:
            texte = f.read()
            # Calculer la fréquence de chaque mot
            comptage = score_tf(texte)
            for mot, occurence in comptage.items():
                mots_chirac[mot] = mots_chirac.get(mot,0) + occurence

    mots_plus_repete = None
    occurence_max = 0

    # Trouver le mot le plus répété
    for mot, occurence in mots_chirac.items():
        if occurence > occurence_max:
            mots_plus_repete = mot
            occurence_max = occurence

    # Affichage du mot le plus répété par Chirac

    print("Le mot le plus répété par Chirac est:", mots_plus_repete)
    print("\n")




def occurences_nation(destination_directory, mot_a_chercher):
    # Fonction qui calcule l'occurences du mot nation
    # Initialiser le compteur d'occurrences maximales et le nom du président correspondant
    max_occurrences = 0
    president_occurrences = ""

    # Parcourir chaque fichier texte dans le répertoire de destination
    for fichier in os.listdir(destination_directory):
        if fichier.endswith(".txt"):
            chemin_fichier = os.path.join(destination_directory, fichier)
            with open(chemin_fichier, 'r') as f:
                contenu = f.read()
                mots = contenu.split()
                occurrences = mots.count(mot_a_chercher)

                # Mettre à jour le président avec le plus grand nombre d'occurrences
                if occurrences > max_occurrences:
                    max_occurrences = occurrences
                    # Extraire le nom du président à partir du nom du fichier
                    nom_fichier = os.path.splitext(fichier)[0]  # Séparer le nom du fichier de son extension
                    president_occurrences = nom_fichier.split("_")[1] # Retourner le nom du président

    # Afficher le président ayant le plus mentionné le mot spécifié
    if max_occurrences > 0:
        print(f"Le président ayant le plus mentionné le mot 'nation' est {president_occurrences} avec {max_occurrences} occurrences.")

        print("\n")


def premier_president_a_parler(mots_cles):
    # Fonction qui trouve quel président a parlé de l'écologie en premier
    # Parcourir chaque fichier dans le répertoire des destination
    for fichier in os.listdir(destination_directory):
        if fichier.endswith(".txt"):
            chemin_fichier = os.path.join(destination_directory, fichier)
            with open(chemin_fichier, 'r') as f:
                contenu = f.read()
                # Vérifier si l'un des mots clés est présent dans le contenu du fichier
                for mot_cle in mots_cles:
                    if mot_cle in contenu:
                        # Extraire le nom du président à partir du nom du fichier
                        nom_fichier = os.path.splitext(fichier)[0] # Séparer le nom du fichier de son extension
                        return nom_fichier.split("_")[1] # Retourner le nom du président



def afficher_premier_president(mots_cles):
    # Appeler la fonction premier_president_a_parler pour obtenir le nom du premier président parlant des mots clés
    premier_president = premier_president_a_parler(mots_cles)

    # Afficher le résultat
    if premier_president:
        print(f"Le premier président à parler du climat et/ou de l'écologie est {premier_president}.")

def mots_communs_presidents(destination_directory):
    # Obtenir les scores IDF pour tous les mots
    idf_scores = score_idf(destination_directory)
    # Trouver les mots dont le score IDF est proche de log(2)
    mots_communs = [mot for mot, score in idf_scores.items() if math.isclose(score, math.log(2))]

    # Afficher le résulat
    print("Hormis les mots non importants, les mots communs sont : ", mots_communs)

def mot_evoques_president(tf_idf):

    mot_evoques_presidents = []

    for mot, scores in tf_idf.items():
        if all(score != 0 for score in scores):
            if mot in #(dictionnaire avec les noms des présidents pour vérifier que tous les présidents l'ont dit):
                mot_evoques_presidents.append(mot)

def affichage_menu():
        # Affichage des options du menu principal
        print("\nMenu des Options :")
        print("1. Quel est le nom du président choisi")
        print("2. Afficher les mots les moins importants")
        print("3. Afficher le mot avec le score TD-IDF le plus élevé")
        print("4. Afficher le mot le plus répété par Chirac")
        print("5. Afficher le président qui parle le plus de la 'Nation'")
        print("6. Afficher le premier président à parler du climat/écologie")
        print("7. Afficher les mots évoqués par tous les présidents")
        print("8. Quitter")

        # Demander à l'utilisateur de faire un choix
        choix = input("Entrez votre choix : ")

        # Exécuter l'action correspondante au choix de l'utilisateur
        if choix == '1':
            prenom_president()
            affichage_menu()
        elif choix == '2':
            # Afficher les mots les moins importants du corpus
            mots_moins_importants(tf_idf)
            affichage_menu()
        elif choix == '3':
            # Afficher le mot avec le score TD-IDF le plus élevé
            mot_plus_haut_score(tf_idf)
            affichage_menu()
        elif choix == '4':
            # Afficher le mot le plus répété par Chirac dans les deux discours de Chirac
            textes_chirac = ["Nomination_Chirac1.txt", "Nomination_Chirac2.txt"]
            mot_chirac(textes_chirac)
            affichage_menu()
        elif choix == '5':
            # Afficher le président qui a le plus mentionné "nation"
            mot_a_chercher = "nation"
            occurences_nation(destination_directory,mot_a_chercher)
            affichage_menu()
        elif choix == '6':
            # Afficher le premier président qui a parlé de ces mots cles
            mots_cles = ["climat", "écologie"]
            afficher_premier_president(mots_cles)
            affichage_menu()
        elif choix == '7':
            # Afficher les mots communs des présidents
            mots_communs_presidents(destination_directory)
            affichage_menu()
        elif choix == '8':
            # Quitter le programme
            quit(affichage_menu())

# Appeler la fonction affichage_menu pour démarrer le programme
affichage_menu()


