import pytest
from BionicEye import init_app
from BionicEye.singelton_classes.os_manager import OSManager


@pytest.fixture(scope='module')
def test_client():
    app = init_app(testing=True)
    testing_client = app.test_client()
    ctx = app.app_context()
    OSManager(testing=True)

    ctx.push()

    yield testing_client

    ctx.pop()
