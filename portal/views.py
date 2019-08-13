from django.shortcuts import render
from django.views.generic import TemplateView, View


class HomeView(TemplateView):
    template_name = "portal/home.html"


class ContactView(TemplateView):
    template_name = "portal/contact.html"