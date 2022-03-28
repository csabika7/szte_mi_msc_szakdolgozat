from model_storage.database import db


class MLModel(db.Model):
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    file_name = db.Column(db.String(120), unique=True, nullable=False)