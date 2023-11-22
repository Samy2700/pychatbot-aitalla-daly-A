import os
import math

president_names = []
speeches = os.listdir('speeches')
for texte in speeches:
    if texte.endswith('txt'):
        president_names.append(texte[len('Nomination_'):len(texte)-4])
for texte in range(len(president_names)):
 print(president_names[texte])


presidents = {
    "Macron": "Emmanuel",
    "Hollande": "François",
    "Sarkozy": "Nicolas",
    "Chirac": "Jacques",
    "Mitterrand": "François"
}

for nom, prenom in presidents.items():
    print(f"Le prénom du président {nom} est {prenom}.")
print("\n")


source_directory = "C:/Users/samya/PycharmProjects/pythonProject/speeches"
destination_directory = "C:/Users/samya/PycharmProjects/pythonProject/cleaned"

def texte_modifié(texte):
    texte_miniscule = ""
    for char in texte:
        if ord("A") <= ord(char) <= ord("Z"):
            texte_miniscule += chr(ord(char) + ord("a")-ord("A"))
        elif char == "," or char == "." or char == ";" or char == '"':
            texte_miniscule += ""
        elif char == "-":
            texte_miniscule += " "
        elif char == "'":
            texte_miniscule += "e "
        else:
            texte_miniscule += char
    return texte_miniscule


for fichier in os.listdir(source_directory):
    if fichier.endswith(".txt"):
        source_chemin_fichier = os.path.join(source_directory, fichier)
        destination_chemin_fichier = os.path.join(destination_directory, fichier)

        with open(source_chemin_fichier, 'r') as f:
            texte = f.read()

        texte_converti = texte_modifié(texte)

        with open(destination_chemin_fichier, 'w') as f:
            f.write(texte_converti)

        print(f"Fichier modifié pour: {fichier}")

print("\n")


def score_tf(texte):
    compteur = {}
    mots = texte.split()
    for mot in mots:
        if mot in compteur:
            compteur[mot] += 1
        else:
            compteur[mot] = 1
    return compteur

for fichier in os.listdir(destination_directory):
    if fichier.endswith(".txt"):
        chemin_fichier = os.path.join(destination_directory, fichier)
        with open(chemin_fichier, 'r') as f:
            texte = f.read()

        comptage = score_tf(texte)
        print(f"Voici l'occurences de chaque mots dans '{fichier}':")
        for mot, occurence in comptage.items():
            print(f"{mot}: {occurence}", end=", ")
        print("\n")

def score_idf(destination_directory):
    nombres_documents = 0
    mots_dans_documents = {}

    for fichier in os.listdir(destination_directory):
        if fichier.endswith(".txt"):
            nombres_documents += 1
            chemin_fichier = os.path.join(destination_directory, fichier)
            with open(chemin_fichier, 'r') as f:
                texte = f.read()
                mots_uniques = set(texte.split())
                for mot in mots_uniques:
                    if mot in mots_dans_documents:
                        mots_dans_documents[mot] += 1
                    else:
                        mots_dans_documents[mot] = 1

    idf_scores = {}
    for mot, nombres_docs in mots_dans_documents.items():
        idf_scores[mot] = math.log((nombres_documents / nombres_docs))

    return idf_scores

idf_resultats = score_idf(destination_directory)
print(f"Voici le score idf pour chaque mot : {idf_resultats}", end=', ')
print("\n")

def matrice_tf_idf(destination_directory):
    tf_idf_matrice = {}
    fichiers = [filename for filename in os.listdir(destination_directory) if filename.endswith(".txt")]

    for fichier in fichiers:
        chemin_fichier = os.path.join(destination_directory, fichier)
        with open(chemin_fichier, 'r') as f:
            tf_scores = score_tf(f.read())
            for mot in tf_scores:
                if mot not in tf_idf_matrice:
                    tf_idf_matrice[mot] = [0] * len(fichiers)
                indice_fichier = fichiers.index(fichier)
                tf_idf_matrice[mot][indice_fichier] = tf_scores[mot] * idf_resultats.get(mot,0)

    return tf_idf_matrice, fichiers

def transposer_matrice(tf_idf_matrice, fichiers):
    transposée = []
    for i in range(len(fichiers)):
        ligne = [tf_idf_matrice[mot][i] for mot in tf_idf_matrice]
        transposée.append(ligne)

    return transposée

tf_idf, fichiers = matrice_tf_idf(destination_directory)

largeur_mot = 15
largeur_colonne = 35

