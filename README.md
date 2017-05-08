# NakedApts-InquiryScrape 
AWS Lambda to scrape and return inquiry data from NakedApartments account

## Requires 
AWS DynamoDB read/write permission and accompanying `awscreds.json` file 

`awscreds.json` schema:

    "id" : "STRING",
    "key" : "STRING",
    "region" : "STRING"

DynamoDB table: `advertapi-proxylist` populated with HTTPS proxy info and login credentials 

`advertapi-proxylist` schema:
    
    "ip" : "STRING",
    "lastused" : datetime.datetime.utcnow(),
    "password" : "STRING",
    "port" : "STRING",
    "username" : "STRING"

## Example Usage

_test.py_
``` python
from nakedinquiry_lambda import main
main({
    'auth': {
        'username':'someone@somewhere.com',
        'password':'someonespassword'
        },
    }, 'context')
```
This will return a JSON object 
``` python
{
    "count" : "STRING",
    "data" : inquiries,
    "user" : "STRING"
}
```
count = total inquiry count
data = [["MONTH", "DAY", "YEAR"],...]
user = the username of the person you scraped inquiries for