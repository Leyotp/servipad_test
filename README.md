# Install all of the dependencies via pip 
#pip install -U flask-cors
#pip install psycopg2
pip install sqlalchemy
pip install Werkzeug
pip install flasgger

#Import sample1 database, there's  default user already created, username: user, passowrd: test

#Utilize Insomnia or any type of API request software to test it out, 

#The route /users has 4 methods: PUT, POST, GET and DELETE

for GET the format should be {"id": " "}

for POST the format should be {"username": " ", 
                                "password": " ",
                                "fullname": ""}

for UPDATE the format should be {"username": " ", 
                                "password": " ",
                                "fullname": ""}

for DELETE the format should be {"id": " "}       


#The route /POSTS has 4 methods: PUT, POST, GET and DELETE

for GET the format should be {"user_id": " "}

for POST the format should be {"title": " ", 
                                "description": " ",
                                "priority": " ",
                                "priority": " "}

for UPDATE the format should be {"title": " ", 
                                "description": " ",
                                "priority": " ",
                                "priority": " ",
                                "post_id": " "}
                                "user_id": " "}

for DELETE the format should be {"post_id": " ",
                                "user_id": ""}   
