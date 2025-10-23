from django.urls import path
from userMeasurement.views import show_measurement, update_measurement

app_name = 'userMeasurement'

urlpatterns = [
    path('', show_measurement, name='show_measurement'),
    path('update/', update_measurement, name='update_measurement'),
]