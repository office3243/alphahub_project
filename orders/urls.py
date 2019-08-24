from . import views
from django.conf.urls import url

app_name = "orders"

urlpatterns = [
    url("^place/$", views.place, name="place"),
    # url("^place/$", views.OrderPlaceView, name="place"),
    url("^detail/(?P<uuid>[0-9a-f-]+)/$", views.OrderDetailView.as_view(), name="detail"),
    url("^list/$", views.OrderListView.as_view(), name="list"),

]
