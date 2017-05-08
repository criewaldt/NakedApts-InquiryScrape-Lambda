import json
from nakedinquiry_lambda import main

with open('nakedcreds.json') as data_file:    
    creds = json.load(data_file)
username  = creds['username']
password = creds['password']
incorrect_password = "thisIsthewrongpassword"


#Incorrect login
def incorrectLogin():
    assert main({'auth':{
                'username': username,
                'password': incorrect_password,
                }}, 'context') == None

#Correct login
def correctLogin():
    assert main({'auth':{
                    'username' : username,
                    'password' : password,
                    }}, 'context')

if __name__ == "__main__":
    print "Incorrect login:", incorrectLogin()
    print "Correct login:", correctLogin()
