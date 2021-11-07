from statistics import mean

import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..utils import build_url, calculate_median

base_weather_api_url = settings.BASE_WEATHER_API_URL
weather_api_key = settings.WEATHER_API_KEY


class WeatherStatisticsAPIView(APIView):
    # make the API to be open, no authentication needed
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        # ensure that the day query param exists in the url,
        # and that it has a value.
        # if not, raise an exception error.
        if "days" in request.GET.keys():
            days = request.GET.get("days")
            if days is not None and days != "":
                try:
                    days_to_lookup = int(days)
                    # check whether days to look up lie between 1 and 10 days,
                    # if not raise exception errors
                    acceptable_range_of_days = range(1, 11)
                    if days_to_lookup in acceptable_range_of_days:
                        city = kwargs.get("city")
                        forecast_data_stats = self.get_city_forecast_stats(
                            city, days_to_lookup
                        )
                        return forecast_data_stats

                    raise NotAcceptable(
                        _("Number of days to look up must be between 0 and 10")
                    )
                except ValueError:
                    raise NotAcceptable(_("Days provided must be a valid integer."))

            raise NotAcceptable(_("Number of days to lookup cannot be an empty value."))

        raise NotAcceptable(_("Provide number of days to look up forecast"))

    def get_city_forecast_stats(self, city, days):
        # defines the weather api endpoint to make requests to
        base_url = f"{base_weather_api_url}/forecast.json"
        url = build_url(
            base_url,
            params={
                "key": weather_api_key,
                "q": city,
                "days": days,
                "aqi": "no",
                "alerts": "no",
            },
        )
        response = requests.get(url)

        # response handling. If succesful, return the results in json form.
        if response.status_code == 200:
            forecast_response = response.json()
            forecast_lookup_list = forecast_response.get("forecast").get("forecastday")

            # retrieve the 'day' key in the responses as this
            # holds all data we want to retrieve from the API
            forecasted_days_conditions = [
                forecast.get("day") for forecast in forecast_lookup_list
            ]

            # initialize the temperatures we need as empty lists till
            # we loop through the response data
            max_temperatures = []
            min_temperatures = []
            average_temperatures = []

            # loop through the forecasted list and retrieve the temp values
            # after which, append each to the relevant array.
            for forecasted_day_condition in forecasted_days_conditions:
                max_temperatures.append(forecasted_day_condition.get("maxtemp_c"))
                min_temperatures.append(forecasted_day_condition.get("mintemp_c"))
                average_temperatures.append(forecasted_day_condition.get("avgtemp_c"))

            average_temperature = round(mean(average_temperatures), 2)
            median_temperature = calculate_median(average_temperatures)

            forecast_stats = {
                "maximum": max(max_temperatures),
                "minimum": min(min_temperatures),
                "average": average_temperature,
                "median": median_temperature,
            }
            return Response(forecast_stats, status=status.HTTP_200_OK)
        
        # in case of any error from the API response, capture it and return
        # message in form of a json object, with corresponding status code
        return Response(response.json(), status=response.status_code)
