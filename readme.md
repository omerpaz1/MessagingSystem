# Messaging System
simple rest API backend system that responsible of handling messages between users

# REST API
The REST API to the example app is described below.
link to the site:

> http://msg-sys.herokuapp.com/api

## Users Information & Token

This table contains the existing users for checking the API

| User_id | Token |
| --- | --- |
| 1 | b34e9deda41bf4f1c8a6c7f6810f4f3e40633d09 **(admin user)** |
| 2 | d1d6c01a1c5012b37fa95200e0ccedc19f527fba |
| 3 | 938497947c814be0d032ac6e686e893c7289687f |
| 4 | f50d5e4f9b4643c26eb6bac0a5fcf739dad7a2f7 |

## Get all messages

### Request(as superuser)

`GET /api/get-all-messages`

    curl -i -H 'Accept: application/json' http://localhost:7000/thing/

### Response

    HTTP/1.1 200 OK
    Date: Thu, 24 Feb 2011 12:36:30 GMT
    Status: 200 OK
    Connection: close
    Content-Type: application/json
    Content-Length: 2

    []
