# NakedApts-InquiryScrape 
AWS Lambda to scrape and return inquiry data from NakedApartments account

## Requires 
AWS DynamoDB read/write permission 

DynamoDB table: `advertapi-proxylist`

Schema:
    
    {
    "ip" : "STRING",
    "lastused" : `datetime.datetime.utcnow()`,
    "password" : "mypassword",
    "port" : "12345",
    "username" : "myusername"
    }
**This tool uses AWS region: us-east-1** 

## Example Usage 
``` python
inquiries = main({'auth':{
                'username':'someone@somewhere.com',
                'password':'someonespassword'},}, 'context')
```
This will return an array of arrays 
``` python
[["MONTH", "DAY", "YEAR"],...]
```