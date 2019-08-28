from . import views
from django.conf.urls import url

app_name = "orders"

urlpatterns = [
    url("^place/$", views.place, name="place"),
    # url("^place/$", views.OrderPlaceView, name="place"),
    url("^detail/(?P<order_id>[0-9]+)/$", views.OrderDetailView.as_view(), name="detail"),
    url("^list/$", views.OrderListView.as_view(), name="list"),

]
