import pytest
import mock
from datetime import (
    datetime,
    timedelta,
)


def test_execute_condition_true(dummy_executor):
    command = {'type': 'get',
               'provider': 'selenium',
               'url': 'http://1',
               'condition': '"$foo" === "bar"'}
    dummy_executor._navigation.page.driver.evaluate_script.return_value = True
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .driver \
        .evaluate_script \
        .assert_called_once_with('"bar" === "bar"') is None
    dummy_executor \
        ._navigation \
        .page \
        .driver_adapter \
        .open \
        .assert_called_once_with(command['url']) is None


def test_execute_condition_false(dummy_executor):
    command = {'type': 'get',
               'provider': 'selenium',
               'url': 'http://1',
               'condition': '"$foo" === "bar1"'}
    dummy_executor._navigation.page.driver.evaluate_script.return_value = False
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .driver \
        .evaluate_script \
        .assert_called_once_with('"bar" === "bar1"') is None
    dummy_executor \
        ._navigation \
        .page \
        .driver_adapter \
        .open \
        .called is False


def test_execute_get(dummy_executor):
    command = {'type': 'get', 'url': 'http://1', 'provider': 'selenium'}
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .driver_adapter \
        .open \
        .assert_called_once_with(command['url']) is None


def test_execute_get_page_none(dummy_executor, page_instance):
    command = {'type': 'get', 'url': 'http://1', 'provider': 'selenium'}
    dummy_executor._navigation.page = None
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .driver_adapter \
        .open \
        .assert_called_once_with(command['url']) is None


def test_execute_get_basestring(dummy_executor):
    import yaml
    command = yaml.load("""
---
type: get
provider: selenium
url: http://1
    """)
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .driver_adapter \
        .open \
        .assert_called_once_with('http://1') is None


def test_execute_get_basestring_param(dummy_executor):
    import yaml
    command = yaml.load("""
---
type: get
provider: selenium
url: http://$foo
""")
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .driver_adapter \
        .open \
        .assert_called_once_with('http://bar') is None


def test_execute_click(dummy_executor):
    command = {
        'type': 'clickElement',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        }
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .return_value \
        .click \
        .assert_called_once_with() is None
    assert dummy_executor._navigation.page.wait.until.called is True


