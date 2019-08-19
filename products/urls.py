from django.conf.urls import url
from . import views


app_name = "products"

urlpatterns = [

    # url(r"^$", views.ProductListView.as_view(), name="list"),
    url(r"^$", views.ProductListFilterView.as_view(), name="list"),
    url(r"^detail/(?P<slug>[-\w]+)/$", views.ProductDetailView.as_view(), name="detail"),
    url(r'^visiting_cards/$', views.ProductListFilterView.as_view(), name="visiting_cards"),
    url(r'^pens/$', views.PenFilterView.as_view(), name="pens"),
    url(r'^identity_cards/$', views.ProductListFilterView.as_view(), name="identity_cards"),
]
