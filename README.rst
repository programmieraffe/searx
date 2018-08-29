A searx fork for OER
====================

This is a proof of concept for connecting several free license centric repositories and other sites.

Main change is adding the SPDX License repository. (do a recursive checkout!)
With this, we can (try) to match openly licenced content and provide this information to users.

further possible candidates, for openly licensed content:

- jamendo: https://developer.jamendo.com/v3.0/tracks
- figshare: https://docs.figshare.com/
- pixabay: https://pixabay.com/api/docs/#api_search_images
- flickr: https://www.flickr.com/services/api/flickr.photos.search.html
  in combination with https://www.flickr.com/services/api/flickr.photos.getInfo.html for a license id.
  and how they are mapped: https://www.flickr.com/services/api/flickr.photos.licenses.getInfo.html
- europeana: https://pro.europeana.eu/page/api-rest-console?function=search&query=Paris&reusability=open&media=true
  and https://pro.europeana.eu/resources/apis/search
- sources listed in 'OER-Hoernchen' https://oerhoernchen.de/suche
- memucho


searx
=====

A privacy-respecting, hackable `metasearch
engine <https://en.wikipedia.org/wiki/Metasearch_engine>`__.

Pronunciation: səːks

List of `running
instances <https://github.com/asciimoo/searx/wiki/Searx-instances>`__.

See the `documentation <https://asciimoo.github.io/searx>`__ and the `wiki <https://github.com/asciimoo/searx/wiki>`__ for more information.

|OpenCollective searx backers|
|OpenCollective searx sponsors|

Installation
~~~~~~~~~~~~

-  clone source:
   ``git clone https://github.com/asciimoo/searx.git && cd searx``
-  install dependencies: ``./manage.sh update_packages``
-  edit your
   `settings.yml <https://github.com/asciimoo/searx/blob/master/searx/settings.yml>`__
   (set your ``secret_key``!)
-  run ``python searx/webapp.py`` to start the application

For all the details, follow this `step by step
installation <https://github.com/asciimoo/searx/wiki/Installation>`__.

Bugs
~~~~

Bugs or suggestions? Visit the `issue
tracker <https://github.com/asciimoo/searx/issues>`__.

`License <https://github.com/asciimoo/searx/blob/master/LICENSE>`__
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

More about searx
~~~~~~~~~~~~~~~~

-  `openhub <https://www.openhub.net/p/searx/>`__
-  `twitter <https://twitter.com/Searx_engine>`__
-  IRC: #searx @ freenode


.. |OpenCollective searx backers| image:: https://opencollective.com/searx/backers/badge.svg
   :target: https://opencollective.com/searx#backer


.. |OpenCollective searx sponsors| image:: https://opencollective.com/searx/sponsors/badge.svg
   :target: https://opencollective.com/searx#sponsor
