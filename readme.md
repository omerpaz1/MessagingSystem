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
using Token for authentications users

### Request
for admin authenticated user, for example: id = 2

`GET /api/get-all-messages?user_id=2`

### Response

``` 
HTTP/1.1 200 OK
```
### Body

```
]
        {
        "id": 10,
        "sender_id": 3,
        "receiver_id": 2,
        "message": "hello user 2 :) , nice to meet you!",
        "subject": "hey user 2",
        "creation_date": "2020-10-04",
        "read": false,
        "visible": true
        }
]
 ```
 ## New message

### Request

`POST /api/new-message`

#### Request Body
```
sender: "2"
receiver: "4"
msg: "hello user 4 :) , nice to meet you!"
subject: "hey user 4"
 ```

### Response

``` 
HTTP/1.1 200 OK
```
### Body

```
The message was created successfully
 ```

### Request
for authenticated user, for example: id = 3

`GET /api/get-all-messages`

### Response

``` 
HTTP/1.1 200 OK
```
### Body
```
[
    {
        "id": 7,
        "sender_id": 4,
        "receiver_id": 3,
        "message": "hello user 3 :) , nice to meet you!",
        "subject": "hey user 3",
        "creation_date": "2020-10-04",
        "read": true,
        "visible": true
    }
]
 ```
 
 ## Get all unread messages for a specific user
using Token for authentications users

### Request
for admin authenticated user, for example: id = 4

`GET /api/get-all-unread-messages?user_id=4`

### Response

```
HTTP/1.1 200 OK

```
### Body

```
[
    {
        "id": 5,
        "sender_id": 3,
        "receiver_id": 4,
        "message": "hello user 4 :) , nice to meet you!",
        "subject": "hey user 4",
        "creation_date": "2020-10-04",
        "read": false,
        "visible": true
    },
    {
        "id": 9,
        "sender_id": 2,
        "receiver_id": 4,
        "message": "hello user 4 :) , nice to meet you!",
        "subject": "hey user 4",
        "creation_date": "2020-10-04",
        "read": false,
        "visible": true
    },
    {
        "id": 12,
        "sender_id": 3,
        "receiver_id": 4,
        "message": "hello user 4 :) , nice to meet you!",
        "subject": "hey user 4",
        "creation_date": "2020-10-04",
        "read": false,
        "visible": true
    }
]

 ```
 
 ### Request
for authenticated user, for example: id = 2

`GET /api/get-all-unread-messages`

### Response

``` 
HTTP/1.1 200 OK
```
### Body

```
[
    {
        "id": 6,
        "sender_id": 4,
        "receiver_id": 2,
        "message": "hello user 2 :) , nice to meet you!",
        "subject": "hey user 2",
        "creation_date": "2020-10-04",
        "read": false,
        "visible": true
    },
    {
        "id": 8,
        "sender_id": 3,
        "receiver_id": 2,
        "message": "hello user 2 :) , nice to meet you!",
        "subject": "hey user 2",
        "creation_date": "2020-10-04",
        "read": false,
        "visible": true
    },
    {
        "id": 10,
        "sender_id": 3,
        "receiver_id": 2,
        "message": "hello user 2 :) , nice to meet you!",
        "subject": "hey user 2",
        "creation_date": "2020-10-04",
        "read": false,
        "visible": true
    },
    {
        "id": 11,
        "sender_id": 4,
        "receiver_id": 2,
        "message": "hello user 2 :) , nice to meet you!",
        "subject": "hey user 2",
        "creation_date": "2020-10-04",
        "read": false,
        "visible": true
    }
]

 ```
 
## Read message
using parameters without authentication

### Request
for example: id = 2

`PUT /api/read-message?user_id=2`

### Response

``` 
HTTP/1.1 200 OK
```
 
### Body
The field 'read' become 'true' , then it will not apper in the unreaded messages anymore.

```
{
    "id": 11,
    "sender": 4,
    "receiver": 2,
    "message": "hello user 2 :) , nice to meet you!",
    "subject": "hey user 2",
    "creation_date": "2020-10-04",
    "read": true,
    "visible": true
}

```

## Delete message
using Token for authentication users

### Request
for admin authenticated user, for example: id = 2 , msg id = 11 (the message from the 'read message' example)

`DELETE /api/delete-message?user_id=2&msg_id=11`

### Response

```
HTTP/1.1 200 OK
```
### Body
```
The message was deleted successfully
```


