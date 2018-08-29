"""
 Wikipedia (Web)

 @website     https://{language}.wikipedia.org
 @provide-api yes

 @using-api   yes
 @results     JSON
 @stable      yes
 @parse       url, infobox
"""

from lxml.html import fromstring
from searx.url_utils import quote, urlencode
from searx.utils import match_language
from searx.engines import licensing
import urllib.parse
from searx import logger

"""
For more info about the search parameters, visit:
https://en.wikipedia.org/wiki/Special:ApiSandbox#action=query&format=json&prop=imageinfo%7Cimages%7Cdescription%7Cpageimages&titles=Cat&generator=images&iiprop=timestamp%7Cuser%7Curl%7Cextmetadata%7Cmediatype%7Ccanonicaltitle%7Cmime&iimetadataversion=latest&iiextmetadatafilter=&piprop=thumbnail%7Cname&pithumbsize=300

you can play with the parameters and maybe add some more information about the results.
Especially pagination would be incredibly useful
"""


log = logger.getChild('wikimedia')

# search-url
base_url = u'https://{language}.wikipedia.org/'

search_url = base_url + u'w/api.php?{query}'

search_parameters = {
    'action': 'query',
    'format': 'json',
    'prop': 'imageinfo|images|description|pageimages',
    'generator': 'images',
    'iiprop': 'timestamp|user|url|extmetadata|mediatype|mime',
    'iimetadataversion': 'latest',
    'iiextmetadatafilter': '',
    'pithumbsize': '300',
    'titles': '{query_goes_here}'
}
supported_languages_url = 'https://meta.wikimedia.org/wiki/List_of_Wikipedias'


# set language in base_url
def url_lang(lang):
    return match_language(lang, supported_languages).split('-')[0]


# get supported languages from their site
def _fetch_supported_languages(resp):
    supported_languages = {}
    dom = fromstring(resp.text)
    tables = dom.xpath('//table[contains(@class,"sortable")]')
    for table in tables:
        # exclude header row
        trs = table.xpath('.//tr')[1:]
        for tr in trs:
            td = tr.xpath('./td')
            code = td[3].xpath('./a')[0].text
            name = td[2].xpath('./a')[0].text
            english_name = td[1].xpath('./a')[0].text
            articles = int(td[4].xpath('./a/b')[0].text.replace(',', ''))
            # exclude languages with too few articles
            if articles >= 100:
                supported_languages[code] = {"name": name, "english_name": english_name, "articles": articles}

    return supported_languages


class WikiThing:
    def __init__(self):
        self.state = False
    # TODO paging
    def request(self, query, params):
        if self.state:
            log.debug(f'state {self.state}')
            self.state = False
        else:
            log.debug(f'state {self.state}')
            self.state = True

        if query.islower():
            query = u'{0}|{1}'.format(query.decode('utf-8'), query.decode('utf-8').title()).encode('utf-8')

        search_parameters['titles'] = query
        parameters = urllib.parse.urlencode(search_parameters)
        params['url'] = search_url.format(query=parameters,
                                          language=url_lang(params['language']))

        return params

    def response(self, resp):
        results = []
        search_result = resp.json()

        # wikipedia article's unique id
        # first valid id is assumed to be the requested article
        for page in search_result['query']['pages'].values():
            imginfo = page['imageinfo'][0]
            ext = imginfo['extmetadata']
            thumbnail_src = ''
            license_short_name = ''
            if 'LicenseShortName' in ext:
                license_short_name = ext['LicenseShortName']['value']
            else:
                log.debug(f'page has no LicenseShortName: {page}')
            content = ext.get('ImageDescription', {'value': ''})['value']
            artist = ext.get('Artist', {'value': ''})['value']
            template = 'images.html'
            url = imginfo['url']
            mime = imginfo['mime']
            if 'VIDEO' == imginfo['mediatype']:
                template = 'videos.html'
            results.append({
                'url': imginfo['descriptionurl'],
                'title': page.get('title'),
                'content': content,
                'thumbnail_src': page['thumbnail']['source'],
                'thumbnail': page['thumbnail']['source'],
                'embedded': f'<video controls><source src="{url}" type="{mime}"></video>',
                'img_src': url,
                'template': template,
                'author': artist,
                'license': licensing.spdx.maybe_match(license_short_name),
            })
        return results


wt = WikiThing()
request = wt.request
response = wt.response
