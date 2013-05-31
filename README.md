Chysel
======

Authors
-------

- Final work: Alan Schneider <https://github.com/shkschneider/chysel>
- Original work: David Zhou <https://github.com/dz/chisel>
- Bootstrap: Twitter <http://twitter.github.com/bootstrap/>

Features
--------

- Done in pure Python
- Plain Text / HTML / Markdown syntax
- Jinja2 templates
- Bootstrap default theme
- Nice urls

Usage
-----

Edit `chysel.py` to configure it.

    SITE = {'url': '/', # trailing slash
            'name': 'Chysel'}
    INPUT = './content/' # trailing slash
    OUTPUT = '../www/' # trailing slash
    TEMPLATE_PATH = './template/'
    TEMPLATE_OPTIONS = {}
    TIME_FORMAT = '%B %d, %Y'
    ENTRY_TIME_FORMAT = '%Y/%m/%d'

Then generate the website:

    $ python chysel.py
    Chyseling
    * Reading files...
      - example
    * Generating HTML...
      ./template/index.html -> ../www/index.html
      ./content/example -> ../www/example/index.html
      ./template/archives.html -> ../www/archives/index.html
      ./template/about.html -> ../www/about/index.html
      ./template/js -> ../www/js
      ./template/css -> ../www/css
      ./template/img -> ../www/img
    Browse at: </>
    $

Website is now fully static, in `./www/`.

    $ ls -l ./www/
    d--------- about/
    d--------- archives/
    d--------- css/
    d--------- example/
    d--------- img/
    d--------- index.html
    d--------- js/

Format
------

Entries are created as flat files in `./content/` and will be generated as html files in `./www/`.

Formatting is done using Markdown syntax.

    The First Line Contains The Title
    2012/12/24

    Hello world!

    ...

Read more about Markdown: <http://daringfireball.net/projects/markdown/>
