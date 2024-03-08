import sqlite3

# Connexion et curseur
connection = sqlite3.connect("donnees.db")
cursor = connection.cursor()

#cursor.execute("CREATE TABLE utilisateurs (name TEXT, password TEXT)")


def AjoutUtilisateur() -> None:
    """
    Demande un login et un mot de passe à l'utilisateur. Affiche le contenu de la
    BDD à la fin de l'execution de la fonction
    """

    nom = ""
    password = ""

    # Demande du nom
    demander_name = True
    while demander_name:
        nom = input("Entrer votre nom :\n> ")
        cursor.execute("SELECT name FROM utilisateurs WHERE name='{}'".format(nom))

        # Le nom est libre donc sortie de boucle
        if cursor.fetchone() is None:
            break

        print("Le nom est déjà utilisé")

    # Demande du mot de passe
    confirmation_invalide = True
    while confirmation_invalide:
        password = input("Entrer votre mot de passe :\n> ")
        confirmation = input("Entrer à nouveau votre mot de passe :\n> ")

        if password == confirmation:
            break

        print("Les mots de passe sont différents")

    cursor.execute("INSERT INTO utilisateurs VALUES (?, ?)", (nom, password))
    print("Utilisateur {} ajouté".format(nom))

    ## Affichage de la BDD
    cursor.execute("SELECT * FROM utilisateurs")
    print(cursor.fetchall())

def Verifier() -> None:
    """
    Authentifie un utilisateur.
    """

def main():
    while True:
        AjoutUtilisateur()

main()
