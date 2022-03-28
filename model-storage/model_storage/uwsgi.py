from model_storage import create_app, init_database, get_config

app = create_app(get_config())
init_database(app)
