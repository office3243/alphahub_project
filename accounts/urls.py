from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView, logout_then_login
from . import views

app_name = "accounts"

urlpatterns = [

    url(r"^login/$", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    url(r"^register/$", views.register, name="register"),
    url(r"^logout/$", logout_then_login, {"login_url": "/accounts/login/"}, name="logout"),


]