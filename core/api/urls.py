from django.urls import path
from .views import WeatherStatisticsAPIView


app_name = 'weather_lookup_api'

urlpatterns = [
    path('<city>/', WeatherStatisticsAPIView.as_view(), name='stats')
]

