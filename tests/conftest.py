import pytest
from BionicEye import init_app


@pytest.fixture(scope='module')
def test_client():
    app = init_app(testing=True)
    testing_client = app.test_client()
    ctx = app.app_context()

    ctx.push()

    yield testing_client

    ctx.pop()
