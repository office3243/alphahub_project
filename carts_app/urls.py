from django.conf.urls import url
from . import views


app_name = "carts_app"

urlpatterns = [
    url(r"^$", views.CartView.as_view(), name="cart_view"),
    url(r"^item/add/$", views.ItemAddView.as_view(), name="item_add"),
]
