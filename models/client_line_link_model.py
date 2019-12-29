from app import db
from datetime import datetime
from models import ClientModel, LineModel


class ClientLineLinkModel(db.Model):
    __tablename__ = "clients_lines_link"

    #id = db.Column(db.Integer, primary_key=True)
    line_name = db.Column(db.String(), db.ForeignKey('lines.name'), primary_key=True)
    client_username = db.Column(db.String(), db.ForeignKey('clients.username'), primary_key=True)
    place_in_line = db.Column(db.Integer())

    @classmethod
    def assign_place(cls, line, client, place):
        """ Assigns place to client in specific line """
        link = cls.query.filter_by(line_name=line.name, client_username=client.username).first()
        link.place_in_line = place
        db.session.commit()

    @classmethod
    def get_client_by_place_in_line(cls, line, place):
        link = cls.query.filter_by(line_name=line.name, place_in_line=place).first()
        return ClientModel.query.filter_by(username=link.client_username).first()
