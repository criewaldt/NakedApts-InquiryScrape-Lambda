from nakedinquiry_lambda import main

#Incorrect login
assert main({'auth':{
                'username':'aziff@nylivingsolutions.com',
                'password':'teamziff19765'},}, 'context') == None

#Correct login
assert main({'auth':{
                'username':'aziff@nylivingsolutions.com',
                'password':'teamziff1976'},}, 'context')

