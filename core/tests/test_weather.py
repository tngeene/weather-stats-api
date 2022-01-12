from rest_framework import status
from rest_framework.test import APITestCase

from ..utils import build_reverse_url

base_api_url = "core:weather_lookup_api:stats"


class WeatherForecastLookupTests(APITestCase):
    def test_valid_request(self):
        # A valid request made

        url = build_reverse_url(
            base_api_url,
            kwargs={"city": "mombasa"},
            params={"days": 6},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        expected_keys = ["maximum", "minimum", "average", "median"]
        self.assertEqual(list(response.data), expected_keys)

    def test_days_below_range(self):
        """
        check the results of a scenario
        where a day provided is below 1
        """
        url = build_reverse_url(
            base_api_url,
            kwargs={"city": "Lusaka"},
            params={"days": 0},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data,
            {"detail": "Number of days to look up must be between 0 and 10"},
        )

    def test_days_above_range(self):
        """
        check the results of a scenario
        where the days provided is above 10
        """
        url = build_reverse_url(
            base_api_url,
            kwargs={"city": "London"},
            params={"days": 12},
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data,
            {"detail": "Number of days to look up must be between 0 and 10"},
        )

    def test_days_param_in_url(self):
        # Check if the 'days' query param has been passed
        url = build_reverse_url(base_api_url, kwargs={"city": "Durban"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data,
            {"detail": "Provide number of days to look up forecast"},
        )

    def test_days_param_value_in_url(self):
        # Check if the 'days' query param has is not empty
        url = build_reverse_url(
            base_api_url, kwargs={"city": "kigali"}, params={"days": ""}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data,
            {"detail": "Number of days to lookup cannot be an empty value."},
        )
    
    def test_days_is_an_integer(self):
        # Check if the 'days' query param has is an integer
        url = build_reverse_url(
            base_api_url, kwargs={"city": "cairo"}, params={"days": "two"}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(
            response.data,
            {"detail": "Days provided must be a valid integer."},
        )


    def test_invalid_city_lookup(self):
        # Test response when a non existent city is looked up
        url = build_reverse_url(
            base_api_url, kwargs={"city": "nocity"}, params={"days": 3}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "No matching location found.",
            response.data.get("error").get("message"),
        )
