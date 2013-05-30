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

STEPS = []

def step(func):
    def wrapper(*args, **kwargs):
        func(*args, **kwargs)
    STEPS.append(wrapper)
    return wrapper

def get_tree(source):
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
                name = re.sub(r'\.[^\.]+$', '', path.replace(INPUT, ''))
                print '  -', name
                category = os.path.dirname(name)
                if len(category):
                    title = category.capitalize() + '/ ' + title
                date = time.strptime(f.readline().strip(), ENTRY_TIME_FORMAT)
                year, month, day = date[:3]
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
                              'filename': name})
    return files

def compare_entries(x, y):
    result = cmp(-x['epoch'], -y['epoch'])
    if result == 0:
        return -cmp(x['filename'], y['filename'])
    return result

def write_file(url, data):
    path = OUTPUT + url
    dirs = os.path.dirname(path)
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    with open(path, 'w') as f:
        f.write(data.encode('UTF-8'))

@step
def step_index(f, e):
    print '  %s%s -> %sindex.html' % (TEMPLATE_PATH, 'index.html', OUTPUT)
    template = e.get_template('index.html')
    write_file('index.html', template.render(chysel={'entries': f, 'site': SITE}))

@step
def step_entries(f, e):
    template = e.get_template('entry.html')
    for file in f:
        print '  %s%s -> %s%sindex.html' % (INPUT, file['slug'], OUTPUT, file['url'])
        write_file(file['url'] + 'index.html', template.render(chysel={'entry': file, 'site': SITE}))

@step
def step_archive(f, e):
    print '  %s%s -> %s%sindex.html' % (TEMPLATE_PATH, 'archives.html', OUTPUT, 'archives/')
    template = e.get_template('archives.html')
    write_file('archives/index.html', template.render(chysel={'entries': f, 'site': SITE}))

@step
def step_about(f, e):
    print '  %s%s -> %s%sindex.html' % (TEMPLATE_PATH, 'about.html', OUTPUT, 'about/')
    template = e.get_template('about.html')
    write_file('about/index.html', template.render(chysel={'entry': f, 'site': SITE}))

@step
def step_assets(f, e):
    for name in [name for name in os.listdir(TEMPLATE_PATH) if os.path.isdir(os.path.join(TEMPLATE_PATH, name))]:
        print '  %s%s -> %s%s' % (TEMPLATE_PATH, name, OUTPUT, name)
        dir_util.copy_tree(TEMPLATE_PATH + name, OUTPUT + name)

if __name__ == '__main__':
    print 'Chyseling'
    print '* Reading files...'
    files = sorted(get_tree(INPUT), cmp=compare_entries)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH), **TEMPLATE_OPTIONS)
    print '* Generating HTML...'
    for step in STEPS:
        step(files, env)
    print 'Browse at: <%s>' % (SITE['url'])
