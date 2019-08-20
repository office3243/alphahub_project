from django.shortcuts import render, get_object_or_404
from django.views.generic import FormView, DetailView, View
from django.urls import reverse_lazy
from .models import Cart
from django.http import Http404


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

    def form_valid(self, form):
        temp_form = form.save(commit=False)
        temp_form.instance.cart = get_request_cart(self.request)
        temp_form.save()
        return super().form_valid(temp_form)
