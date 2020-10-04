# Messaging System
simple rest API backend system that responsible of handling messages between users


## Users Information & Token

This table contains the existing users for checking the API

| id | Token |
| --- | --- |
| 1 | b34e9deda41bf4f1c8a6c7f6810f4f3e40633d09 **(admin user)** |
| 2 | d1d6c01a1c5012b37fa95200e0ccedc19f527fba |
| 3 | 938497947c814be0d032ac6e686e893c7289687f |
| 4 | f50d5e4f9b4643c26eb6bac0a5fcf739dad7a2f7 |

# REST API
The REST API to the example app is described below.
link to the site:

> http://msg-sys.herokuapp.com/api

## Get all messages for a specific user

### Request(for admin user)

`GET /api/get-all-messages?user_id=id`

### Response

``` HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/19.9.0
Date: Sun, 04 Oct 2020 13:18:58 GMT
Content-Type: application/json
Vary: Accept
Allow: OPTIONS, GET
X-Frame-Options: SAMEORIGIN
Content-Length: 366
Via: 1.1 vegur 
```
### Body

```{
        "id": 10,
        "sender_id": 3,
        "receiver_id": 2,
        "message": "hello user 2 :) , nice to meet you!",
        "subject": "hey user 2",
        "creation_date": "2020-10-04",
        "read": false,
        "visible": true
 }
 ```

### Request(for authenticated user)

`GET /api/get-all-messages?user_id=id`

### Response

``` HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/19.9.0
Date: Sun, 04 Oct 2020 13:18:58 GMT
Content-Type: application/json
Vary: Accept
Allow: OPTIONS, GET
X-Frame-Options: SAMEORIGIN
Content-Length: 366
Via: 1.1 vegur 
```
### Body

```{
        "id": 10,
        "sender_id": 3,
        "receiver_id": 2,
        "message": "hello user 2 :) , nice to meet you!",
        "subject": "hey user 2",
        "creation_date": "2020-10-04",
        "read": false,
        "visible": true
 }```