en_tetes = "|".join(f"{nom_fichier:{largeur_colonne}}" for nom_fichier in fichiers)
print(f"{'Mot':{largeur_mot}}" + en_tetes)

for mot, scores in tf_idf.items():
    mot_matrice = f"{mot:<{largeur_mot}}"
    scores_matrice = "|".join(f"{score:<{largeur_colonne}.2f}" for score in scores)
    print(mot_matrice + scores_matrice)

print("\n")


def mots_moins_importants(tf_idf):
    mots_score_zero = []

    for mot, scores in tf_idf.items():
        if all(score == 0 for score in scores):
            mots_score_zero.append(mot)

    print("Mots les moins importants: ", end="")
    for mot in mots_score_zero:
        print(mot, end="; ")
    print("\n")



def mot_plus_haut_score(tf_idf):
    max_score = 0
    mots_max_score = []

    for mot, scores in tf_idf.items():
        for score in scores:
            if score > max_score:
                max_score = score
                mots_max_score = [mot]
            elif score == max_score:
                mots_max_score.append(mot)

    print("Mot avec le plus haut score TF-IDF:", mots_max_score, "Score:", max_score)
    print("\n")


def mot_chirac(textes_chirac):
    mots_chirac = {}

    for fichier in textes_chirac:
        chemin_fichier = os.path.join(destination_directory, fichier)
        with open(chemin_fichier, 'r') as f:
            texte = f.read()
            comptage = score_tf(texte)
            for mot, occurence in comptage.items():
                mots_chirac[mot] = mots_chirac.get(mot,0) + occurence

    mots_plus_repete = None
    occurence_max = 0

    for mot, occurence in mots_chirac.items():
        if occurence > occurence_max:
            mots_plus_repete = mot
            occurence_max = occurence


    print("Le mot le plus répété par Chirac est:", mots_plus_repete)
    print("\n")




def occurences_nation(destination_directory, mot_a_chercher):
    max_occurrences = 0
    president_occurrences = ""

    for fichier in os.listdir(destination_directory):
        if fichier.endswith(".txt"):
            chemin_fichier = os.path.join(destination_directory, fichier)
            with open(chemin_fichier, 'r') as f:
                contenu = f.read()
                mots = contenu.split()
                occurrences = mots.count(mot_a_chercher)

                if occurrences > max_occurrences:
                    max_occurrences = occurrences
                    nom_fichier = os.path.splitext(f.name)[0]
                    president_occurrences = nom_fichier.split("_")[1]

    if max_occurrences > 0:
        print(f"Le président ayant le plus mentionné le mot 'nation' est {president_occurrences} avec {max_occurrences} occurrences.")

        print("\n")



def premier_president_a_parler(mots_cles):
    for fichier in os.listdir(destination_directory):
        if fichier.endswith(".txt"):
            chemin_fichier = os.path.join(destination_directory, fichier)
            with open(chemin_fichier, 'r') as f:
                contenu = f.read()
                for mot_cle in mots_cles:
                    if mot_cle in contenu:
                        nom_fichier = os.path.splitext(fichier)[0]
                        return nom_fichier.split("_")[1]


def afficher_premier_president(mots_cles):
    premier_president = premier_president_a_parler(mots_cles)
    if premier_president:
        print(f"Le premier président à parler du climat et/ou de l'écologie est {premier_president}.")
    else:
        print("Aucun président n'a abordé ces sujets.")




def affichage_menu():
        print("\nMenu des Options :")
        print("1. Afficher les mots les moins importants")
        print("2. Afficher le mot avec le score TD-IDF le plus élevé")
        print("3. Afficher le mot le plus répété par Chirac")
        print("4. Afficher le président qui parle le plus de la 'Nation'")
        print("5. Afficher le premier président à parler du climat/écologie")
        print("6. Afficher les mots évoqués par tous les présidents")
        print("7. Quitter")
        choix = input("Entrez votre choix : ")


        if choix == '1':
            mots_moins_importants(tf_idf)
        elif choix == '2':
            mot_plus_haut_score(tf_idf)
        elif choix == '3':
            textes_chirac = ["Nomination_Chirac1.txt", "Nomination_Chirac2.txt"]
            mot_chirac(textes_chirac)
        elif choix == '4':
            mot_a_chercher = "nation"
            occurences_nation(destination_directory,mot_a_chercher)
        elif choix == '5':
            mots_cles = ["climat", "écologie"]
            afficher_premier_president(mots_cles)



affichage_menu()


