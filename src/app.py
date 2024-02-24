"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from bcrypt import gensalt
from flask_jwt_extended import create_access_token, get_jwt_identity, JWTManager, jwt_required
from flask_bcrypt import generate_password_hash, check_password_hash
#from models import Person


app = Flask(__name__)
app.url_map.strict_slashes = False

#jwt config
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  

jwt = JWTManager(app)


db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#create user
@app.route('/user', methods=['GET', "POST"])
def handle_user():

    if request.method == "POST":
        #data
        data = request.json
        email = data.get("email")
        password = data.get("password")
        name = data.get("name")
        last_name = data.get("last_name")


        #check that the email is unique
        check_email = User.query.filter_by(email=email).one_or_none()
        if check_email:
            return jsonify({
                "msg": "Email already exists"
            }), 400
        
        #check that the data is complete
        data_check = [email, password, name, last_name]
        if None in data_check:
            return jsonify({
                "msg": "Data is incomplete"
            }), 400
        
        #genetare salt
        salt = str(gensalt(), encoding = "utf-8")

        #generate hashed pasword
        hashed_password = str(generate_password_hash(password + salt) , encoding = "utf-8") 

        #create an instance of the user
        new_user = User(
            name = name,
            last_name = last_name,
            salt = salt,
            email = email,
            hashed_password = hashed_password,
        )

        try: 
            db.session.add(new_user)
            db.session.commit()
        except Exception as error:
            db.session.rollback()
            return jsonify({
                "msg": "there has been a problem with the data base"
            }), 500
        
        return jsonify({
            "msg": "User has been created successfully"
        }), 201
    
    if request.method == "GET":
        #get all users
        all_users = User.query.all()
        #arreglo para guardar los usuarios ya serializados
        user_serialized = []
        for user in all_users:
            user_serialized.append(user.serialize())
        return jsonify(user_serialized), 200


#create user token
@app.route('/user-token', methods=["POST"])
def handle_user_login():
    
    #data
    data = request.json
    email = data.get("email")
    password = data.get("password")

    #check that the data is complete
    data_check = [email, password]
    if None in data_check:
        return jsonify({
            "msg": "Data is incomplete"
        }), 400
    
    #check that the user exists
    user = User.query.filter_by(email = email).one_or_none()
    if not user:
        return jsonify({
            "msg": "User does not exists"
        }), 404

    #check that the password is valid
    password_is_valid = check_password_hash(
        user.hashed_password,
        password + user.salt
    )

    if not password_is_valid:
        return jsonify({
            "msg": "Incorrect password"
        }), 401




@app.route('/user/<int:id>', methods=['GET'])
def handle_specific_user():
    pass




























# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
