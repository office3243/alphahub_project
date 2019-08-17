from django.shortcuts import render
from django.views.generic import ListView, DeleteView, DetailView
from .models import Product


class ProductListView(ListView):

    model = Product
    template_name = "products/list.html"
    context_object_name = "products"


