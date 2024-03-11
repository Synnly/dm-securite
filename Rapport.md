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

### 3.
Voici le code de `Verifer()`:
```python
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
```
### 4.
Voici le code de `InsererUtilisateurSHA256()` et `VerificationSHA256()`:
```python
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
```
```python
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
```

### 5.

Voici le code de `InsererUtilisateurSHA256SelConstant()` et `VerificationSHA256SelConstant()` avec la constante `SEL` définie par `SEL = "CRYPTE"`:

```python
def InsererUtilisateurSHA256SelConstant(nom: str, password: str) -> bool:
    """
    Insere un utilisateur avec le mot de passe haché en SHA-256 et avec un sel constant
    :param nom: Le nom de l'utilisateur
    :param password: Le mot de passe de l'utilisateur
    :return: True si l'insertion a réussi, False sinon
    """
    
    return InsererUtilisateurSHA256(nom, SEL+password)
```

```python
def VerificationSHA256SelConstant() -> bool:
    """
    Authentifie un utilisateur en utilisant le haché SHA-256 du mot de passe avec un sel constant

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
    password_hashed_salted = SEL + hashlib.sha256(password.encode('utf-8')).hexdigest()
    cursor.execute("SELECT * FROM utilisateurs WHERE name='{}' AND password='{}'".format(nom, password_hashed_salted))
    return cursor.fetchone() is not None
```

### 6.
En début de programme, on ajoute la ligne :
```python
cursor.execute("CREATE TABLE sels (salt TEXT, name TEXT)")
```
Voici le code des fonctions `InsererUtilisateurSHA256SelAleatoire()`  et `VerificationSHA256SelAleatoire()`:
```python
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
```

```python
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
```

## Exercice 3

### 1.
L'attaque bruteforce commence à 9h01 (et 24s).

### 2.
L'attaquant a essayé les extensions `.phtml`, `.php`, `.php3`, `.php4`, `.php5`, `.php6`, `.php7` et `.phar`.

### 3.
L'attaquant utilise l'extension `.phar`.

### 4.
Il récupère une fiche de poste, le renomme, s'octroie les autorisations pour pouvoir exécuter le fichier et l'execute.

## Exercice 5
Les 3 identifiants trouvés sont :

|Login|Mot de passe|
|-----|------| 
|insite|2getin|
|xruser|4$xray|
|root|#superxr|
Ces identifiants ont été trouvés grâce au CVE n° CVE-2014-7232.