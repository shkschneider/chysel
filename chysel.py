#!/usr/bin/env python
#
# chysel
#   Alan Schneider <https://github.com/shkschneider/chisel>
#   David Zhou <https://github.com/dz/chisel>
#

### DEPENDS: jinja2 markdown Pygments ###

try:
    from distutils import dir_util
    import markdown
    import jinja2
    import time
    import sys
    import os
    import re
except ImportError as error:
    print 'ImportError:', str(error)
    exit(1)

### SETTINGS ###

SITE = {'url': '/', # trailing slash
        'name': 'Chysel'}
INPUT = './content/' # trailing slash
OUTPUT = './www/' # trailing slash
TEMPLATE_PATH = './template/'
TEMPLATE_OPTIONS = {}
TIME_FORMAT = '%B %d, %Y'
ENTRY_TIME_FORMAT = '%Y/%m/%d'
FORMAT = lambda text: markdown.markdown(text, ['abbr',
                                               'def_list',
                                               'fenced_code',
                                               'footnotes',
                                               'tables',
                                               'codehilite(force_linenos=True)'])

### DO NOT EDIT BELOW THIS LINE ###

def parse(source):
    files = []
    for root, ds, fs in os.walk(source):
        for name in fs:
            if name[0] == '.':
                continue
            if not re.match(r'^.+\.(md|markdown)$', name):
                continue
            path = os.path.join(root, name)
            with open(path, 'rU') as f:
                title = f.readline().strip('\n\t')
                name = os.path.splitext(path.replace(INPUT, ''))[0]
                print '  -', name
                category = os.path.dirname(name)
                if len(category):
                    title = category.capitalize() + '/ ' + title
                date = time.strptime(f.readline().strip(), ENTRY_TIME_FORMAT)
                year, month, day = date[:3]
                comments = f.readline().strip() == 'Opened'
                revision = int(f.readline().strip())
                f.readline()
                content = ''.join(f.readlines()).decode('UTF-8')
                files.append({'slug': name,
                              'title': title,
                              'except': content[:100],
                              'content': FORMAT(content),
                              'url': name + '/',
                              'date': time.strftime(TIME_FORMAT, date),
                              'epoch': time.mktime(date),
                              'year': year,
                              'month': time.strftime('%B', date),
                              'day': day,
                              'comments': comments,
                              'revision': revision,
                              'filename': name})
    return files

def write_file(url, data):
    path = OUTPUT + url
    dirs = os.path.dirname(path)
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    with open(path, 'w') as f:
        f.write(data.encode('UTF-8'))

if __name__ == '__main__':
    print 'Chyseling'

    print ' * Reading entries...'

    entries = sorted(parse(INPUT), key=lambda entry: entry['epoch'], reverse=True)
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH), **TEMPLATE_OPTIONS)

    print ' * Generating site...'

    print '   %s%s -> %sindex.html' % (TEMPLATE_PATH, 'index.html', OUTPUT)
    write_file('index.html', environment.get_template('index.html').render(chysel={'entries': entries, 'site': SITE}))

    print '   %s%s -> %s%sindex.html' % (TEMPLATE_PATH, 'archives.html', OUTPUT, 'archives/')
    write_file('archives/index.html', environment.get_template('archives.html').render(chysel={'entries': entries, 'site': SITE}))

    for asset in [asset for asset in os.listdir(TEMPLATE_PATH) if os.path.isdir(os.path.join(TEMPLATE_PATH, asset))]:
        print '   %s%s -> %s%s/' % (TEMPLATE_PATH, asset, OUTPUT, asset)
        dir_util.copy_tree(TEMPLATE_PATH + asset, OUTPUT + asset)

    print ' * Generating entries...'

    for entry in entries:
        print '   %s%s -> %s%sindex.html' % (INPUT, entry['slug'], OUTPUT, entry['url'])
        write_file(entry['url'] + 'index.html', environment.get_template('entry.html').render(chysel={'entry': entry, 'site': SITE}))

    print 'Browse at: <%s>' % (SITE['url'])
