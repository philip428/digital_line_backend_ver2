import time

from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from app import jwt, app, db, ma
from models import ClerkModel, LineModel


@app.route('/clerks/authorize', methods=['POST'])
def clerks_authorize():

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
    """ body: {"line_name": "line_name"} """
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


@app.route('/clerks/my-lines', methods=['GET'])
@jwt_required
def clerks_my_lines():
    # Check user authorization
    current_user = get_jwt_identity()
    if current_user.get('role') != "clerk":
        return {"msg": "This endpoint is for clerks. Your role is {}".format(current_user.get('role'))}, 403

    clerk = ClerkModel.get_by_username(username=current_user.get('username'))
    lines = clerk.my_lines()

    class LineSchema(ma.ModelSchema):
        class Meta:
            model = LineModel

    line_schema = LineSchema(many=True)

    return jsonify(line_schema.dump(lines)), 200


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
        return {"msg": "Line with name '{}' does not exist".format(line_name)}, 404  # todo error code

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
    #time.sleep(3)
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
