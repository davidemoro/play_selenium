import os
import pytest
import mock


pytest_plugins = 'pytester'


@pytest.fixture
def data_base_path():
    """ selenium/splinter base path, where json files live """
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, 'data')


@pytest.fixture(scope='session')
def variables(skin):
    return {
        'pytest-play': {'date_format': 'YYYYMMDD'},
        'skins': {
            skin: {
                'base_url': 'http://',
                'credentials': {
                    'Administrator': {
                        'username': 'admin',
                        'password': 'pwd'
                    }
                }
            }
        }
    }


@pytest.fixture
def browser():
    from zope.interface import alsoProvides
    from pypom.splinter_driver import ISplinter
    driver = mock.MagicMock()
    alsoProvides(driver, ISplinter)
    return driver


@pytest.fixture
def page_instance(browser):
    return mock.MagicMock()


@pytest.fixture
def dummy_executor(page_instance, request, navigation):
    from pytest_play.engine import PlayEngine
    engine = PlayEngine(request, {'foo': 'bar'})
    # initialize browser
    engine._navigation = navigation
    engine._navigation.setPage(page_instance)
    engine._navigation.get_page_instance = lambda *args, **kwargs: page_instance
    return engine
