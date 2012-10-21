#!/usr/bin/env python
#
# chisel
#   David Zhou <https://github.com/dz/chisel>
#   Alan Schneider <https://github.com/shkschneider/chisel>
#

### DEPENDS: jinja2 markdown ###

try:
    from distutils import dir_util
    import markdown
    import codecs
    import jinja2
    import time
    import sys
    import os
    import re
except ImportError as error:
    print 'ImportError: ', str(error)
    exit(1)

### SETTINGS ###

INPUT = './content/' # ends with slash
OUTPUT = './www/' # ends with slash
HOME_SHOW = 15
TEMPLATE_PATH = './templates/'
TEMPLATE_OPTIONS = {}
TEMPLATES = {'index': 'index.html',
             'page': 'page.html',
             'archive': 'archive.html'}
TIME_FORMAT = '%B %d, %Y'
ENTRY_TIME_FORMAT = '%m/%d/%Y'
FORMAT = lambda text: markdown.markdown(text, ['footnotes'])

### DO NOT EDIT BELOW THIS LINE ###

STEPS = []

def step(func):
    def wrapper(*args, **kwargs):
        print func.__name__
        func(*args, **kwargs)
    STEPS.append(wrapper)
    return wrapper

def get_tree(source):
    files = []
    for root, ds, fs in os.walk(source):
        for name in fs:
            if name[0] == '.':
                continue
            path = os.path.join(root, name)
            with open(path, 'rU') as f:
                title = f.readline()
                date = time.strptime(f.readline().strip(), ENTRY_TIME_FORMAT)
                year, month, day = date[:3]
                files.append({'title': title,
                              'epoch': time.mktime(date),
                              'content': FORMAT(''.join(f.readlines()[1:]).decode('UTF-8')),
                              'url': '/'.join([str(year), '%.2d' % month, '%.2d' % day, os.path.splitext(name)[0] + '.html']),
                              'pretty_date': time.strftime(TIME_FORMAT, date),
                              'date': date,
                              'year': year,
                              'month': month,
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
    '''Generate homepage'''
    template = e.get_template(TEMPLATES['index'])
    write_file('index.html', template.render(entries=f[:HOME_SHOW]))

@step
def step_page(f, e):
    '''Generate detail pages of individual posts'''
    template = e.get_template(TEMPLATES['page'])
    for file in f:
        write_file(file['url'], template.render(entry=file))

@step
def step_archive(f, e):
    '''Generate master archive list of all entries'''
    template = e.get_template(TEMPLATES['archive'])
    write_file('archive.html', template.render(entries=f))

@step
def step_assets(f, e):
    '''Copies assets'''
    for name in [name for name in os.listdir(TEMPLATE_PATH) if os.path.isdir(os.path.join(TEMPLATE_PATH, name))]:
        dir_util.copy_tree(TEMPLATE_PATH + name, OUTPUT + name)

def main():
    print 'Chiseling...'
    print '* Reading files...',
    files = sorted(get_tree(INPUT), cmp=compare_entries)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH), **TEMPLATE_OPTIONS)
    print 'Done.'
    print '* Running steps...'
    for step in STEPS:
        print '  ',
        step(files, env)
    print 'Done.'

if __name__ == '__main__':
    sys.exit(main())
