money_map README
==================
OS
--

- sudo apt install gettext

Getting Started
---------------

- cd <directory containing this file>

- $VENV/bin/pip install -e .

- $VENV/bin/pserve development.ini


DB
--

- initialize_money_map_db development.ini


Translations
------------

- pot-create -o money_map/locale/money_map.pot money_map

- msginit -l et -i money_map/locale/money_map.pot -o money_map/locale/et/LC_MESSAGES/money_map.po

- msgmerge --update money_map/locale/et/LC_MESSAGES/money_map.po money_map/locale/money_map.pot

- msgfmt -o money_map/locale/et/LC_MESSAGES/money_map.mo money_map/locale/et/LC_MESSAGES/money_map.po