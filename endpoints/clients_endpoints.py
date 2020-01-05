from app import jwt, app, db, ma
from flask import request, jsonify
from models import ClientModel, LineModel
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


@app.route('/clients/authorize', methods=['POST'])
def clients_authorize():

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

    if not ClientModel.check_if_user_exists(username=username):
        ClientModel.register_new_user(username=username, password=password)

        jwt_indentity = {
            "role": "client",
            "username": username
        }
        access_token = create_access_token(identity=jwt_indentity)
        return {"msg": "Successfully logged in as client '{}'".format(username),
                "token": access_token
                }, 200

    # Check password
    # Error on wrong password
    # Token on success

    if ClientModel.check_password(username=username, password=password):
        jwt_indentity = {
            "role": "client",
            "username": username
        }
        access_token = create_access_token(identity=jwt_indentity)
        return {"msg": "Successfully logged in as client '{}'".format(username),
                "token": access_token
                }, 200
    else:
        return {"msg": "Wrong credentials"}, 400


@app.route('/clients/get-in-line', methods=['POST'])
@jwt_required
def clients_get_in_line():
    # Check user authorization
    current_user = get_jwt_identity()
    if current_user.get('role') != "client":
        return {"msg": "Only clients can get in line. Your role is {}".format(current_user.get('role'))}, 403

    # Dealing with arguments
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, 415

    line_name = request.json.get("line_name", None)

    if not line_name:
        return {"msg": "Missing 'line_name' body parameter"}, 422

    client = ClientModel.get_by_username(username=current_user.get('username'))
    line = LineModel.get_by_name(name=line_name)

    if not line:
        return {"msg": "Line '{}' was not found".format(line_name)}, 400

    if client in line.clients:
        return {"msg": "Client '{}' is already in line '{}'".format(client.username, line.name)}, 409

    line.add_client(client)

    return {"msg": "Successfully put client '{}' in line '{}'".format(client.username, line.name)}, 200


@app.route('/clients/my-lines', methods=['GET'])
@jwt_required
def clients_my_lines():
    # Check user authorization
    current_user = get_jwt_identity()
    if current_user.get('role') != "client":
        return {"msg": "This endpoint is for clients. Your role is {}".format(current_user.get('role'))}, 403

    client = ClientModel.get_by_username(username=current_user.get('username'))
    lines = client.my_lines()

    class LineSchema(ma.ModelSchema):
        class Meta:
            model = LineModel

    line_schema = LineSchema(many=True)

    return jsonify(line_schema.dump(lines)), 200


@app.route('/clients/protected', methods=['GET'])
@jwt_required
def clients_protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


@app.route('/clients', methods=['GET'])
def get_all_clients():
    users = ClientModel.query.all()

    class ClienTschema(ma.ModelSchema):
        class Meta:
            model = ClientModel
    client_schema = ClienTschema(many=True)
    serialized_users = client_schema.dump(users)

    return jsonify(serialized_users)


@app.route('/clients', methods=['DELETE'])
def delete_all_clients():
    num_rows = ClientModel.query.delete()
    db.session.commit()

    return {"msg": "Deleted {} rows".format(num_rows)}, 200
