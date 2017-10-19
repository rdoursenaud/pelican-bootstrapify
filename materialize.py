# coding=utf8
#
# Copyright 2017 Raphaël Doursenaud

"""
Materialize
===========

This pelican plugin adds css classes to nonstatic html output.

This is especially useful if you want to use material design lite and want
to add its default classes to your tables and images.
"""

from bs4 import BeautifulSoup
from pelican import signals, contents

MATERIALIZE_DEFAULT = {
    'table': ['mdl-data-table', 'mdl-js-data-table', 'mdl-shadow--2dp'],
    'th': ['mdl-data-table__cell--non-numeric'],
    'td': ['mdl-data-table__cell--non-numeric'],
    # TODO: detect numeric content?

    # FIXME: Does not play well with ordered list.
    # 'ul': ['mdl-list'],
    # 'li': ['mdl-list__item']

    # TODO: add a '<span class="mdl-list__item-primary-content"></span>' around the li content
}
MATERIALIZE_KEY = 'MATERIALIZE'


def init_default_config(pelican):
    from pelican.settings import DEFAULT_CONFIG

    def update_settings(settings):
        temp = MATERIALIZE_DEFAULT.copy()
        if MATERIALIZE_KEY in settings:
            temp.update(settings[MATERIALIZE_KEY])
        settings[MATERIALIZE_KEY] = temp
        return settings

    DEFAULT_CONFIG = update_settings(DEFAULT_CONFIG)
    if pelican:
        pelican.settings = update_settings(pelican.settings)


def replace_in_with(searchterm, soup, attributes):
    for item in soup.select(searchterm):
        attribute_set = set(item.attrs.get('class', []) + attributes)
        item.attrs['class'] = list(attribute_set)


def materialize(instance):
    if isinstance(instance, contents.Static):
        return

    replacements = instance.settings[MATERIALIZE_KEY]
    soup = BeautifulSoup(instance._content, 'html.parser')

    for selector, classes in replacements.items():
        replace_in_with(selector, soup, classes)

    instance._content = soup.decode()


def register():
    signals.initialized.connect(init_default_config)
    signals.content_object_init.connect(materialize)
