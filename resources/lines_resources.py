from app import jwt, app, db, ma
from flask import request, jsonify
from models import ClerkModel, LineModel
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity


@app.route('/lines', methods=['GET'])
def get_all_lines():
    lines = LineModel.query.all()

    class LineSchema(ma.ModelSchema):
        class Meta:
            model = LineModel
    line_schema = LineSchema(many=True)
    serialized_lines = line_schema.dump(lines)

    return jsonify(serialized_lines)


@app.route('/lines', methods=['DELETE'])
def delete_all_lines():
    num_rows = ClerkModel.query.delete()
    db.session.commit()

    return {"msg": "Deleted {} rows".format(num_rows)}, 200
