Pycharm ChatBot
Ce projet consiste à créer un mini chatbot en Python, utilisant la méthode TF-IDF (Term Frequency-Inverse Document Frequency) pour analyser et traiter des données dans un ensemble de documents.

Membres du groupe :
- Samy AIT ALLA
- Anis DALY

Lien Github :
https://github.com/Samy2700/pychatbot-aitalla-daly-A.git

Fonctionnalités principale:
- texte_modifié
- score_tf
- score_idf
- matrice_tf_idf
- transposer_matrice
- mots_moins_importants
- mot_plus_haut_score
- mot_chirac
- occurences_nation
- premier_president_a_parler
- afficher_premier_president
- affichage_menu

Notice d'Utilisation :
- Bibliothèques Python : math, os
- Configurez les chemins globaux dans main.py à savoir:
        - source_directory : chemin vers le dossier source "speeches"
        - destination_directory : chemin vers le dossier de destination "cleaned"
- Les fichiers modifiés doivent être stocker dans un nouveau dossier "cleaned" qui se situe au même niveau que le programme main.py et le dossier "speeches".

Dépendances à installer :
- Installation de python (préférablement la version la plus récente)
- Installation de Git

Liste des bugs connus :
- Problèmes de chemins de fichiers : Les utilisateurs peuvent rencontrer des problèmes concernant les chemins de dossier s'ils ne sont pas correctement configurés ou s'ils ne sont pas compatibles avec leur système d'exploitation
- Erreurs de compatibilité de Version Python :

Solution :
- Vérifier et ajuster manuellement les chemins avant le lancement du programme
- Télécharger la version la plus récente de Python
