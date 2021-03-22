from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
import jwt
import datetime
from project import app, db
from project.models import User, Content
from functools import wraps
from project.helpers import construct_content_object


def token_required(f):
    """
    Wrapper function which checks whether a user is logged in or not
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return {'message': 'Token is missing!'}, 401
        try:
            current_user = User.query.filter_by(token_key=token).first()
        except:
            return {'message': 'Token is invalid!'}, 401
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/users', methods=['GET'])
def get_all_users():
    """
    This function give us the details of all the users
    """
    users = User.query.all()
    result = []
    for user in users:
        user_data = {'public_id': user.public_id, 'email': user.email, 'full_name': user.full_name,
                     'phone_number': user.phone_number, 'admin': user.admin}
        result.append(user_data)
    return {'users': result}


@app.route('/signup', methods=['POST'])
def create_user():
    """
    This function is used to create a user
    """
    try:
        user_data = request.get_json()
        hashed_password = generate_password_hash(user_data['password'], method='sha256')
        new_user = User(public_id=str(uuid.uuid4()),
                        email=user_data['email'],
                        password=hashed_password,
                        full_name=user_data['full_name'],
                        phone_number=user_data['phone_number'],
                        address=user_data['address'],
                        city=user_data['city'],
                        state=user_data['state'],
                        country=user_data['country'],
                        admin=user_data['admin'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'New user created!'})
    except:
        return jsonify({'message': "Something went Wrong!"})


@app.route('/login')
def login():
    """
    This function is used to login as current user.
    The token is generated and saved to database.
    """
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    user = User.query.filter_by(email=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
            app.config['SECRET_KEY'], algorithm='HS256')
        user.token_key = str(token)
        db.session.commit()
        return {'token': token}
    return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})


@app.route('/logout')
@token_required
def logout(current_user):
    """
    This function is used to logout as current user.
    The token is deleted from the database.
    """
    user = User.query.filter_by(email=current_user.email).first()
    user.token_key = ''
    db.session.commit()
    return {'message': 'User logout successfully'}


@app.route('/content', methods=['GET'])
@token_required
def get_all_content(current_user):
    """
    This function is used to get all the content from a logged in user.
    It will also check if a user is admin
    """

    def get_content_object(data):
        result = []
        for content in data:
            result.append(construct_content_object(content))
        return result

    if not (current_user and current_user.admin):
        contents = Content.query.filter_by(user_id=current_user.id).all()
        get_content = get_content_object(contents)
        return {'content': get_content}

    contents = Content.query.all()
    get_content = get_content_object(contents)
    return {'contents': get_content}


@app.route('/content/<content_id>', methods=['GET'])
@token_required
def get_content_by_id(current_user, content_id):
    """
    This function will give us a content based on its id.
    It will also check if a user is logged in and admin
    """

    if not (current_user and current_user.admin):
        content = Content.query.filter_by(id=content_id, user_id=current_user.id).first()
        if not content:
            return {'message': 'No Content found!'}
        get_content = construct_content_object(content)
        return jsonify(get_content)

    content = Content.query.filter_by(id=content_id).first()
    if not content:
        return {'message': 'No Content found!'}
    get_content = construct_content_object(content)
    return jsonify(get_content)


@app.route('/content', methods=['POST'])
@token_required
def create_content(current_user):
    """
    This function is used to create a content if a user is logged in
    """
    try:
        content_data = request.get_json()
        new_content = Content(title=content_data['title'],
                              body=content_data['body'],
                              summary=content_data['summary'],
                              user_id=current_user.id)
        db.session.add(new_content)
        db.session.commit()
        return jsonify({'message': "Content created!"})
    except:
        return jsonify({'message': "Something went Wrong!"})


@app.route('/content/<content_id>', methods=['PUT'])
@token_required
def edit_content(current_user, content_id):
    """
    This function is used to edit a contents based on its id.
    It is also check for the admin status hence admin user can also edit the content
    """
    content_data = request.get_json()

    def update_data(data):
        data.title = content_data['title']
        data.body = content_data['body']
        data.summary = content_data['summary']
        db.session.commit()

    if not (current_user and current_user.admin):
        content = Content.query.filter_by(id=content_id, user_id=current_user.id).first()
        if not content:
            return {'message': 'No Content found!'}
        update_data(content)
        return {'message': 'Content item Updated!'}

    content = Content.query.filter_by(id=content_id).first()
    if not content:
        return {'message': 'No Content found!'}
    update_data(content)
    return {'message': 'Content item Updated!'}


@app.route('/content/<content_id>', methods=['DELETE'])
@token_required
def delete_content(current_user, content_id):
    """
    This function is used to delete a contents based on its id.
    It is also check for the admin status hence admin user can also delete the content
    """
    if not (current_user and current_user.admin):
        content = Content.query.filter_by(id=content_id, user_id=current_user.id).first()
        if not content:
            return {'message': 'No Content found!'}
        db.session.delete(content)
        db.session.commit()
        return {'message': 'Content item deleted!'}

    content = Content.query.filter_by(id=content_id).first()
    if not content:
        return {'message': 'No Content found!'}
    db.session.delete(content)
    db.session.commit()
    return {'message': 'Content item deleted!'}


@app.route('/content/search', methods=['GET'])
def search_content():
    """
    This function is used to search content by matching terms in title, body, summary and return the content
    """
    requested_search_data = request.get_json()
    contents = Content.query.all()

    output = []
    for content in contents:
        if requested_search_data['search'].lower() in content.title.lower():
            output.append(construct_content_object(content))
        elif requested_search_data['search'].lower() in content.body.lower():
            output.append(construct_content_object(content))
        elif requested_search_data['search'].lower() in content.summary.lower():
            output.append(construct_content_object(content))
        else:
            continue
    return {'Content': output}
