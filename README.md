Chysel
======

Authors
-------

- Final work: Alan Schneider <https://github.com/shkschneider/chysel>
- Original work: David Zhou <https://github.com/dz/chisel>
- Bootstrap: Twitter <http://twitter.github.com/bootstrap/>
- Pygments: <http://pygments.org/docs/authors/>
- Disqus <http://disqus.com>

Features
--------

- Done in pure Python
- Plain Text / HTML / Markdown syntax
- Syntax highlight
- Jinja2 templates
- Bootstrap default theme
- Nice urls (without url rewriting)
- Comments on entries by Disqus

Usage
-----

Edit `chysel.py` to configure it.

    SITE = {'url': '/', # trailing slash
            'name': 'Chysel'}
    INPUT = './content/' # trailing slash
    OUTPUT = './www/' # trailing slash
    TEMPLATE_PATH = './template/'
    TEMPLATE_OPTIONS = {}
    TIME_FORMAT = '%B %d, %Y'
    ENTRY_TIME_FORMAT = '%Y/%m/%d'
    DISQUS_ID = '' # empty if always disabled

Then generate the website:

    $ python chysel.py
    Chyseling
    * Reading entries...
      - example
    * Generating site...
      ./template/index.html -> ../www/index.html
      ./template/archives.html -> ../www/archives/index.html
      ./template/js -> ../www/js/
      ./template/img -> ../www/img/
      ./template/css -> ../www/css/
    * Generating entries...
      ./content/example -> ../www/example/index.html
      ./content/category/example -> ../www/example/category/index.html
    * Generating categories...
      ./content/category -> ../www/category/example/index.html
    Browse at: </>
    $

Website is now fully static, in `./www/`.

    $ ls -l ./www/
    d--------- about/
    d--------- archives/
    d--------- category/
    d--------- css/
    d--------- example/
    d--------- img/
    d--------- index.html
    d--------- js/

Format
------

Entries are created as flat files in `./content/` and will be generated as html files in `./www/`.

Formatting is done using Markdown syntax.

    The First Line Contains The Title <<< Title
    2012/24/12                        <<< Date YYYY/DD/MM
    Opened                            <<< Comments 'Yes' or 'No', 'Open[ed]' or 'Close[d]'
    1                                 <<< Revision number, '0' to hide

    Hello world!

    ...

Read more about Markdown: <http://daringfireball.net/projects/markdown/>
