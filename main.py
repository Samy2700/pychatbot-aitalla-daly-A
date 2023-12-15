# Partie 1
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
        elif char == "," or char == "." or char == ";" or char == '"' or char == "?" or char == "!":
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
        with open(source_chemin_fichier, 'r', encoding='utf-8') as f:
            texte = f.read()

        # Convertir le texte
        texte_converti = texte_modifié(texte)

        # Écrire le texte converti dans le fichier de destination
        with open(destination_chemin_fichier, 'w', encoding='utf-8') as f:
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
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
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
        idf_scores[mot] = math.log10((nombres_documents / nombres_docs))

    return idf_scores

# Calculer et afficher les scores IDF pour chaque mot dans le corpus
idf_resultats = score_idf(destination_directory)
print(f"Voici le score idf pour chaque mot : {idf_resultats}", end=', ')
print("\n")



def matrice_tf_idf(destination_directory):
    # Fonction pour créer une matrice TF-IDF
    tf_idf_matrice_corpus = {}
    # Récupérer la liste des fichiers texte dans le dossier de destination
    fichiers = [filename for filename in os.listdir(destination_directory) if filename.endswith(".txt")]

    # Calculer les scores TF pour chaque mot dans chaque fichier
    for fichier in fichiers:
        chemin_fichier = os.path.join(destination_directory, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            tf_scores = score_tf(f.read())
            for mot in tf_scores:
                # Initialiser la matrice pour chaque mot
                if mot not in tf_idf_matrice_corpus:
                    tf_idf_matrice_corpus[mot] = [0] * len(fichiers)
                # Calculer le score TF-IDF pour chaque mot dans chaque fichier
                indice_fichier = fichiers.index(fichier)
                tf_idf_matrice_corpus[mot][indice_fichier] = tf_scores[mot] * idf_resultats.get(mot,0)

    return tf_idf_matrice_corpus, fichiers


def affichage_matrice_tf_idf_corpus(tf_idf_matrice_corpus, fichiers):
    largeur_mot = 35

    # Créer l'en-tête avec les mots (colonnes)
    en_tete = f"{'Fichier':<{largeur_mot}}" + "".join(f"{mot:{largeur_mot}}" for mot in tf_idf_matrice_corpus.keys())
    print(en_tete)

    # Afficher les scores TF-IDF pour chaque fichier
    for index_fichier in range(len(fichiers)):
        fichier = fichiers[index_fichier]
        ligne = f"{fichier:<{largeur_mot}}" + "".join(
            f"{tf_idf_matrice_corpus[mot][index_fichier]:<{largeur_mot}.2f}" for mot in tf_idf_matrice_corpus.keys())
        print(ligne)
    print("\n")

# Appel de la fonction pour créer la matrice TF-IDF et afficher la matrice
tf_idf, fichiers = matrice_tf_idf(destination_directory)
affichage_matrice_tf_idf_corpus(tf_idf, fichiers)


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


def mot_chirac(destination_directory,textes_chirac):
    # Fonction qui trouve le mot le plus répété par Chirac hormis les mots non importants
    mots_non_importants = set(mot for mot, scores in tf_idf.items() if all(score == 0 for score in scores))
    if mots_non_importants is None:
        print("Erreur: la matrice TF-IDF est invalide")
        return
    mots_chirac = {}

    # Parcourir les textes associés à Chirac
    for fichier in textes_chirac:
        chemin_fichier = os.path.join(destination_directory, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            texte = f.read()
            # Calculer la fréquence de chaque mot
            comptage = score_tf(texte)
            for mot, occurence in comptage.items():
                if mot not in mots_non_importants:
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
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
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
    # Parcourir chaque fichier dans le répertoire des destinations
    for fichier in os.listdir(destination_directory):
        if fichier.endswith(".txt"):
            chemin_fichier = os.path.join(destination_directory, fichier)
            with open(chemin_fichier, 'r', encoding='utf-8') as f:
                contenu = f.read()
                # Vérifier si l'un des mots clés est présent dans le contenu du fichier
                for mot_cle in mots_cles:
                    if mot_cle in contenu:
                        # Extraire le nom du président à partir du nom du fichier
                        nom_president = os.path.splitext(fichier)[0].split("_")[1] # Séparer le nom du fichier de son extension
                        print(f"Le premier président à parler du climat et/ou de l'écologie est {nom_president}.")
                        return # Retourner le nom du président




def affichage_menu():
        # Affichage des options du menu principal
        print("\nMenu des Options :")
        print("1. Quel est le nom du président choisi")
        print("2. Afficher les mots les moins importants")
        print("3. Afficher le mot avec le score TD-IDF le plus élevé")
        print("4. Afficher le mot le plus répété par Chirac")
        print("5. Afficher le président qui parle le plus de la 'Nation'")
        print("6. Afficher le premier président à parler du climat/écologie")
        print("7. Quitter")

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
            mot_chirac(destination_directory, textes_chirac)
            affichage_menu()
        elif choix == '5':
            # Afficher le président qui a le plus mentionné "nation"
            mot_a_chercher = "nation"
            occurences_nation(destination_directory, mot_a_chercher)
            affichage_menu()
        elif choix == '6':
            # Afficher le premier président qui a parlé de ces mots cles
            mots_cles = ["climat", "écologie"]
            premier_president_a_parler(mots_cles)
            affichage_menu()
        elif choix == '7':
            # Quitter le programme
            quit(affichage_menu())


# Appeler la fonction affichage_menu pour démarrer le programme
affichage_menu()




# Partie 2
def traiter_question(question_utilisateur):
    question = ""
    for char in question_utilisateur:
        # Convertir les majuscules en minuscules
        if ord("A") <= ord(char) <= ord("Z"):
            question += chr(ord(char) + ord("a") - ord("A"))
        # Ignorer les virgules, points, points-virgules et guillemets
        elif char in [",", ".", ";", '"', "?", "!"]:
            continue
        # Remplacer les tirets et les underscores par des espaces
        elif char in ["-", "_"]:
            question += " "
        # Remplacer les apostrophes par "e "
        elif char == "'":
            question += "e "
        # Conserver les autres caractères
        else:
            question += char

    # Séparer la chaîne de caractères traitée en mots
    question_traitee = question.split()

    return question_traitee


def intersection_question_corpus(tf_idf):
    question_traitee = traiter_question(question_utilisateur)
    mot_question_dans_corpus = []
    for mot_questions in question_traitee:
        for mot, scores in tf_idf.items():
            if mot == mot_questions:
                mot_question_dans_corpus.append(mot_questions)

    print("Les mots communs sont :", mot_question_dans_corpus)


def score_tf_question(question_traitee):
    # Fonction pour calculer la fréquence de chaque mot dans une question
    compteur = {}
    mots = question_traitee
    for mot in mots:
        # Si le mot est déjà dans le compteur, incrémenter sa valeur
        if mot in compteur:
            compteur[mot] += 1
        # Sinon, initialiser sa valeur à 1
        else:
            compteur[mot] = 1
    return compteur

def score_idf_question(question_traitee, idf_resultats):
    # Fonction pour calculer le score IDF de chaque mot dans une question
    scores_idf = {}
    mots = question_traitee
    for mot in mots:
        if mot in idf_resultats:
            scores_idf[mot] = idf_resultats[mot]
        else:
            scores_idf[mot] = 0
    return scores_idf

def matrice_tf_idf_question(question_traitee, idf_resultats):
    tf_idf_matrice_question = {}
    fichiers = [filename for filename in os.listdir(destination_directory) if filename.endswith(".txt")]

    # Construire une liste de tous les mots dans l'ordre de leur apparition dans le corpus
    mots_corpus = []
    for fichier in fichiers:
        chemin_fichier = os.path.join(destination_directory, fichier)
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            mots = f.read().split()
            for mot in mots:
                if mot not in mots_corpus:
                    mots_corpus.append(mot)
                    tf_idf_matrice_question[mot] = 0

    # Calculer les scores TF pour la question
    tf_scores = score_tf(" ".join(question_traitee))

    # Mettre à jour la matrice TF-IDF pour la question en utilisant les scores TF de la question
    for mot in mots_corpus:
        tf_score = tf_scores.get(mot, 0)
        idf_score = idf_resultats.get(mot, 0)
        tf_idf_matrice_question[mot] = tf_score * idf_score

    return tf_idf_matrice_question


def afficher_matrice_tf_idf_question(tf_idf_question):
    largeur_mot = 35

    # Créer l'en-tête avec les mots (colonnes)
    en_tete = f"{'Mot: ':<{largeur_mot}}" + "".join(f"{mot:{largeur_mot}}" for mot in tf_idf_question.keys())
    print(en_tete)

    # Afficher les scores TF-IDF pour la question
    ligne = "".join(f"{tf_idf_question[mot]:<{largeur_mot}.2f}" for mot in tf_idf_question.keys())
    print(f"{'Score TF-IDF de la question':<{largeur_mot}}" + ligne)


def produit_scalaire(tf_idf_question, tf_idf, fichiers):
    resultats = {}
    for fichier in fichiers:
        score = 0
        indice_fichier = fichiers.index(fichier)  # Obtenir l'indice du fichier actuel
        for mot in tf_idf_question:
            score_tf_idf_question = tf_idf_question.get(mot, 0)
            # Accès au score TF-IDF du mot pour le fichier spécifique
            score_tf_idf_fichier = tf_idf.get(mot, [0] * len(fichiers))[indice_fichier]
            score += score_tf_idf_question * score_tf_idf_fichier
        resultats[fichier] = score
    return resultats


def calculer_norme_question(tf_idf_question):
    if mot not in tf_idf:
        return 0
    # Initialiser la somme des carrés à 0
    somme_carres = 0

    # Additionner les carrés des scores TF-IDF
    for score in tf_idf_question.values():
        somme_carres += score ** 2

    # Calculer la racine carrée de la somme des carrés pour obtenir la norme
    norme = math.sqrt(somme_carres)

    return norme


def calculer_norme_corpus(tf_idf):
    if mot not in tf_idf:
        return 0  # Le mot n'est pas dans la matrice TF-IDF

    scores_tf_idf = tf_idf[mot]
    somme_carres = 0
    for score in scores_tf_idf:
        somme_carres = score ** 2

    norme = math.sqrt(somme_carres)

    return norme




def calculer_similarite_cosinus(tf_idf_question, tf_idf, fichiers):
    # Calcul du produit scalaire pour chaque fichier
    resultats_produit_scalaire = produit_scalaire(tf_idf_question, tf_idf, fichiers)

    # Calcul de la norme de la question
    norme_question = calculer_norme_question(tf_idf_question)
    norme_fichier = calculer_norme_corpus(tf_idf)  # Calcul de la norme du fichier
    # Stockage des similarités cosinus
    similarites = {}

    # Calcul de la similarité cosinus pour chaque fichier
    for fichier in fichiers:
        if norme_fichier != 0 and norme_question != 0:
            similarite = resultats_produit_scalaire[fichier] / (norme_fichier * norme_question)
        else:
            similarite = 0
        similarites[fichier] = similarite

    return similarites

def trouver_document_le_plus_pertinent(tf_idf_question, tf_idf_corpus, fichiers):
    similarites = calculer_similarite_cosinus(tf_idf_question, tf_idf_corpus, fichiers)

    fichier_le_plus_pertinent = None
    similarite_maximale = -1  # Initialiser à une valeur basse

    for fichier, similarite in similarites.items():
        if similarite > similarite_maximale:
            similarite_maximale = similarite
            fichier_le_plus_pertinent = fichier

    return fichier_le_plus_pertinent



def mot_avec_score_tfidf_le_plus_eleve(tf_idf_question):
    mot_max = None
    score_max = 0

    for mot, score in tf_idf_question.items():
        if score > score_max:
            mot_max = mot
            score_max = score

    return mot_max


def trouver_phrase_contenant_mot(source_directory, document, mot):
    chemin_fichier = os.path.join(source_directory, document)
    # Ouvrir et lire le fichier
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()

    # Trouver la première occurrence du mot
    index_mot = contenu.find(mot)
    if index_mot == -1:
        return "Mot non trouvé dans le document."

    # Trouver le début et la fin de la phrase
    debut_phrase = contenu.rfind(".", 0, index_mot) + 1
    fin_phrase = contenu.find(".", index_mot)

    # Extraire et retourner la phrase
    phrase = contenu[debut_phrase:fin_phrase + 1].strip()

    return phrase





import random

def personnaliser_reponse(reponse_brute):
    # Votre dictionnaire de formules de début de réponse
    question_starters = {
        "Comment": "Après analyse, ",
        "Pourquoi": "Car, ",
        "Peux-tu": "Oui, bien sûr! ",
        # Vous pouvez ajouter d'autres formules ici
    }

    # Choisir une expression au hasard parmi les valeurs du dictionnaire
    expression_choisie = random.choice(list(question_starters.values()))

    # S'assurer que le premier caractère de la réponse brute est en minuscule
    if reponse_brute:
        reponse_brute = reponse_brute[0].lower() + reponse_brute[1:]

    # Ajouter l'expression choisie au début de la réponse brute
    reponse_personnalisee = expression_choisie + reponse_brute

    # S'assurer que la réponse commence par une majuscule et se termine par un point
    reponse_personnalisee = reponse_personnalisee[0] + reponse_personnalisee[1:]
    if not reponse_personnalisee.endswith('.'):
        reponse_personnalisee += '.'

    return reponse_personnalisee




question_utilisateur = input("Veuillez entrer votre question : ")
question_traitee = traiter_question(question_utilisateur)
print("Question traitée :", question_traitee)

intersection_question_corpus(tf_idf)

tf_score_question = score_tf_question(question_traitee)
print("Les scores tf sont :", tf_score_question)

idf_score_question = score_idf_question(question_traitee,idf_resultats)
print("Les scores idf sont :", idf_score_question)

tf_idf_question_matrice = matrice_tf_idf_question(question_traitee, idf_resultats)
print("Les scores tf-idf sont : ", tf_idf_question_matrice)
print("\n")

afficher_matrice_tf_idf_question(tf_idf_question_matrice)
print("\n")




# Calculs pour toute la question
resultats_comparaison = produit_scalaire(tf_idf_question_matrice, tf_idf, fichiers)
print("Produit scalaire pour la question :", resultats_comparaison)

norme_question = calculer_norme_question(tf_idf_question_matrice)
print("Norme du vecteur de la question :", norme_question)

similarite = calculer_similarite_cosinus(tf_idf_question_matrice, tf_idf, fichiers)
print("Similarité cosinus pour la question :", similarite)

document_pertinent = trouver_document_le_plus_pertinent(tf_idf_question_matrice, tf_idf, fichiers)
print("Document le plus pertinent pour la question :", document_pertinent)

# Trouver le mot avec le score TF-IDF le plus élevé dans la question
mot_important = mot_avec_score_tfidf_le_plus_eleve(tf_idf_question_matrice)
print("Mot le plus important dans la question :", mot_important)

# Trouver la phrase contenant le mot dans le document pertinent
phrase_reponse = trouver_phrase_contenant_mot(source_directory, document_pertinent, mot_important)

reponse_personnalisee = personnaliser_reponse(phrase_reponse)

print("Réponse générée :", reponse_personnalisee)

