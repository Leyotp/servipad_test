#app.py
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy #pip install sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash #pip install Werkzeug
from flask_cors import CORS, cross_origin #pip install -U flask-cors
from datetime import timedelta
from flasgger import Swagger, LazyString, LazyJSONEncoder
from flasgger import swag_from
 
import psycopg2 #pip install psycopg2 
import psycopg2.extras
 
app = Flask(__name__)
app.json_encoder = LazyJSONEncoder
  
app.config['SECRET_KEY'] = 'leotrujillo'
  
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)
CORS(app) 
##Database parameters 
DB_HOST = "localhost"
DB_NAME = "sample1"
DB_USER = "postgres"
DB_PASS = "1234"

##Conenction is created, conn being the connection variable 
      
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)  
#Method for hashing the passwords
def hsh(v):
    passhash = generate_password_hash(v)
    return passhash



@cross_origin() 
@app.route('/')
def home():
   
#Verifies if the user is logged in already
    if 'username' in session:
        username = session['username']
        return jsonify({'message' : 'You are already logged in', 'username' : username})
    else:
        resp = jsonify({'message' : 'Unauthorized'})
        resp.status_code = 401
        return resp



@cross_origin()  
@app.route('/login', methods=['POST'])
def login():
    _json = request.json
    _username = _json['username']
    _password = _json['password']
    print(_password)
    # validate the received values
    if _username and _password:
        #check user exists          
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
          
        sql = "SELECT * FROM useracc WHERE username=%s"
        sql_where = (_username,)
          
        cursor.execute(sql, sql_where)
        row = cursor.fetchone()
        username = row['username']
        password = row['password']
        if row:
            if check_password_hash(password, _password):
                session['username'] = username
                cursor.close()
                return jsonify({'message' : 'You are logged in successfully'})
            else:
                resp = jsonify({'message' : 'Bad Request - invalid password'})
                resp.status_code = 400
                return resp
    else:
        resp = jsonify({'message' : 'Bad Request - invalid credendtials'})
        resp.status_code = 400
        return resp

@cross_origin() 
@app.route('/users', methods=['POST'])

def insert_user():
    try:
        _json = request.json
        _username = _json['username']
        _password = hsh(_json['password'])
        _fullname = _json['fullname']

        
    
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        mssg = "insert into useracc ( username, password, fullname) values (%s,%s,%s)" 
        
        mssg_values =( _username, _password, _fullname)

        cursor.execute(mssg, mssg_values)

        resp = jsonify({'message' : 'You have inserted an user successfully'})
        resp.status_code = 200
        conn.commit()
        cursor.close()
        return resp

    except Exception as e: 
        print(e)
        resp1 = jsonify({'message' : 'User could not be inserted'})
        resp1.status_code = 400
        return  resp1

@cross_origin()     
@app.route("/users", methods=['GET'])
def get_user():
    try:
        _json = request.json
        _iduser = _json['id']

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        mssg = "SELECT * FROM useracc WHERE id = %s ;" 
        
        mssg_values =[_iduser]

        cursor.execute(mssg, mssg_values)

        resp = cursor.fetchall()
        dict = {}
        for item in resp:
            dict.update(item)
        
        print(dict)

        ans = jsonify(dict)
        conn.commit()
        cursor.close()
        return ans


    
    except Exception as e: 
        print(e)
        resp1 = jsonify({'message' : 'User could not be returned'})
        resp1.status_code = 400
        return  resp1


        

@cross_origin()     
@app.route("/users", methods=['PUT'])
def update_user():
    try:
        _json = request.json
        _iduser = _json['id']
        _username = _json['username']
        _password = hsh(_json['password'])
        _fullname = _json['fullname']

        _pss = hsh(_password)


        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        mssg = """UPDATE useracc SET username = %s, password= %s, fullname = %s
                WHERE id = %s RETURNING *;""" 

        mssg_values =( _username, _password, _fullname, _iduser)

        cursor.execute(mssg, mssg_values)

        resp = cursor.fetchall()


        ans = jsonify(resp)
        conn.commit()
        cursor.close()
        return ans

        
    except Exception as e: 
        print(e)
        resp1 = jsonify({'message' : 'User could not be updated'})
        resp1.status_code = 400
        return  resp1

