import pytest
from app import create_app


@pytest.fixture(autouse=True)
def app():
    global app
    config_name = app.config.from_object(
        'config.TestingConfig')  # config_name = "development"
    app = create_app(config_name)
    return app
