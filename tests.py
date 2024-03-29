import json
from nakedinquiry_lambda import main

with open('nakedcreds.json') as data_file:    
    creds = json.load(data_file)
username  = creds['username']
password = creds['password']
incorrect_password = "definitelyNotThePassword"

#Incorrect login
def incorrectLogin():
    assert main({'username': username,
                'password': incorrect_password,
                }, 'context') == None

    return True

#Correct login
def correctLogin():
    assert main({'username' : username,
                'password' : password,
                }, 'context')
    return True

if __name__ == "__main__":

    print incorrectLogin()
    print correctLogin()
