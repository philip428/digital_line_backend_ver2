import time

from flask import request, jsonify
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from app import jwt, app, db, ma
from models import ClerkModel, LineModel


import logging

logger = logging.getLogger(__name__)


@app.route('/lines', methods=['GET'])
def get_all_lines():
    #time.sleep(3)
    lines = LineModel.query.all()

    class LineSchema(ma.ModelSchema):
        class Meta:
            model = LineModel
    line_schema = LineSchema(many=True)
    serialized_lines = line_schema.dump(lines)

    return jsonify(serialized_lines)


@app.route('/lines/get-by-name', methods=['GET'])
def get_by_name():
    line_name = request.args.get('line_name')

    line = LineModel.get_by_name(line_name)

    class LineSchema(ma.ModelSchema):
        class Meta:
            model = LineModel
    line_schema = LineSchema()
    serialized_line = line_schema.dump(line)

    return jsonify(serialized_line)


@app.route('/lines/get-current-client', methods=['GET'])
def get_current_client():
    from models import ClientModel

    line_name = request.args.get('line_name')

    line = LineModel.get_by_name(line_name)

    client = ClientModel.get_by_username(line.current_client_username)

    class ClientSchema(ma.ModelSchema):
        class Meta:
            model = ClientModel
    client_schema = ClientSchema()

    serialized_client = client_schema.dump(client)

    return jsonify(serialized_client)


@app.route('/lines/get-next-client', methods=['GET'])
def get_next_client():
    from models import ClientModel

    line_name = request.args.get('line_name')

    line = LineModel.get_by_name(line_name)

    client = ClientModel.get_by_username(line.next_client_username)

    class ClientSchema(ma.ModelSchema):
        class Meta:
            model = ClientModel
    client_schema = ClientSchema()

    serialized_client = client_schema.dump(client)

    return jsonify(serialized_client)


@app.route('/lines', methods=['DELETE'])
def delete_all_lines():
    num_rows = ClerkModel.query.delete()
    db.session.commit()

    return {"msg": "Deleted {} rows".format(num_rows)}, 200
