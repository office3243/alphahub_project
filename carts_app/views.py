from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import FormView, DetailView, View, DeleteView
from django.urls import reverse_lazy
from .models import Cart, CartItem
from django.http import Http404, HttpResponse
from .forms import CartItemAddForm
from products.models import Product
import decimal
from django.core.validators import ValidationError
from django.contrib import messages


def get_request_cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get_or_create(user=request.user)
    else:
        if "cart_uuid" in request.session:
            try:
                cart = Cart.objects.get(uuid=request.session.get("cart_uuid"))
            except Cart.DoesNotExist:
                del request.session['cart_uuid']
                return get_request_cart(request)
        else:
            cart = Cart.objects.create()
            request.session['cart_uuid'] = str(cart.uuid)
    return cart


class ItemAddView(FormView):

    success_url = reverse_lazy("portal:home")
    form_class = CartItemAddForm
    template_name = "carts_app/cart_view2.html"

    def form_valid(self, form):
        temp_form = form.save(commit=False)
        # product = get_object_or_404(Product, id=form.data.get("product_id"))
        temp_form.instance.cart = get_request_cart(self.request)
        # temp_form.instance.product = product
        temp_form.save()
        return super().form_valid(temp_form)


def item_add(request):
    if request.method == "POST":
        product = get_object_or_404(Product, id=request.POST.get("product_id"), is_active=True)
        quantity = int(request.POST['quantity'])
        cart = get_request_cart(request)
        item = CartItem(product=product, cart=cart, quantity=quantity)
        try:
            item.full_clean()
            item.save()
        except ValidationError as e:
            messages.warning(request, "Getting Issues. Please Try Again.")
        return redirect("carts_app:cart_view")
    return redirect("portal:home")


class CartView(DetailView):

    template_name = "carts_app/cart_view.html"
    model = Cart

    def get_object(self, queryset=None):
        return get_request_cart(self.request)


class ItemDeleteView(DeleteView):

    template_name = "carts_app/cart_view.html"
    model = Cart

    def get_object(self, queryset=None):
        return get_request_cart(self.request)


def item_delete(request):
    if request.method == "POST":
        item = get_object_or_404(CartItem, id=request.POST["item_id"], cart=get_request_cart(request))
        item.delete()
        messages.success(request, "Item Deleted Successfully")
        return redirect("carts_app:cart_view")
    return redirect("portal:home")

