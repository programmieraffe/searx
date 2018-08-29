"""
This module contains licensing information for templates
"""

import os
from pathlib import Path
from searx import logger
import re

class SpdxLicenses:
    cc_splitter = re.compile(r'CC-([A-Z\-]*)-([0-9]\.[0-9])')
    def __init__(self):
        current_dir = os.path.dirname(os.path.realpath(__file__))
        spdx_folder = Path(current_dir) / '..' / 'data' / 'spdx' / 'src'
        xml_files = spdx_folder.glob('*.xml')
        self.name2file = {}
        self.log = logger.getChild('SpdxLicenses')
        for xmlfile in xml_files:
            self.name2file[xmlfile.stem] = xmlfile

    def maybe_match(self, license_str):
        up = str(license_str).upper().replace(' ', '-')
        if up in self.name2file:
            cc_match = self.cc_splitter.match(up)
            if cc_match:
                return CreativeCommonsLicense(cc_match.group(1).lower(), "Creative Commons", cc_match.group(2))

            return LicenseInfo(license_str, license_str, [], '')
        elif 'PUBLIC-DOMAIN' == up:
            return CreativeCommonsPublicDomain('mark', 'public domain')
        else:
            self.log.debug(f'no matching license for {license_str}')
            return LicenseInfo(license_str, 'Unknown License', [], '')


class LicenseInfo:
    def __init__(self, short_name, full_name, icons, url):
        self._short_name = short_name
        self._full_name = full_name
        self._icons = icons
        self._url = url

    @property
    def short_name(self):
        return self._short_name

    @property
    def full_name(self):
        return self._full_name

    @property
    def icons(self):
        return self._icons

    @property
    def url(self):
        return self._url


class CreativeCommonsLicense(LicenseInfo):
    def __init__(self, name, full_name, version='4.0'):
        icons = [f'/static/cc/{part}.svg' for part in name.split('-')]
        url = f'https://creativecommons.org/licenses/{name}/{version}'
        super().__init__(name, full_name, icons, url)


class CreativeCommonsPublicDomain(LicenseInfo):
    def __init__(self, name, full_name, version='1.0'):
        icons = [f'/static/cc/{part}.svg' for part in name.split('-')]
        url = f'https://creativecommons.org/publicdomain/{name}/{version}'
        super().__init__(name, full_name, icons, url)


class CreativeCommons:
    @property
    def by(self):
        return CreativeCommonsLicense('by', 'Creative Commons Attribution')

    @property
    def by_sa(self):
        return CreativeCommonsLicense('by-sa', 'Creative Commons Attribution-ShareAlike')

    @property
    def by_nd(self):
        return CreativeCommonsLicense('by-nd', 'Creative Commons Attribution-NoDerivs')

    @property
    def by_nc(self):
        return CreativeCommonsLicense('by-nc', 'Creative Commons Attribution-NonCommercial')

    @property
    def by_nc_sa(self):
        return CreativeCommonsLicense('by-nc-sa', 'Creative Commons Attribution-NonCommercial-ShareAlike')

    @property
    def by_nc_nd(self):
        return CreativeCommonsLicense('by-nc-nd', 'Creative Commons Attribution-NonCommercial-NoDerivs')

    @property
    def zero(self):
        return CreativeCommonsPublicDomain('zero', 'Creative Commons Zero')

    @property
    def pd(self):
        return CreativeCommonsPublicDomain('mark', 'Creative Commons Public Domain Mark')


spdx = SpdxLicenses()
