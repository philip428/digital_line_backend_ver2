from app import db
from datetime import datetime


class LineModel(db.Model):
    __tablename__ = "lines"

    #id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), primary_key=True, unique=True, nullable=False)
    created_at = db.Column(db.DateTime(), nullable=False)

    clerks = db.relationship('ClerkModel', secondary="clerks_lines_link")
    clients = db.relationship('ClientModel', secondary="clients_lines_link")

    place_for_next_client = db.Column(db.Integer(), nullable=False)
    people_in_line = db.Column(db.Integer(), nullable=False)

    next_to_call = db.Column(db.Integer())

    def __init__(self, name):
        self.name = name
        self.created_at = datetime.utcnow()
        self.place_for_next_client = 1
        self.people_in_line = 0
        self.next_to_call = 1

    def assign_clerk(self, clerk):
        self.clerks.append(clerk)
        db.session.add(self)
        db.session.commit()

    def add_client(self, client):
        from models import ClientLineLinkModel
        self.clients.append(client)
        ClientLineLinkModel.assign_place(self, client, self.place_for_next_client)
        self.people_in_line += 1
        self.place_for_next_client += 1
        db.session.commit()

    def check_clerk_authority(self, clerk):
        """ Cheks if clerk is authorized to make changes to line """
        return clerk in self.clerks

    def call_next(self):
        from models import ClientLineLinkModel
        next_client = ClientLineLinkModel.get_client_by_place_in_line(self, self.next_to_call)
        self.people_in_line -= 1
        self.next_to_call += 1
        db.session.commit()
        return next_client


    @classmethod
    def check_if_line_exists(cls, name: str) -> bool:
        line = cls.query.filter_by(name=name).first()
        return True if line else False

    @classmethod
    def get_by_name(cls, name: str) -> "LineModel":
        return cls.query.filter_by(name=name).first()

    @classmethod
    def create_line(cls, name: str) -> "LineModel":
        line = cls(name=name)
        db.session.add(line)
        db.session.commit()
        return line