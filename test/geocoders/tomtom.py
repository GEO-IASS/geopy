
import unittest

from geopy import exc
from geopy.compat import u
from geopy.geocoders import TomTom
from test.geocoders.util import GeocoderTestBase, env


@unittest.skipUnless(  # pylint: disable=R0904,C0111
    bool(env.get('TOMTOM_APIKEY')),
    "No TOMTOM_APIKEY env variable set"
)
class TomTomTestCase(GeocoderTestBase):

    @classmethod
    def setUpClass(cls):
        token = env.get('TOMTOM_APIKEY')
        cls.geocoder = TomTom(token=token, timeout=3)
        print('caraka')

    def test_config_error(self):
        """
        TomTom.__init__ invalid authentication
        """
        with self.assertRaises(exc.ConfigurationError):
            TomTom()

    def test_geocode(self):
        """
        TomTom.geocode
        """
        self.geocode_run(
            {"query": "avenida getulio vargas, 100, uberlandia, minas gerais, brasil"},
            {"latitude": -18.91554, "longitude": -48.28015},
        )

    def test_unicode_name(self):
        """
        TomTom.geocode unicode
        """
        self.geocode_run(
            {"query": u("\u6545\u5bab")},
            {"latitude": 23.47985, "longitude": 120.28024},
        )

    # def test_reverse_point(self):
    #     """
    #     TomTom.reverse using point
    #     """
    #     self.reverse_run(
    #         {"query": Point(40.753898, -73.985071)},
    #         {"latitude": 40.75376406311989, "longitude": -73.98489005863667},
    #     )
