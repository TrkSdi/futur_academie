# Future Academie

## Admin access / Using HoneyPot

Access to Django administration is via this URL {host}/admin_future/

## Migrations Master :

PIERRICK  
RACHEL

## Djoser & JWT : User authentication and management

### Create en account

POST {host}/auth/users/

_Data example_

```{
            "email": "example@example.com",
            "username": "exampleUsername",
            "password" : "examplePWD"
        }
```

### Create tokens

POST {host}/auth/jwt/create/ with the same data

```{
            "email": "example@example.com",
            "username": "exampleUsername",
            "password" : "examplePWD"
        }
```

### Logout

{host}/logout POST :

_Data example_

```
{
    "refresh": "tokenrefresh.tokenrefresh",
}


```

### All commands

URL: {host}/auth/users/ Method: POST Body: JSON with username, email, password Connexion:

URL: {host}/auth/jwt/create/ Method: POST Body: JSON with username, password

**To obtain the tokens**  
URL : {host}/auth/jwt/token/

**Protected endpoint :**  
URL: {host}/protected-endpoint/ Method: GET Headers: Authorization: Bearer <your_access_token>

**to refresh the token**  
URL: {host}/auth/jwt/refresh/ Method: POST Body: JSON with refresh: <your_refresh_token>

**2 sorts of tokens**

```{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwNTU3MTcwNywiaWF0IjoxNzA1NDg1MzA3LCJqdGkiOiIxNjAwNjI3YzAwMmQ0ODM3OTA4YjgwMzcxZTE1OWY4MyIsInVzZXJfaWQiOiJjNDUxOGEwYy01ODRjLTQ4NGEtODY4ZC01NmI4ZDY5YTUwNzIifQ.gE8rcZ4EJ_IBjiqs5dP-_3hz4B5tQx_VfYe0xVWwdnY",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA1NDg2ODA3LCJpYXQiOjE3MDU0ODUzMDcsImp0aSI6ImI2Mjk1ZjRjNWIzNTQyZTNiNGYyZjVhYjJlMGEyYjk2IiwidXNlcl9pZCI6ImM0NTE4YTBjLTU4NGMtNDg0YS04NjhkLTU2YjhkNjlhNTA3MiJ9.EddtHbQW2L3iPKQy3ZUTQz7lURgs0X-oECIkzETvRTc"
}
```
