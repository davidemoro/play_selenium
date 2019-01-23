=============
play_selenium
=============


.. image:: https://travis-ci.org/davidemoro/play_selenium.svg?branch=master
    :target: https://travis-ci.org/davidemoro/play_selenium
    :alt: See Build Status on Travis CI

.. image:: https://readthedocs.org/projects/play_selenium/badge/?version=latest
    :target: http://play_selenium.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://codecov.io/gh/davidemoro/play_selenium/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/davidemoro/play_selenium

pytest-play plugin driving browsers using Selenium/Splinter under the hood.
Selenium grid compatible and implicit auto wait actions for more robust scenarios with less pain.

More info and examples on:

* pytest-play_, documentation
* cookiecutter-qa_, see ``pytest-play`` in action with a working example if you want to start hacking

Browser based commands
----------------------

Browser based commands here.
``play_selenium`` supports by default browser interactions. For example it can be used for running selenium splinter_ scenarios driving your browser for your UI test or system tests.

``play_selenium`` is also your friend when page object approach (considered best practice) is not possible. For example:

* limited time, and/or
* lack of programming skills

Instead if you are interested in a page object pattern have a look at pypom_form_ or pypom_.

``play_selenium`` supports automatic waiting that should help to keep your tests more reliable with implicit waits before
moving on. By default it waits for node availability and visibility but it supports also some wait commands and
wait until a given Javascript expression is ok. So it is at the same time user friendly and flexible.

 
Conditional commands (Javascript)
=================================

Based on a browser level expression (Javascript)::

    - type: clickElement
      provider: selenium
      locator:
        type: css
        value: body
      condition: "'$foo' === 'bar'"


Supported locators
==================

Supported selector types:

* css
* xpath
* tag
* name
* text
* id
* value

Open a page
===========

With parametrization::

    - type: get
      provider: selenium
      url: "$base_url"

or with a regular url::

    - type: get
      provider: selenium
      url: https://google.com


Pause
=====

This command invokes a javascript expression that will
pause the execution flow of your commands::

    - type: pause
      provider: selenium
      waitTime: 1500

If you need a pause/sleep for non UI tests you can use the
``sleep`` command provided by the play_python_ plugin.

Click an element
================
::

    - type: clickElement
      provider: selenium
      locator:
        type: css
        value: body

Fill in a text
==============
::

    - type: setElementText
      provider: selenium
      locator:
        type: css
        value: input.title
      text: text value

Interact with select input elements
===================================

Select by label::

    - type: select
      provider: selenium
      locator:
        type: css
        value: select.city
      text: Turin

or select by value::

    - type: select
      provider: selenium
      locator:
        type: css
        value: select.city
      value: '1'

Eval a Javascript expression
============================

::

    - type: eval
      provider: selenium
      script: alert('Hello world!')

Create a variable starting from a Javascript expression
=======================================================

The value of the Javascript expression will be stored in
``play.variables`` under the name ``count``::

    - type: storeEval
      provider: selenium
      variable: count
      script: document.getElementById('count')[0].textContent

Assert if a Javascript expression matches
=========================================

If the result of the expression does not match an ``AssertionError``
will be raised and the test will fail::

    - type: verifyEval
      provider: selenium
      value: '3'
      script: document.getElementById('count')[0].textContent

Verify that the text of one element contains a string
=====================================================

If the element text does not contain the provided text an
``AssertionError`` will be raised and the test will fail::

    - type: verifyText
      provider: selenium
      locator:
        type: css
        value: ".my-item"
      text: a text

Send keys to an element
=======================

All ``selenium.webdriver.common.keys.Keys`` are supported::

    - type: sendKeysToElement
      provider: selenium
      locator:
        type: css
        value: ".confirm"
      text: ENTER


Supported keys::

    KEYS = [
        'ADD', 'ALT', 'ARROW_DOWN', 'ARROW_LEFT', 'ARROW_RIGHT',
        'ARROW_UP', 'BACKSPACE', 'BACK_SPACE', 'CANCEL', 'CLEAR',
        'COMMAND', 'CONTROL', 'DECIMAL', 'DELETE', 'DIVIDE',
        'DOWN', 'END', 'ENTER', 'EQUALS', 'ESCAPE', 'F1', 'F10',
        'F11', 'F12', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8',
        'F9', 'HELP', 'HOME', 'INSERT', 'LEFT', 'LEFT_ALT',
        'LEFT_CONTROL', 'LEFT_SHIFT', 'META', 'MULTIPLY',
        'NULL', 'NUMPAD0', 'NUMPAD1', 'NUMPAD2', 'NUMPAD3',
        'NUMPAD4', 'NUMPAD5', 'NUMPAD6', 'NUMPAD7', 'NUMPAD8',
        'NUMPAD9', 'PAGE_DOWN', 'PAGE_UP', 'PAUSE', 'RETURN',
        'RIGHT', 'SEMICOLON', 'SEPARATOR', 'SHIFT', 'SPACE',
        'SUBTRACT', 'TAB', 'UP',
    ]

Wait until a Javascript expression matches
==========================================

Wait until the given expression matches or raise a 
``selenium.common.exceptions.TimeoutException`` if takes too time.

At this time of writing there is a global timeout (20s) but in future releases
you will be able to override it on command basis::

    - type: waitUntilCondition
      provider: selenium
      script: document.body.getAttribute('class') === 'ready'

Wait for element present in DOM
===============================

Present::

    - type: waitForElementPresent
      provider: selenium
      locator:
        type: css
        value: body

or not present::

    - type: waitForElementPresent
      provider: selenium
      locator:
        type: css
        value: body
      negated: true

Wait for element visible
========================

Visible::

    - type: waitForElementVisible
      provider: selenium
      locator:
        type: css
        value: body

or not visible::

    - type: waitForElementVisible
      provider: selenium
      locator:
        type: css
        value: body
      negated: true

Assert element is present in DOM
================================

An ``AssertionError`` will be raised if assertion fails.

Present::

    - type: assertElementPresent
      provider: selenium
      locator:
        type: css
        value: div.elem

or not present::

    - type: assertElementPresent
      provider: selenium
      locator:
        type: css
        value: div.elem
      negated: true

Assert element is visible
=========================

An ``AssertionError`` will be raised if assertion fails.

Present::

    - type: assertElementVisible
      provider: selenium
      locator:
        type: css
        value: div.elem

or not present::

    - type: assertElementVisible
      provider: selenium
      locator:
        type: css
        value: div.elem
      negated: true


Twitter
-------

``play_selenium`` tweets happens here:

* `@davidemoro`_
 

.. _`pytest-play`: https://github.com/davidemoro/pytest-play
.. _`pypom_form`: http://pypom-form.readthedocs.io/en/latest/
.. _`splinter`: https://splinter.readthedocs.io/en/latest/
.. _`pypom`: http://pypom.readthedocs.io/en/latest/
.. _`@davidemoro`: https://twitter.com/davidemoro
.. _`cookiecutter-qa`: https://github.com/davidemoro/cookiecutter-qa
.. _`play_python`: https://github.com/davidemoro/play_python
