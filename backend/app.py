from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from os import environ

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
app.config["JWT_SECRET_KEY"] = "mysecret" 
jwt = JWTManager(app)
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  #auth_id = db.Column(db.Integer, db.ForeignKey('auth.id'), unique=False, nullable=False)
  #auth = db.relationship("AuthModel", back_populates="users")

  def json(self):
    return {'id': self.id,'name': self.name, 'email': self.email}

class Auth(db.Model):
  __tablename__ = 'auth'
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password1 = db.Column(db.String(120), unique=True, nullable=False)
  password2 = db.Column(db.String(120), unique=True, nullable=False)
  #users = db.relationship('UserModel', back_populates='auth', lazy='dynamic')

  def json(self):
    return {'id': self.id,'name': self.name, 'email': self.email}
  
db.create_all()

# create a test route
@app.route('/test', methods=['GET'])
def test():
  return jsonify({'message': 'The server is running'})


# create a user
@app.route('/auth/create', methods=['POST'])
def create_auth():
  try:
    data = request.get_json()
    if data['password1'] == data['password2']:
      new_auth = Auth(name=data['name'], email=data['email'], password1=data['password1'], password2=data['password2'])
      db.session.add(new_auth)
      db.session.commit()
    
      return jsonify({
          'id': new_auth.id,
          'name': new_auth.name,
          'email': new_auth.email
      }), 201
    else:
      return jsonify({'message': 'Password1 must match Password2'}), 500

  except Exception as e:
    return make_response(jsonify({'message': 'error creating user', 'error': str(e)}), 500)

# login a user
@app.route('/auth/login', methods=['POST'])
def login_auth():
  try:
    data = request.get_json()
    email = data['email']
    auth = Auth.query.filter_by(email=email).first() 
    if auth:
      password = data['password']
      if auth.password1 == password:
        access_token = create_access_token(identity=email)
        return make_response(jsonify({'auth': auth.json(), 'access_token': access_token}), 200)
      else : return make_response(jsonify({'message': 'wrong password'}), 500)
    else : return make_response(jsonify({'message': 'auth not found'}), 404) 
  except Exception as e:
    return make_response(jsonify({'message': 'error getting user', 'error': str(e)}), 500)

# get all auths
@app.route('/auth', methods=['GET'])
def get_auth():
  try:
    auths = Auth.query.all()
    auths_data = [{'id': auth.id, 'name': auth.name, 'email': auth.email} for auth in auths]
    return jsonify(auths_data), 200
  except Exception as e:
    return make_response(jsonify({'message': 'error getting users', 'error': str(e)}), 500)
  
# get an auth by id
@app.route('/auth/<id>', methods=['GET'])
def auth_detail(id):
  try:
    auth = Auth.query.filter_by(id=id).first() # get the first user with the id
    if auth:
      return make_response(jsonify({'auth': auth.json()}), 200)
    return make_response(jsonify({'message': 'auth not found'}), 404) 
  except Exception as e:
    return make_response(jsonify({'message': 'error getting user', 'error': str(e)}), 500)
  
# update an auth by id
@app.route('/auth/<id>', methods=['PUT'])
def update_auth(id):
  try:
    auth = Auth.query.filter_by(id=id).first()
    if auth:
      data = request.get_json()
      auth.name = data['name']
      auth.email = data['email']
      auth.password1 = data['password1']
      auth.password2 = data['password2']
      if data['password1'] == data['password2']:
        db.session.commit()
        return make_response(jsonify({'message': 'auth updated'}), 200)
      return make_response(jsonify({'message': 'Password1 must match Password2'}), 500)
    return make_response(jsonify({'message': 'auth not found'}), 404)  
  except Exception as e:
      return make_response(jsonify({'message': 'error updating auth', 'error': str(e)}), 500)

# delete an auth by id
@app.route('/auth/delete/<id>', methods=['DELETE'])
def delete_auth(id):
  try:
    auth = Auth.query.filter_by(id=id).first()
    if auth:
      db.session.delete(auth)
      db.session.commit()
      return make_response(jsonify({'message': 'user deleted'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404) 
  except Exception as e:
    return make_response(jsonify({'message': 'error deleting user', 'error': str(e)}), 500)  

############################################################

# create a user
@app.route('/api/flask/users', methods=['POST'])
def create_user():
  try:
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()  

    return jsonify({
        'id': new_user.id,
        'name': new_user.name,
        'email': new_user.email
    }), 201  

  except Exception as e:
    return make_response(jsonify({'message': 'error creating user', 'error': str(e)}), 500)
  
# get all users
@app.route('/api/flask/users', methods=['GET'])
@jwt_required()
def get_users():
  try:
    current_auth = get_jwt_identity()
    users = User.query.all()
    users_data = [{'id': user.id, 'name': user.name, 'email': user.email} for user in users]
    return make_response(jsonify(data=users_data, logged_in_as=current_auth), 200)
  except Exception as e:
    return make_response(jsonify({'message': 'error getting users', 'error': str(e)}), 500)
  
# get a user by id
@app.route('/api/flask/users/<id>', methods=['GET'])
def get_user(id):
  try:
    user = User.query.filter_by(id=id).first() # get the first user with the id
    if user:
      return make_response(jsonify({'user': user.json()}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404) 
  except Exception as e:
    return make_response(jsonify({'message': 'error getting user', 'error': str(e)}), 500)
  
# update a user by id
@app.route('/api/flask/users/<id>', methods=['PUT'])
def update_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.name = data['name']
      user.email = data['email']
      db.session.commit()
      return make_response(jsonify({'message': 'user updated'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)  
  except Exception as e:
      return make_response(jsonify({'message': 'error updating user', 'error': str(e)}), 500)

# delete a user by id
@app.route('/api/flask/users/<id>', methods=['DELETE'])
def delete_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonify({'message': 'user deleted'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404) 
  except Exception as e:
    return make_response(jsonify({'message': 'error deleting user', 'error': str(e)}), 500)   