def test_execute_fill(dummy_executor):
    command = {
        'type': 'setElementText',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'text': 'text value',
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .return_value \
        .fill \
        .assert_called_once_with('text value') is None


def test_execute_select_text(dummy_executor):
    command = {
        'type': 'select',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'text': 'text value',
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .return_value \
        ._element \
        .find_element_by_xpath \
        .assert_called_once_with(
            './option[text()="{0}"]'.format('text value')) is None
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .return_value \
        ._element \
        .find_element_by_xpath \
        .return_value \
        .click \
        .assert_called_once_with() is None


def test_execute_select_value(dummy_executor):
    command = {
        'type': 'select',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'value': '1',
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .return_value \
        ._element \
        .find_element_by_xpath \
        .assert_called_once_with(
            './option[@value="{0}"]'.format('1')) is None
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .return_value \
        ._element \
        .find_element_by_xpath \
        .return_value \
        .click \
        .assert_called_once_with() is None


def test_execute_select_bad(dummy_executor):
    command = {
        'type': 'select',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'value': '1',
        'text': 'text',
    }
    with pytest.raises(ValueError):
        dummy_executor.execute_command(command)


def test_execute_assert_element_present_default(dummy_executor):
    command = {
        'type': 'assertElementPresent',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_present_negated(dummy_executor):
    command = {
        'type': 'assertElementPresent',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'negated': False,
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_present_negated_false(dummy_executor):
    command = {
        'type': 'assertElementPresent',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'negated': False,
    }
    dummy_executor._navigation.page.find_element.return_value = None
    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)

    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_present_negated_true(dummy_executor):
    command = {
        'type': 'assertElementPresent',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'negated': True,
    }
    dummy_executor._navigation.page.find_element.return_value = 1
    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)

    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_visible_default(dummy_executor):
    command = {
        'type': 'assertElementVisible',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
    }
    dummy_executor._navigation.page.find_element.return_value.visible = True
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_visible_negated(dummy_executor):
    command = {
        'type': 'assertElementVisible',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'negated': False,
    }
    dummy_executor._navigation.page.find_element.return_value.visible = True
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_visible_negated_false(dummy_executor):
    command = {
        'type': 'assertElementVisible',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'negated': False,
    }
    dummy_executor._navigation.page.find_element.return_value.visible = False
    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)

    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_assert_element_visible_negated_true(dummy_executor):
    command = {
        'type': 'assertElementVisible',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'negated': True,
    }
    dummy_executor._navigation.page.find_element.return_value.visible = True
    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)

    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_send_keys(dummy_executor):
    from selenium.webdriver.common.keys import Keys
    command = {
        'type': 'sendKeysToElement',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'text': 'ENTER',
    }
    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .return_value \
        ._element \
        .send_keys \
        .assert_called_once_with(getattr(Keys, 'ENTER'))


def test_execute_send_keys_bad(dummy_executor):
    command = {
        'type': 'sendKeysToElement',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
        'text': 'ENTERxxx',
    }
    with pytest.raises(ValueError):
        dummy_executor.execute_command(command)


def test_execute_pause(dummy_executor):
    command = {
        'type': 'pause',
        'provider': 'selenium',
        'waitTime': '1500',
    }
    now = datetime.now()
    dummy_executor.execute_command(command)
    now_now = datetime.now()
    future_date = now + timedelta(milliseconds=1500)
    assert now_now >= future_date


def test_execute_pause_int(dummy_executor):
    command = {
        'type': 'pause',
        'provider': 'selenium',
        'waitTime': 1500,
    }
    now = datetime.now()
    dummy_executor.execute_command(command)
    now_now = datetime.now()
    future_date = now + timedelta(milliseconds=1500)
    assert now_now >= future_date


def test_execute_pause_bad(dummy_executor):
    command = {
        'type': 'pause',
        'provider': 'selenium',
        'waitTime': 'adsf',
    }
    with pytest.raises(ValueError):
        dummy_executor.execute_command(command)


def test_execute_store_eval(dummy_executor):
    command = {
        'type': 'storeEval',
        'provider': 'selenium',
        'variable': 'TAG_NAME',
        'script': 'document.body.tagName',
    }
    assert 'TAG_NAME' not in dummy_executor.variables
    dummy_executor \
        ._navigation \
        .page \
        .driver \
        .evaluate_script \
        .return_value = 'BODY'

    dummy_executor.execute_command(command)
    assert dummy_executor.variables['TAG_NAME'] == 'BODY'


def test_execute_store_eval_param(dummy_executor):
    command = {
        'type': 'storeEval',
        'provider': 'selenium',
        'variable': 'DYNAMIC',
        'script': '"$foo" + "$foo"',
    }
    assert 'DYNAMIC' not in dummy_executor.variables
    assert 'foo' in dummy_executor.variables
    assert dummy_executor.variables['foo'] == 'bar'

    dummy_executor.execute_command(command)

    dummy_executor \
        ._navigation \
        .page \
        .driver \
        .evaluate_script \
        .assert_called_once_with('"bar" + "bar"')


def test_execute_eval(dummy_executor):
    command = {
        'type': 'eval',
        'provider': 'selenium',
        'script': '"$foo" + "$foo"',
    }
    assert dummy_executor.variables['foo'] == 'bar'

    dummy_executor.execute_command(command)

    dummy_executor \
        ._navigation \
        .page \
        .driver \
        .evaluate_script \
        .assert_called_once_with('"bar" + "bar"')


def test_execute_verify_eval(dummy_executor):
    command = {
        'type': 'verifyEval',
        'provider': 'selenium',
        'value': 'result',
        'script': '"res" + "ult"',
    }
    dummy_executor \
        ._navigation \
        .page \
        .driver \
        .evaluate_script \
        .return_value = 'result'

    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .driver \
        .evaluate_script \
        .assert_called_once_with('"res" + "ult"')


def test_execute_verify_eval_false(dummy_executor):
    command = {
        'type': 'verifyEval',
        'provider': 'selenium',
        'value': 'result',
        'script': '"res" + "ult"',
    }
    dummy_executor \
        ._navigation \
        .page \
        .driver \
        .evaluate_script \
        .return_value = 'resultXXX'

    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)


