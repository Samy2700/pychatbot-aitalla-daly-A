import os

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

compteur = {}
def compteur_mots(texte):
    mots = texte.split()
    for mot in mots:
        if mot in compteur:
            compteur[mot] += 1
        else:
            compteur[mot] = 1
    return compteur_mots


for filename in os.listdir(destination_directory):
    if filename.endswith(".txt"):
        file_path = os.path.join(destination_directory, filename)
        with open(file_path, 'r') as file:
            text = file.read()
        comptages = compteur_mots(text)
        compteur[filename] = comptages

print(compteur, end='')





















# def ponctuation(text):
#     sans_ponctuation = ""
#     for char in text:
#         if char == "'" or char == "," or char == "." or char == ";" or char == "-":
#             sans_ponctuation += " "
#         else:
#             sans_ponctuation += char
#     return sans_ponctuation

# for filename in os.listdir(source_directory):
#     if filename.endswith(".txt"):
#         source_file_path = os.path.join(source_directory, filename)
#         destination_file_path = os.path.join(destination_directory, filename)
#
#         with open(source_file_path, 'r') as file:
#             text = file.read()
#
#         texte_sans_ponctuation = ponctuation(text)
#
#         with open(destination_file_path, 'w') as file:
#             file.write(texte_sans_ponctuation)
#
#         print(f"Fichier sans ponctuation pour: {filename}")

# def verif_espace(text):
#     espacecount = 0
#     verif_ponctuation = ""
#     for char in text:
#         if espacecount == 1:
#             verif_ponctuation += ""
#             espacecount = 0
#         elif char == " ":
#             espacecount += 1
#             verif_ponctuation += char
#         else:
#             verif_ponctuation += char
#     return verif_ponctuation

# for filename in os.listdir(source_directory):
#     if filename.endswith(".txt"):
#         source_file_path = os.path.join(source_directory, filename)
#         destination_file_path = os.path.join(destination_directory, filename)
#
#         with open(source_file_path, 'r') as file:
#             text = file.read()
#
#         texte_verif_ponctuation = verif_espace(text)
#
#         with open(destination_file_path, 'w') as file:
#             file.write(texte_verif_ponctuation)
#
#         print(f"Fichier verifié sans ponctuation pour: {filename}")