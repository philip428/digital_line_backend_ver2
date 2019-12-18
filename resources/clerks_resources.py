from app import jwt, app, db, ma
from flask import request, jsonify
from models import ClerkModel
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


@app.route('/clerks/register-and-login', methods=['POST'])
def clerks_register_and_login():

    # Dealing with arguments
    if not request.is_json:
        return {"msg": "Missing JSON in request"}, 415

    username = request.json.get("username", None)
    password = request.json.get("password", None)

    if not username:
        return {"msg": "Missing username parameter"}, 422
    if not password:
        return {"msg": "Missing password parameter"}, 422

    # Registering a user if they don't exist
    # Returning token

    if not ClerkModel.check_if_user_exists(username=username):
        ClerkModel.register_new_user(username=username, password=password)  # TODO

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
    print(username, password)

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
