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
- Markdown syntax
- Jinja2 templates
- Bootstrap default theme
- Nice urls

Usage
-----

Edit `chysel.py` toconfigure it.

Then generate the website:

    python chysel.py

Website is now fully static and in `./www/`.

Format
------

Entries are created as flat files in `./content/` and will be generated as html files in `./www/`.

Formatting is done using Markdown syntax.

    The First Line Contains The Title
    2012/12/24

    Hello world!

    ...

Read more about Markdown: <http://daringfireball.net/projects/markdown/>
