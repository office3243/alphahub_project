from django.shortcuts import render, get_object_or_404
from carts_app.views import get_request_cart
from .models import Order, Address


def place(request):
    cart = get_request_cart(request)
    address = get_object_or_404(Address, id=request.POST['address_id'], user=request.user)
    order = Order.objects.create(user=request.user, address=address)
    order.items.add(list(cart.cartitem_set.all()))
    cart.cartitem_set.all().delete()
    order.save()
    return
