# Future Academie

## Admin access / Using HoneyPot

Access to Django administration is via this URL {host}/admin_future/

## Migrations Master :

PIERRICK  
RACHEL

## Djoser & JWT

### POST an user

POST {host}/auth/users/  
data

```{
            "email": "user29@test.com",
            "username": "TestUser1",
            "password" : "aoziehrqsdf"
        }
```

(change the data please)

### Logout with simple Token

{host}/logout2/ will delete the token of the user



### Tests in Postman

Enregistrement:

URL: {host}/auth/users/
Méthode: POST
Corps: JSON avec username, email, password
Connexion:

URL: {host}/auth/jwt/create/
Méthode: POST
Corps: JSON avec username, password
Accès Protégé:

URL: {host}/protected-endpoint/
Méthode: GET
Headers: Authorization: Bearer <your_access_token>
Rafraîchissement de Token:

URL: {host}/auth/jwt/refresh/
Méthode: POST
Corps: JSON avec refresh: <your_refresh_token>