@cross_origin()     
@app.route("/users", methods=['DELETE'])
def delete_user():
    try:
        _json = request.json
        _iduser = _json['id']
        


        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        mssg = """DELETE FROM useracc  WHERE id = %s;""" 

        mssg_values =( _iduser)

        cursor.execute(mssg, mssg_values)


        ans = jsonify({'message':'User has been eliminated'})
        conn.commit()
        cursor.close()
        return ans

    except Exception as e: 
        print(e)
        resp1 = jsonify({'message' : 'User could not be deleted'})
        resp1.status_code = 400
        return  resp1

@cross_origin() 
@app.route('/posts', methods=['POST'])

def insert_post():
    try:
        _json = request.json
        _iduser = _json['user_id']
        _title = _json['title']
        _description = _json['description']
        _priority = _json['priority']
        _status = _json['status']

     

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        mssg = "insert into posts (user_id, title, description, priority, status) values (%s,%s,%s,%s,%s)" 
        
        mssg_values =(_iduser, _title, _description, _priority, _status)


        
    
        cursor.execute(mssg, mssg_values)

        resp = jsonify({'message' : 'You have inserted in posts successfully'})
        resp.status_code = 200
        conn.commit()
        cursor.close()
        return resp


    
    except Exception as e: 
        print(e)
        resp1 = jsonify({'message' : 'Post could not be inserted'})
        resp1.status_code = 400
        return  resp1

@cross_origin()     
@app.route("/posts", methods=['GET'])
def get_post():
    try:
        _json = request.json
        _iduser = _json['user_id']

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        mssg = "SELECT * FROM posts WHERE user_id = %s;" 
        
        mssg_values =[_iduser]

        cursor.execute(mssg, mssg_values)

        resp = cursor.fetchall()

        dict = {}
        for item in resp:
            dict.update(item)
        
        print(dict)

        ans = jsonify(dict)
        conn.commit()
        cursor.close()
        return ans


    
    except Exception as e: 
        print(e)
        resp1 = jsonify({'message' : 'Post could not be returned'})
        resp1.status_code = 400
        return  resp1


        

@cross_origin()     
@app.route("/posts", methods=['PUT'])
def update_post():
    try:
        _json = request.json
        _post_id = _json['post_id']
        _iduser = _json['user_id']
        _title = _json['title']
        _description = _json['description']
        _priority = _json['priority']
        _status = _json['status']


        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        mssg = """UPDATE posts SET title = %s, description = %s, priority = %s, status = %s
                WHERE post_id = %s AND user_id = %s RETURNING *;""" 

        mssg_values =( _title, _description, _priority, _status, _post_id, _iduser)

        cursor.execute(mssg, mssg_values)

        resp = cursor.fetchall()


        ans = jsonify(resp)
        conn.commit()
        cursor.close()
        return ans

        
    except Exception as e: 
        print(e)
        resp1 = jsonify({'message' : 'Post could not be updated'})
        resp1.status_code = 400
        return  resp1

@cross_origin()     
@app.route("/posts", methods=['DELETE'])
def delete_post():
    try:
        _json = request.json
        _post_id = _json['post_id']
        _iduser = _json['user_id']
        


        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        mssg = """DELETE FROM posts WHERE post_id = %s AND user_id = %s;""" 

        mssg_values =( _post_id, _iduser)

        cursor.execute(mssg, mssg_values)


        ans = jsonify({'message':'Post has been eliminated'})
        conn.commit()
        cursor.close()
        return ans

    except Exception as e: 
        print(e)
        resp1 = jsonify({'message' : 'Post could not be eliminated'})
        resp1.status_code = 400
        return  resp1
##Logs out and closes session
@cross_origin()
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message' : 'You successfully logged out'})
          
if __name__ == "__main__":
    app.run()