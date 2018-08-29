#  Vimeo (Videos)
#
# @website     https://vimeo.com/
# @provide-api yes (http://developer.vimeo.com/api),
#              they have a maximum count of queries/hour
#
# @using-api   no (TODO, rewrite to api)
# @results     HTML (using search portal)
# @stable      no (HTML can change)
# @parse       url, title, publishedDate,  thumbnail, embedded, license
#
# @todo        rewrite to api
# @todo        set content-parameter with correct data

from json import loads
from dateutil import parser

from searx.engines import licensing
from searx.url_utils import urlencode

# engine dependent config
categories = ['videos']
paging = True

# search-url
base_url = 'https://vimeo.com/'
search_url = base_url + '/search/page:{pageno}?{query}'

embedded_url = '<iframe data-src="//player.vimeo.com/video/{videoid}" ' +\
    'width="540" height="304" frameborder="0" ' +\
    'webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe>'


# do search-request
def request(query, params):
    params['headers'] = {'Authorization': 'Bearer XXX'}
    params['url'] = search_url.format(pageno=params['pageno'],
                                      query=urlencode({'q': query}))
    params['url'] = 'https://api.vimeo.com/videos?filter=CC'

    return params


# get response from search-request
def response(resp):
    results = []
    data = resp.json()
    # parse results
    for result in data['data']:
        videoid = result['uri'].split('/')[-1]
        url = base_url + videoid
        title = result['name']
        thumbnail = result['pictures']['sizes'][-1]['link']
        publishedDate = parser.parse(result['created_time'])
        embedded = result['embed']['html']

        # append result
        results.append({'url': url,
                        'title': title,
                        'content': 'asd',
                        'template': 'videos.html',
                        'publishedDate': publishedDate,
                        'embedded': embedded,
                        'thumbnail': thumbnail,
                        'license': licensing.CreativeCommonsLicense(result['license'], "Creative Commons")})

    # return results
    return results
