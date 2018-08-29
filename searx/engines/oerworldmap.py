"""
 OerWorldMap (Map)

 @website     https://oerworldmap.org/
 @provide-api yes (somewhere, have to ask them)

 @using-api   yes
 @results     JSON
 @stable      yes
 @parse       url, title
"""

from searx.url_utils import urlencode

# engine dependent config
categories = ['map']
paging = False

# search-url
base_url = 'https://oerworldmap.org/resource/?q={query}&size=20&features=true'
search_string = ''
# base_url = 'https://nominatim.openstreetmap.org/'
# search_string = 'search/{query}?format=json&polygon_geojson=1&addressdetails=1'
result_base_url = 'https://openstreetmap.org/{osm_type}/{osm_id}'


# do search-request
def request(query, params):
    params['headers'] = {'Accept': 'application/json'}
    q = urlencode({"q": query})
    params['url'] = f'https://oerworldmap.org/resource/?{q}&size=20&features=true'

    return params


# get response from search-request
def response(resp):
    results = []
    json = resp.json()

    for r in json['features']['features']:
        prop = r['properties']

        title = prop['name'][0]['@value']  # TODO, seems like language strings, not sure tho.
        osm_type = r.get('osm_type', r.get('type'))
        # url = result_base_url.format(osm_type=osm_type,
        #                              osm_id=r['osm_id'])
        url=''

        # osm = {'type': osm_type,
        #        'id': r['osm_id']}

        geojson = r['geometry']

        address_raw = r.get('address')
        address = {}

        # get name
        # if r['class'] == 'amenity' or \
        #         r['class'] == 'shop' or \
        #         r['class'] == 'tourism' or \
        #         r['class'] == 'leisure':
        #     if address_raw.get('address29'):
        #         address = {'name': address_raw.get('address29')}
        #     else:
        #         address = {'name': address_raw.get(r['type'])}

        # add rest of adressdata, if something is already found
        location = prop['location']
        if type(location) == list:
            location = location[0]
        if 'address' in location:
            a = location['address']
            address.update({'house_number': 1,  # TODO, regex? addresses are weird. Better not do that.
                            'road': a.get('streetAddress'),
                            'locality': a.get('addressLocality'),
                            'postcode': a.get('postalCode'),
                            'country': a.get('addressRegion'),
                            'country_code': a.get('addressCountry')})
        else:
            address = None

        # append result
        results.append({'template': 'map.html',
                        'title': title,
                        'content': '',
                        'longitude': location['geo']['lon'],
                        'latitude': location['geo']['lat'],
                        'boundingbox': '',
                        'geojson': geojson,
                        'address': address,
                        'osm': '',
                        'url': f'https://oerworldmap.org/resource/{prop["@id"]}'})

    # return results
    return results