def test_execute_verify_eval_param(dummy_executor):
    command = {
        'type': 'verifyEval',
        'provider': 'selenium',
        'value': 'resultbar',
        'script': '"res" + "ult" + "$foo"',
    }
    dummy_executor \
        ._navigation \
        .page \
        .driver \
        .evaluate_script \
        .return_value = 'resultbar'

    dummy_executor.execute_command(command)
    dummy_executor \
        ._navigation \
        .page \
        .driver \
        .evaluate_script \
        .assert_called_once_with('"res" + "ult" + "bar"')


def test_execute_wait_until_condition(dummy_executor):
    command = {
        'type': 'waitUntilCondition',
        'provider': 'selenium',
        'script': "document.body.getAttribute('id')",
    }

    dummy_executor.execute_command(command)

    dummy_executor \
        ._navigation \
        .page \
        .wait \
        .until \
        .called


def test_execute_wait_for_element_present(dummy_executor):
    command = {
        'type': 'waitForElementPresent',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
    }

    def _until(func):
        func(dummy_executor._navigation.page.driver)

    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .return_value \
        .visible = True
    dummy_executor \
        ._navigation \
        .page \
        .wait \
        .until \
        .side_effect = _until

    dummy_executor.execute_command(command)

    dummy_executor \
        ._navigation \
        .page \
        .wait \
        .until \
        .called
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_wait_for_element_visible(dummy_executor):
    command = {
        'type': 'waitForElementVisible',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': 'body'
        },
    }

    def _until(func):
        func(dummy_executor._navigation.page.driver)

    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .return_value \
        .visible = True
    dummy_executor \
        ._navigation \
        .page \
        .wait \
        .until \
        .side_effect = _until

    dummy_executor.execute_command(command)

    dummy_executor \
        ._navigation \
        .page \
        .wait \
        .until \
        .called
    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .assert_called_once_with('css', 'body') is None


def test_execute_verify_text_default(dummy_executor):
    command = {
        'type': 'verifyText',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': '.my-item'
        },
        'text': 'a text',
    }

    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .return_value \
        .text = 'hi, this is a text!'

    dummy_executor.execute_command(command)


def test_execute_verify_text(dummy_executor):
    command = {
        'type': 'verifyText',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': '.my-item'
        },
        'text': 'a text',
        'negated': False
    }

    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .return_value \
        .text = 'hi, this is a text!'

    dummy_executor.execute_command(command)


def test_execute_verify_text_negated(dummy_executor):
    command = {
        'type': 'verifyText',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': '.my-item'
        },
        'text': 'a text',
        'negated': True
    }

    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .return_value \
        .text = 'hi, this is a text!'

    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)


def test_execute_verify_text_false(dummy_executor):
    command = {
        'type': 'verifyText',
        'provider': 'selenium',
        'locator': {
             'type': 'css',
             'value': '.my-item'
        },
        'text': 'a text',
    }

    dummy_executor \
        ._navigation \
        .page \
        .find_element \
        .return_value \
        .text = 'hi, this is another text!'

    with pytest.raises(AssertionError):
        dummy_executor.execute_command(command)


def test_splinter_execute_includes(dummy_executor, data_base_path):
    execute_command_mock = mock.MagicMock()
    dummy_executor.execute_command = execute_command_mock

    yml_data = [
        {'type': 'include', 'provider': 'include',
         'path': '{0}/{1}'.format(
             data_base_path, 'login.yml')},
        {'type': 'get', 'url': 'http://2', 'provider': 'selenium'}
    ]
    dummy_executor.execute(yml_data)

    calls = [
        mock.call(yml_data[0]),
        mock.call(yml_data[1]),
    ]
    assert dummy_executor.execute_command.assert_has_calls(
        calls, any_order=False) is None
