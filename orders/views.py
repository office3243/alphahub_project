from django.shortcuts import render, get_object_or_404, redirect
from carts_app.views import get_request_cart
from .models import Order, Address
from django.views.generic import DetailView, ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404
from .forms import OrderPlaceForm
import random
import string
import decimal


def order_id_generator(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    random_id = ''.join(random.choice(chars) for _ in range(size))
    if not Order.objects.filter(order_id=random_id).exists():
        return random_id
    return order_id_generator()


@login_required
def place(request):
    if request.method == "POST":
        form = OrderPlaceForm(request.POST)
        if form.is_valid():
            cart = get_request_cart(request)
            line_1, line_2, locality, zip_code, phone = request.POST['line_1'], request.POST['line_2'], request.POST['locality'], request.POST['zip_code'], request.POST['phone']
            order = Order.objects.create(user=request.user, line_1=line_1, line_2=line_2, locality=locality, zip_code=zip_code, phone=phone)
            for item in cart.cartitem_set.all():
                order.items.add(item)
                item.cart = None
                item.save()
            order.save()
            return redirect(order.get_absolute_url)
    return redirect("carts_app:cart_view")


class OrderPlaceView(LoginRequiredMixin, CreateView):
    model = Order
    fields = ("line_1", "line_2", "locality", "zip_code", "phone")
    success_url = "/"

    def form_valid(self, form):
        form = form.save(commit=False)
        form.instance.user = self.request.user
        super().form_valid(form)


class OrderDetailView(LoginRequiredMixin, DetailView):

    model = Order
    template_name = "orders/detail.html"
    slug_url_kwarg = "order_id"
    slug_field = "order_id"

    def get_object(self, queryset=None):
        order = super().get_object()
        if order.user == self.request.user:
            return order
        else:
            raise Http404("Not matching Order")


class OrderListView(LoginRequiredMixin, ListView):

    model = Order
    template_name = "orders/list.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

#
# def payment_make(request, order_id):
#     order = get_object_or_404(Order, order_id=order_id, user=request.user)
#
