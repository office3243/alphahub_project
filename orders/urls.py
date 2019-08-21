from . import views
from django.conf.urls import url

urlpatterns = [
    url("^place/$", views.place, name="place")
]