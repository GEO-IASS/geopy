"""
:class:`.tomtom` geocoder.
"""
from geopy.compat import urlencode
from geopy.exc import ConfigurationError
from geopy.geocoders.base import (Geocoder,
                                  DEFAULT_SCHEME,
                                  DEFAULT_TIMEOUT)
from geopy.location import Location
from geopy.util import logger


class TomTom(Geocoder):

    def __init__(self,
                 token=None,
                 api_version=2,
                 timeout=DEFAULT_TIMEOUT,
                 proxies=None,
                 user_agent=None):
        """
        Create a TomTom-based geocoder.

        :param int token: The token for you authentication.

        :param string scheme: Desired scheme. If authenticated mode is in use,
            it must be 'https'.

        :param int timeout: Time, in seconds, to wait for the geocoding service
            to respond before raising a :class:`geopy.exc.GeocoderTimedOut`
            exception.

        :param dict proxies: If specified, routes this geocoder's requests
            through the specified proxy. E.g., {"https": "192.0.2.0"}. For
            more information, see documentation on
            :class:`urllib2.ProxyHandler`.
        """
        super(TomTom, self).__init__(
            scheme=DEFAULT_SCHEME, timeout=timeout,
            proxies=proxies, user_agent=user_agent
        )

        if not token:
            raise ConfigurationError("The token must be specified.")

        self.token = token

        self.api = '%s://api.tomtom.com/search/%s/' % (self.scheme,
                                                       api_version)

    def _make_location(self, queried_address, coords, raw_address):
        location = None
        if coords:
            location = Location(
                queried_address,
                (coords['lat'], coords['lon']) if coords['lat'] and coords['lon'] else None,
                raw_address
            )
        return location

    def _parse_json(self, response):
        json = None
        results_tag = response.get('results', None)
        if results_tag and len(results_tag) > 0:
            json = results_tag[0].get('position', None)

        return json

    def _compose_url(self, address, params):
        """
        Generate API URL.
        """
        address_encoded = urlencode({'query_address': address})
        return '{url}/geocode/{address}.json?{params}'\
            .format(url=self.api,
                    address=address_encoded.split('=')[1],
                    params=urlencode(params))

    def geocode(self, query, timeout=None, restrict_bbox=None):
        """
        Geocode a location query.

        :param string query: The address or query you wish to geocode.

        :param dict restrict_bbox:
            Restrict the geocode on the extent of this bbox.
            Format:
            {
                'topLeft': '{top},{left}',
                'btmRight': '{bottom},{right}'
            }
            any doubts on bbox see: wiki.openstreetmap.org/wiki/Bounding_Box
        """

        params = {
            'key': self.token
        }

        if restrict_bbox:
            params['topLeft'] = restrict_bbox['topLeft']
            params['btmRight'] = restrict_bbox['btmRight']

        url = self._compose_url(query, params)

        logger.debug("%s.geocode: %s", self.__class__.__name__, url)
        queried_address = query
        response = self._call_geocoder(url)
        coords = self._parse_json(response)

        return self._make_location(queried_address, coords, response)

    def _geocoder_exception_handler(self, error, message): # pylint: disable=R0201,W0613
        print(error)
        print(message)

