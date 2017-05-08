import json
from nakedinquiry_lambda import main

with open('nakedcreds.json') as data_file:    
    creds = json.load(data_file)
username  = creds['username']
password = creds['password']
incorrect_password = "thisIsthewrongpassword"

#Incorrect login
assert main({'auth':{
                'username': username,
                'password': password,
                }}, 'context') == None

#Correct login
assert main({'auth':{
                'username' : username,
                'password' : incorrect_password,
                }}, 'context')

