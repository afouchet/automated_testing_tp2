# TP2: Tester une application de réservation de cinéma

Dans ce TD, nous allons tester et implémenter une application "BookMovie", où
les utilisateurs peuvent lister les films à l'affiche avec les séances dans
diverses salles, et réserver leur place. <br/>
Les salles de cinéma peuvent déclarer leurs séances, car elles ont des
utilisateurs spéciaux et ont des "entry points" pour déclarer leurs séances. <br/>
Elles peuvent aussi annuler des séances.

## Partie 1: Tests Gherkin

J'ai mis quelques tests Gherkin dans specs/user.spec, pour créer un
utilisateur. <br/>
J'ai aussi créé un test specs/booking.spec, pour le cas où l'utilisateur veut
réserver une place et nous devons contacter le cinéma. Ce test-là n'est pas
complet, et sera modifié plus tard.

Dans votre groupe, réfléchissez aux cas d'usages de l'application:
- Que pourra faire un utilisateur normal ?
- Que pourra faire un utilisateur "salle de cinéma" ?

Traduisez ces besoins en tests gherkin, dans des fichiers specs/user.spec,
specs/theater.spec, specs/booking.spec, ou autre.

## Partie 2: Implémentation

J'ai mis en place plusieurs services et tests, pour que vous puissiez lire
comment ça marche et vous servir de ça comme point de départ.

Je détaille des premières implémentations pour que vous preniez en main ce
framework.

Ensuite, vous devez être capable d'implémenter toutes les features de BookMovie

### Explication du fonctionnement du Framework Django

Django fonctionne avec une mentalité modulaire, où on fait des apps qui ont un
seul rôle et qui sont ré-utilisables.

Il prend en charge beaucoup de choses pour nous, nous permettant de nous concentrer sur __notre logique métier: afficher et réserver des films___.

Le dossier "book_movie/" est un peu la maison-mère du projet, qui contient les apps à installer, comment se connecter à la base de données, etc. Nous ne devrions rien y changer

Nous allons mettre notre code dans "core/" (le coeur de notre application). <br/>
Nous pourrions nommer ce dossier différemment, mais ce n'est pas le sujet.

Dans une app Django, nous avons:
- urls.py: le fichier listant les URLs. Quand quelqu'un appelle l'URL "http://book_mvies.com/foo", utiliser la fonction views.foo(request) -> response
- views.py: le fichier avec les fonctions request -> response
- models.py: le fichier avec les différents objets que l'on veut stocker en base. On peut avoir un objet User, avec les champs nom, email, etc. Un objet Cinema avec les champs nom, adresse, propriétaire, etc
- tests/: nos tests (unitaires, d'intégrations, pour les specs)


### Vérifier que tout fonctionne

Faites les commandes:
```bash
# Installe les packages
uv sync

# Créer la base de données
uv run python manage.py makemigrations
uv run python manage.py migrate

# Run les test
uv run pytest
```

Normalement, cela devrait fonctionner et vous devriez voir 2 tests verts

### Implémentation #1: Un utilisateur propriétaire de salle de cinéma

Tout d'abord, parmi nos utilisateurs, nous voudrions distinguer 2 types:
- Les utilisateurs normaux, qui vont lister des films, réserver des séances
- Les utilisateurs propriétaires de salles de cinéma, qui peuvent déclarer des salles et les séances de leurs films.

Ajouter à specs/user.spec le test suivant:
```gherkin
Scenario: Create a company user
  Given nothing
  When user sends username, password, email and is_company=True
  Then a "company" account is created
```

On créé le test d'API en s'inspirant des tests utilisateurs précédents de core/tests/specs/test_user.py

Créons le test où quelqu'un créer un utilisateur "is_company = True" dans core/tests/test_user.py

```python
@pytest.mark.django_db
def test_create_user__company_case(client):
    # Given
    user_payload = {
        "name": "UGC",
        "email": "ugc@ugc.com",
	"password": "I_am_Bob",
        "is_company": True,
    }

    # When
    response = client.post(
        "/core/user/create/",
        user_payload,
        content_type="application/json",
    )
    created_user = response.json()
    response = client.get(
        f"/core/user/get/?id={created_user['id']}",
    )
    
    # Then
    assert response.status_code == 200
    assert response.json() == {
        "id": created_user["id"],
        "username": "UGC",
        "email": "ugc@ugc.com",
        "is_company": True
    }
```

Vous lancer `uv run pytest`, votre test est rouge.


Dans core/models.py, on va modifier l'objet BookUser pour contenir le champ "is_company"
```python
    is_company = models.BooleanField(default=False)
```

Puis on exécute les commandes suivantes pour mettre à jour les bases de données:
```bash
uv run python manage.py makemigrations
uv run python manage.py migrate
```

Maintenant, changer le code dans views.py pour que le test passe vert. <br/>
Vous devrez peut-être changer la fixture user_bob.

### Implémentation #2: Déclarer une salle de cinéma

On veut maintenant qu'un utilisateur propriétaire de salles puisse déclarer ses
salles. <br>/
Ajouter ce test Gherkin dans specs/theater.spec:

```gherkin
Scenario: Create a theater
  Given a company user
  When user sends address + theater name
  Then a theater is created
```

Dans core/tests/fixtures.py, créez une fixture user_company, similaire à
"user_bob", à l'exception que cet utilisateur est "is_company=True".<br/>

Dans core/tests/spec/test_theater.py, créé un test, similaire à
test_create_user, à l'exception que celui-ci va utiliser la fixture
"user_company" et créer une salle, en utilisant l'url
"/core/theater/create".<br/>

Faites tourner pytest, le test est rouge.

Dans core/models.py, ajouter un objet "Theater" avec les champs qui vont bien.
<br/>
Faites "python manage.py makemigrations" "python manage.py migrate" pour mettre
à jour la base de données.

Dans core/urls.py, ajoutez l'entry point "/theater/create/", appelant
views.create_theater<br/>
Dans core/views.py, faites la fonction create_theater qui va créer l'objet Theater.

### A vous de jouer

Maintenant, vous pouvez créer les features dans l'ordre que vous souhaitez.

A la fin, il faut:
- Qu'un propriétaire de cinéma puis déclarer des salles, et les séances des films
- Qu'un utilisateur puisse voir la liste des films à l'affiche, et, pour un film, la liste des salles qui le diffusent avec les horaires
- Que l'utilisateur puisse réserver une séance, avec notre code qui callerait
l'API du fournisseur de salle. Dans nos tests, on va mocker l'API.
- Cas intéressant: supposez que vous avez plusieurs fournisseurs de salles (MK2, UGC, Gaumont), avec chacun leur API, avec des signatures différentes. Faites que votre code appelle la bonne API selon le fournisseur.
