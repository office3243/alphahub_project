from django.shortcuts import render
from django.views.generic import ListView, DeleteView, DetailView
from .models import Product
from django_filters.views import FilterView
from .filters import ProductFilter, PenFilter


class ProductListView(ListView):

    model = Product
    template_name = "products/list.html"
    context_object_name = "products"


class ProductListFilterView(FilterView):

    filterset_class = ProductFilter
    template_name = "products/list_filter.html"
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class PenFilterView(FilterView):

    filterset_class = PenFilter
    template_name = "products/pen_list_filter.html"
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class ProductDetailView(DetailView):

    model = Product
    template_name = "products/detail.html"
    context_object_name = "product"


