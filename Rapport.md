<h1 style="text-align: center">Rapport devoir maison <br>-<br> Sécurité</h1>

<p style="text-align: center">Par FERNANDES DOS SANTOS Emanuel et LAGARDE Tristan</p>


## Exercice 1
Les deux mots de passe utilisés sont :
- `tungsten` pour les utilisateurs `Bart`, `Homer`, `Lisa` et `March`
- `123456789` pour les utilisateurs `Bob`, `Carlton`, `John` et `William`

En effet, le hash SHA-256 de `tungsten` est `068be8be83f9bfafd1545d357fd3cd132f8c659effd11e635a698811b796c880` et celui de `123456789` est `15e2b0d3c33891ebb0f1ef609ec419420c20e320ce94c65fbc8c3312448eb225`, ce qui correspond respectivement aux deux hashs.

## Exercice 2
### 1.
Voici le code de `AjouterUtilisateur()`:
```python
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
```

### 2.
Voici le code ajouté à la fin de la fonction `AjouterUtilisateur()`:
```python
def AjoutUtilisateur() -> None:
    ...
    
    ## Affichage de la BDD
    cursor.execute("SELECT * FROM utilisateurs")
    print(cursor.fetchall())
```