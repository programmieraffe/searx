from collections import Iterable
from json import loads
from sys import version_info

from searx.engines import licensing
from searx.url_utils import urlencode
from searx.utils import to_string

if version_info[0] == 3:
    unicode = str

search_url = 'https://www.tutory.de/api/v1/search/worksheet?q={query}&page={pageno}'
url_query = 'id'
content_query = 'id'
title_query = 'name'
paging = True
suggestion_query = ''
results_query = 'worksheets'

# parameters for engines with paging support
#
# number of results on each page
# (only needed if the site requires not a page number, but an offset)
page_size = 1
# number of the first page (usually 0 or 1)
first_page_num = 1


def iterate(iterable):
    if type(iterable) == dict:
        it = iterable.items()

    else:
        it = enumerate(iterable)
    for index, value in it:
        yield str(index), value


def is_iterable(obj):
    if type(obj) == str:
        return False
    if type(obj) == unicode:
        return False
    return isinstance(obj, Iterable)


def parse(query):
    q = []
    for part in query.split('/'):
        if part == '':
            continue
        else:
            q.append(part)
    return q


def do_query(data, q):
    ret = []
    if not q:
        return ret

    qkey = q[0]

    for key, value in iterate(data):

        if len(q) == 1:
            if key == qkey:
                ret.append(value)
            elif is_iterable(value):
                ret.extend(do_query(value, q))
        else:
            if not is_iterable(value):
                continue
            if key == qkey:
                ret.extend(do_query(value, q[1:]))
            else:
                ret.extend(do_query(value, q))
    return ret


def query(data, query_string):
    q = parse(query_string)

    return do_query(data, q)


def request(query, params):
    query = urlencode({'q': query})[2:]

    fp = {'query': query}
    if paging and search_url.find('{pageno}') >= 0:
        fp['pageno'] = (params['pageno'] - 1) * page_size + first_page_num

    params['url'] = search_url.format(**fp)
    params['query'] = query
    return params


def response(resp):
    results = []
    json = loads(resp.text)
    for ws in json['worksheets']:
        lic = licensing.spdx.maybe_match(ws.get('licence', 'no license'))
        results.append({
            'url': 'https://www.tutory.de/worksheet/' + ws['id'],
            'title': ws.get('title') or 'no title given',
            'content': ws['description'] or 'no content provided',
            'thumbnail_src': 'https://www.tutory.de/worksheet/' + ws['id'] + '.jpg?width=100',
            'img_src': 'https://www.tutory.de/worksheet/' + ws['id'] + '.jpg?width=300',
            'template': 'images.html',
            'author': ws['user']['firstname'] + ' ' + ws['user']['lastname'],
            'license': lic,
            })
    return results
