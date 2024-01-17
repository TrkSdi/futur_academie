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

URL: {host}/auth/users/ Méthode: POST Corps: JSON avec username, email, password Connexion:


URL: {host}/auth/jwt/create/ Méthode: POST Corps: JSON avec username, password Accès Protégé:

URL: {host}/protected-endpoint/ Méthode: GET Headers: Authorization: Bearer <your_access_token> Rafraîchissement de Token:

URL: {host}/auth/jwt/refresh/ Méthode: POST Corps: JSON avec refresh: <your_refresh_token>

2 sortes de token

```{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNTU3MTcwNywiaWF0IjoxNzA1NDg1MzA3LCJqdGkiOiIxNjAwNjI3YzAwMmQ0ODM3OTA4YjgwMzcxZTE1OWY4MyIsInVzZXJfaWQiOiJjNDUxOGEwYy01ODRjLTQ4NGEtODY4ZC01NmI4ZDY5YTUwNzIifQ.gE8rcZ4EJ_IBjiqs5dP-_3hz4B5tQx_VfYe0xVWwdnY",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA1NDg2ODA3LCJpYXQiOjE3MDU0ODUzMDcsImp0aSI6ImI2Mjk1ZjRjNWIzNTQyZTNiNGYyZjVhYjJlMGEyYjk2IiwidXNlcl9pZCI6ImM0NTE4YTBjLTU4NGMtNDg0YS04NjhkLTU2YjhkNjlhNTA3MiJ9.EddtHbQW2L3iPKQy3ZUTQz7lURgs0X-oECIkzETvRTc"
}
```


## test du logout
Create an user and got to http://localhost:8001/auth/jwt/create/
to have the tokens


```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNTU4MjExMCwiaWF0IjoxNzA1NDk1NzEwLCJqdGkiOiJmNWY2MDg3YWNhNGE0MDk3YmVlODBmMjA3MTA0MmMyYSIsInVzZXJfaWQiOiI4OWYxM2UxYS01ODBlLTRmYzQtOGQxMy02YmMwNDQ4Y2IwNzAifQ.uKPAtkVhYIfjxrW_Mrcl6TU_7-Lu0ThrXQOWUFRp2LQ",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA1NDk3MjEwLCJpYXQiOjE3MDU0OTU3MTAsImp0aSI6ImFhMTQ4ZDIyNzIzMjQyODg4NGI3OGYzYWVlMTk5MDU5IiwidXNlcl9pZCI6Ijg5ZjEzZTFhLTU4MGUtNGZjNC04ZDEzLTZiYzA0NDhjYjA3MCJ9.vh59nTxjmZgqVyQbPdkxef4HvSK7W6ndBapavaej-iw"
}


```


go to logoutView : 
POST : 

```
{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNTU4MjExMCwiaWF0IjoxNzA1NDk1NzEwLCJqdGkiOiJmNWY2MDg3YWNhNGE0MDk3YmVlODBmMjA3MTA0MmMyYSIsInVzZXJfaWQiOiI4OWYxM2UxYS01ODBlLTRmYzQtOGQxMy02YmMwNDQ4Y2IwNzAifQ.uKPAtkVhYIfjxrW_Mrcl6TU_7-Lu0ThrXQOWUFRp2LQ",
}


```