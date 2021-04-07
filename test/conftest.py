import pytest
from BionicEye.src import init_app
from BionicEye.src.singelton_classes.os_manager import OSManager
from BionicEye.src.singelton_classes.db_manager import DBManager


@pytest.fixture(scope='module')
def test_client():
    app = init_app(testing=True)
    testing_client = app.test_client()
    ctx = app.app_context()

    OSManager(testing=True)
    DBManager()

    ctx.push()

    yield testing_client

    ctx.pop()
