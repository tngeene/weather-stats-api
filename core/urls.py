from django.urls import path, include

app_name = 'core'

urlpatterns = [
    path('api/locations/', include('core.api.urls'))
]