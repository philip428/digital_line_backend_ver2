from app import jwt, app, db, ma
from flask import request, jsonify
from models import ClerkModel, LineModel
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


@app.route('/clerks/register-and-login', methods=['POST'])
def clerks_register_and_login():

    # Dealing with arguments
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, 415

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username:
        return {"msg": "Missing username body parameter"}, 422
    if not password:
        return {"msg": "Missing password body parameter"}, 422

    # Registering a user if they don't exist
    # Returning token

    if not ClerkModel.check_if_user_exists(username=username):
        ClerkModel.register_new_user(username=username, password=password)

        jwt_indentity = {
            "role": "clerk",
            "username": username
        }
        access_token = create_access_token(identity=jwt_indentity)
        return {"msg": "Successfully logged in as clerk '{}'".format(username),
                "token": access_token
                }, 200

    # Check password
    # Error on wrong password
    # Token on success

    if ClerkModel.check_password(username=username, password=password):
        jwt_indentity = {
            "role": "clerk",
            "username": username
        }
        access_token = create_access_token(identity=jwt_indentity)
        return {"msg": "Successfully logged in as clerk '{}'".format(username),
                "token": access_token
                }, 200
    else:
        return {"msg": "Wrong credentials"}, 400


@app.route('/clerks/create-line', methods=['POST'])
@jwt_required
def clerks_create_line():
    # Check user authorization
    current_user = get_jwt_identity()
    if current_user.get('role') != "clerk":
        return {"msg": "Lines can only be created by clerks. Your role is {}".format(current_user.get('role'))}, 403

    # Dealing with arguments
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, 415

    line_name = request.json.get("line_name", None)

    if not line_name:
        return {"msg": "Missing 'line_name' body parameter"}, 422

    if LineModel.check_if_line_exists(name=line_name):
        return {"msg": "Line with name '{}' already exists".format(line_name)}, 409

    new_line = LineModel.create_line(name=line_name)
    clerk = ClerkModel.get_by_username(username=current_user.get('username'))
    new_line.assign_clerk(clerk)
    return {"msg": "Successfully created line '{}' and assigned it to clerk '{}'".format(new_line.name, clerk.username)}, 200

@app.route('/clerks/call-next', methods=['POST'])
@jwt_required
def clerks_call_next():
    # Check user authorization
    current_user = get_jwt_identity()
    if current_user.get('role') != "clerk":
        return {"msg": "Only clerks can call next. Your role is {}".format(current_user.get('role'))}, 403

    # Dealing with arguments
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, 415

    line_name = request.json.get("line_name", None)

    if not line_name:
        return {"msg": "Missing 'line_name' body parameter"}, 422

    clerk = ClerkModel.get_by_username(username=current_user.get('username'))
    line = LineModel.get_by_name(line_name)
    if not line:
        return {"msg": "Line with name '{}' does not exist".format(line_name)}, 404 #todo error code
    
    if not line.check_clerk_authority(clerk):
        return {"msg": "Clerk '{}' is not authorized to perform actions on line '{}'".format(clerk.username, line.name)}, 403

    if line.people_in_line == 0:
        return {"msg": "Line '{}' is empty".format(line.name)}, 409

    next_client = line.call_next()
    print("Client '{}' it's your turn!".format(next_client.username))


    return {"msg": "Client '{}' was called".format(next_client.username)}, 200


@app.route('/clerks/protected', methods=['GET'])
@jwt_required
def clerks_protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/clerks', methods=['GET'])
def get_all_clerks():
    users = ClerkModel.query.all()

    class ClerkSchema(ma.ModelSchema):
        class Meta:
            model = ClerkModel
    clerk_schema = ClerkSchema(many=True)
    serialized_users = clerk_schema.dump(users)

    return jsonify(serialized_users)


@app.route('/clerks', methods=['DELETE'])
def delete_all_clerks():
    num_rows = ClerkModel.query.delete()
    db.session.commit()

    return {"msg": "Deleted {} rows".format(num_rows)}, 200
