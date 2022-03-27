from flask import Flask
from model_storage.database import db
from model_storage.db_models import MLModel
from model_storage.api.v1.routes import api_v1
import os


def get_config():
    model_storage_path = os.environ["MODEL_STORAGE_PATH"]
    meta_data_db_file_name = "metadata.db"
    meta_data_db_path = str(os.path.join(model_storage_path, meta_data_db_file_name))
    conf = dict()
    conf['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(meta_data_db_path)
    return conf


def create_app(config=None):
    app = Flask(__name__)
    # setup config
    if config:
        app.config.from_mapping(config)
    # setup API
    app.register_blueprint(blueprint=api_v1, url_prefix="/v1/model-store")
    # setup DB

    db.init_app(app)

    return app


def init_database(app):
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    app = create_app(get_config())
    init_database(app)
    app.run(host="0.0.0.0")
