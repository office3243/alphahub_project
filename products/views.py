from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DeleteView, DetailView
from .models import Product, Category
from django_filters.views import FilterView
from .filters import ProductFilter, PenFilter
from carts_app.forms import CartItemAddForm
import json

class ProductListView(ListView):

    model = Product
    template_name = "products/list.html"
    context_object_name = "products"


class CategoryProductListView(ListView):

    model = Product
    template_name = "products/category_products_list.html"
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        if "id" in self.kwargs:
            context['products'] = context['products'].filter(category__id=self.kwargs['id'])
            context['category'] = get_object_or_404(Category, id=self.kwargs['id'])
        return context


class ProductListFilterView(FilterView):

    filterset_class = ProductFilter
    template_name = "products/list_filter.html"
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class ProductDetailView(DetailView):

    model = Product
    template_name = "products/detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['cart_item_form'] = CartItemAddForm()
        context['rates_dict'] = {int(rate.quantity): round(float(rate.amount), 2) for rate in self.get_object().rate_set.order_by("-quantity")}
        return context


class CategoryListView(ListView):

    model = Category
    template_name = "products/category_list.html"
    context_object_name = "categories"
