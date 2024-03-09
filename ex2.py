import hashlib
import sqlite3
import random

# Connexion et curseur
connection = sqlite3.connect("donnees.db")
cursor = connection.cursor()

# Sel
SEL = "CRYPTE"

#cursor.execute("CREATE TABLE utilisateurs (name TEXT, password TEXT)")
cursor.execute("CREATE TABLE sels (salt TEXT, name TEXT)")


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

    InsererUtilisateurSHA256SelAleatoire(nom, password)
    print("Utilisateur {} ajouté".format(nom))

    ## Affichage de la BDD
    cursor.execute("SELECT * FROM utilisateurs")
    print(cursor.fetchall())


def Verification() -> bool:
    """
    Authentifie un utilisateur.

    :return: True si le tuple (nom, mot de passe) entrés correspondent et sont présents dans la BDD, False sinon
    """

    # Demande du nom
    demander_name = True
    while demander_name:
        nom = input("Entrer votre nom :\n> ")
        cursor.execute("SELECT name FROM utilisateurs WHERE name='{}'".format(nom))

        # Le nom existe donc sortie de boucle
        if cursor.fetchone() is not None:
            break

        print("Le nom n'existe pas")

    # Demande du mot de passe
    password = input("Entrer votre mot de passe :\n> ")

    # Verification du mot de passe
    cursor.execute("SELECT * FROM utilisateurs WHERE name='{}' AND password='{}'".format(nom, password))
    return cursor.fetchone() is not None


def InsererUtilisateurSHA256(nom: str, password: str) -> bool:
    """
    Insere un utilisateur avec le mot de passe haché en SHA-256
    :param nom: Le nom de l'utilisateur
    :param password: Le mot de passe de l'utilisateur
    :return: True si l'insertion a réussi, False sinon
    """

    cursor.execute("SELECT * FROM utilisateurs WHERE name='{}' AND password='{}'".format(nom, password))

    # Un utilisateur avec ce nom existe déjà
    if cursor.fetchone() is not None:
        return False

    # Hachage et insertion
    password_hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor.execute("INSERT INTO utilisateurs VALUES ('{}', '{}')".format(nom, password_hashed))

    return True


def VerificationSHA256() -> bool:
    """
    Authentifie un utilisateur en utilisant le haché SHA-256 du mot de passe

    :return: True si le tuple (nom, mot de passe) entrés correspondent et sont présents dans la BDD, False sinon
    """

    # Demande du nom
    demander_name = True
    while demander_name:
        nom = input("Entrer votre nom :\n> ")
        cursor.execute("SELECT name FROM utilisateurs WHERE name='{}'".format(nom))

        # Le nom existe donc sortie de boucle
        if cursor.fetchone() is not None:
            break

        print("Le nom n'existe pas")

    # Demande du mot de passe
    password = input("Entrer votre mot de passe :\n> ")

    # Verification du mot de passe
    password_hashed = hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor.execute("SELECT * FROM utilisateurs WHERE name='{}' AND password='{}'".format(nom, password_hashed))
    return cursor.fetchone() is not None


def InsererUtilisateurSHA256SelAleatoire(nom: str, password: str) -> bool:
    """
    Insere un utilisateur avec le mot de passe haché en SHA-256 et avec un sel aléatoire
    :param nom: Le nom de l'utilisateur
    :param password: Le mot de passe de l'utilisateur
    :return: True si l'insertion a réussi, False sinon
    """

    cursor.execute("SELECT * FROM utilisateurs WHERE name='{}' AND password='{}'".format(nom, password))

    # Un utilisateur avec ce nom existe déjà
    if cursor.fetchone() is not None:
        return False

    # Hachage, salage et insertion
    sel = random.randbytes(16).hex()
    password_hashed_salted = sel + hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor.execute("INSERT INTO utilisateurs VALUES ('{}', '{}')".format(nom, password_hashed_salted))
    cursor.execute("INSERT INTO sels VALUES ('{}', '{}')".format(sel, nom))

    return True


def VerificationSHA256SelAleatoire() -> bool:
    """
    Authentifie un utilisateur en utilisant le haché SHA-256 du mot de passe avec un sel aléatoire

    :return: True si le tuple (nom, mot de passe) entrés correspondent et sont présents dans la BDD, False sinon
    """

    # Demande du nom
    demander_name = True
    while demander_name:
        nom = input("Entrer votre nom :\n> ")
        cursor.execute("SELECT name FROM utilisateurs WHERE name='{}'".format(nom))

        # Le nom existe donc sortie de boucle
        if cursor.fetchone() is not None:
            break

        print("Le nom n'existe pas")

    # Demande du mot de passe
    password = input("Entrer votre mot de passe :\n> ")

    # Recuperation du sel
    cursor.execute("SELECT salt from sels WHERE name='{}'".format(nom))
    sel = cursor.fetchone()

    # Verification du mot de passe
    password_hashed_salted = sel + hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor.execute("SELECT * FROM utilisateurs u, sels s WHERE s.name = u.name AND u.name='{}' AND password='{}'".format(nom, password_hashed_salted))
    return cursor.fetchone() is not None


def main():
    while True:
        AjoutUtilisateur()

main()
