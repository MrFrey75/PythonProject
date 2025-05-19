from . import db
import uuid

class Board(db.Model):
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    pages = db.relationship('Page', backref='board', lazy=True)

class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_id = db.Column(db.String, db.ForeignKey('board.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    order = db.Column(db.Integer, default=0)
