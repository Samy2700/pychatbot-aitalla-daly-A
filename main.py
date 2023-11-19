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


source_directory = "C:/Users/samya/PycharmProjects/pythonProject/speeches"
destination_directory = "C:/Users/samya/PycharmProjects/pythonProject/cleaned"

def texte_modifié(texte):
    texte_miniscule = ""
    for char in texte:
        if ord("A") <= ord(char) <= ord("Z"):
            texte_miniscule += chr(ord(char) + ord("a")-ord("A"))
        elif char == "," or char == "." or char == ";":
            texte_miniscule += ""
        elif char == "-":
            texte_miniscule += " "
        elif char == "'":
            texte_miniscule += "e "
        else:
            texte_miniscule += char
    return texte_miniscule


for filename in os.listdir(source_directory):
    if filename.endswith(".txt"):
        source_file_path = os.path.join(source_directory, filename)
        destination_file_path = os.path.join(destination_directory, filename)

        with open(source_file_path, 'r') as file:
            texte = file.read()

        texte_converti = texte_modifié(texte)

        with open(destination_file_path, 'w') as file:
            file.write(texte_converti)

        print(f"Fichier modifié pour: {filename}")


def score_tf(texte):
    compteur = {}
    mots = texte.split()
    for mot in mots:
        if mot in compteur:
            compteur[mot] += 1
        else:
            compteur[mot] = 1
    return compteur

for filename in os.listdir(destination_directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(destination_directory, filename)
        with open(file_path, 'r') as file:
            text = file.read()

        comptage = score_tf(text)
        print(f"Voici l'occurences de chaque mots dans '{filename}':")
        for mot, occurence in comptage.items():
            print(f"{mot}: {occurence}", end=", ")
        print("\n")

def score_idf(destination_directory):
    nombre_documents = 0
    mot_dans_documents = {}

    for filename in os.listdir(destination_directory):
        if filename.endswith(".txt"):
            nombre_documents += 1
            chemin_fichier = os.path.join(destination_directory, filename)
            with open(chemin_fichier, 'r') as fichier:
                texte = fichier.read()
                mots_uniques = set(texte.split())
                for mot in mots_uniques:
                    if mot in mot_dans_documents:
                        mot_dans_documents[mot] += 1
                    else:
                        mot_dans_documents[mot] = 1

    idf_scores = {}
    for mot, nombre_docs in mot_dans_documents.items():
        idf_scores[mot] = math.log(nombre_documents / nombre_docs)

    return idf_scores

idf_resultats = score_idf(destination_directory)
print(f"Voici le score idf pour chaque mot : {idf_resultats}", end=', ')


