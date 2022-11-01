#app.py
from flask import Flask, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin #pip install -U flask-cors
from datetime import timedelta
 
import psycopg2 #pip install psycopg2 
import psycopg2.extras
 
app = Flask(__name__)
  
app.config['SECRET_KEY'] = 'leotrujillo'
  
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=10)
CORS(app) 
 
DB_HOST = "localhost"
DB_NAME = "sample1"
DB_USER = "postgres"
DB_PASS = "1234"
     
conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)  

@cross_origin() 
@app.route('/')
def home():
    passhash = generate_password_hash('asd')
    print(passhash)
    return passhash
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
        _title = _json['title']
        _priority = _json['priority']
        _status = _json['status']

     

        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        mssg = "SELECT * FROM posts WHERE user_id = %s  AND title = %s OR priority = %s OR status = %s ;" 
        
        mssg_values =(_iduser, _title, _priority, _status)


        
    
        cursor.execute(mssg, mssg_values)

        resp = cursor.fetchall()

        ans = jsonify({'message' : resp })
        resp.status_code = 200
        conn.commit()
        cursor.close()
        conn.close()
        return ans


    
    except Exception as e: 
        print(e)
        resp1 = jsonify({'message' : 'Post could not be returned'})
        resp1.status_code = 400
        return  resp1


        



@cross_origin()
@app.route('/logout')
def logout():
    if 'username' in session:
        session.pop('username', None)
    return jsonify({'message' : 'You successfully logged out'})
          
if __name__ == "__main__":
    app.run()