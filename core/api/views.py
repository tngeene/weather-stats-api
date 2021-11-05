import requests
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

base_weather_api_url = settings.BASE_WEATHER_API_URL
weather_api_key = settings.WEATHER_API_KEY


class WeatherStatisticsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):

        

        if 'days' in request.GET.keys():
            days_to_lookup = int(request.GET.get("days"))
            # check whether days to look up lie between 1 and 10 days
            acceptable_range_of_days = range(1, 11)
            if days_to_lookup in acceptable_range_of_days:
                city = kwargs.get("city")
                forecast_data = self.get_city_forecast_stats(city, days_to_lookup)
                return forecast_data
            else:
                raise NotAcceptable(
                    _("Number of days to look up must lie between 1 to 10")
                )

        else:
            raise NotAcceptable(_("Provide number of days to look up forecast"))

    def get_city_forecast_stats(self, city, days):
        url = f"{base_weather_api_url}/forecast.json?key={weather_api_key}&q={city}&days={days}&aqi=no&alerts=no"

        response = requests.get(url)

        if response.status_code == 200:
            forecast_response = response.json()
            forecast_lookup = forecast_response.get("forecast").get("forecastday")

            forecast_stats = {
                "maximum": 20,
                "minimum": 204,
                "average": 3020,
                "median": 21,
            }
            return Response(forecast_stats, status=status.HTTP_200_OK)
        else:
            return Response(response.json(), status=response.status_code)
