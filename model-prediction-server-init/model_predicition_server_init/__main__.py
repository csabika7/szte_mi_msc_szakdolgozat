from model_predicition_server_init.model_storage import ModelStorageClient
import os


client = ModelStorageClient(os.environ.get("MODEL_FILE_URL"),
                            os.environ.get("MODEL_DATA_VOLUME"),
                            os.environ.get("MODEL_FILE_NAME"))
client.download_model()
