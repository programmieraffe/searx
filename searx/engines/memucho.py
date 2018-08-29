from searx.engines import licensing
from searx import logger
from searx.url_utils import urlencode
categories = ['general']  # optional

log = logger.getChild('memucho')


def request(query, params):
    '''pre-request callback
    params<dict>:
      method  : POST/GET
      headers : {}
      data    : {} # if method == POST
      url     : ''
      category: 'search category'
      pageno  : 1 # number of the requested page
    '''
    search = urlencode({'term': query})
    params['url'] = f'https://memucho.de/api/edusharing/search?{search}'

    return params


def response(resp):
    result = []

    json = resp.json()
    log.debug(f'{len(json["Items"])}')
    for item in json['Items']:
        licstr = str(item['Licence']).replace('_', '-').lower()
        result.append({
            'url': item['ItemUrl'],
            'title': item['Name'],
            'content': item['Name'],
            'license': licensing.CreativeCommonsLicense(licstr, 'Creative Commons'),
            'thumbnail_src': item['ImageUrl'],
            'img_src': item['ImageUrl'],
            'author': item['Author'],
            'template': 'images.html'
        })
    return result


