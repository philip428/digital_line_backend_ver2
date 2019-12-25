from app import db
from datetime import datetime
from models import ClerkModel, LineModel


class ClerkLineLinkModel(db.Model):
    __tablename__ = "clerks_lines_link"

    id = db.Column(db.Integer, primary_key=True)
    clerk_username = db.Column(db.String(), db.ForeignKey('clerks.username'))
    line_name = db.Column(db.String(), db.ForeignKey('lines.name'))
