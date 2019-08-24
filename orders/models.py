from django.db import models
from django.db.models import Aggregate, Sum, Q, Count
import uuid
from django.urls import reverse_lazy
from accounts.models import User
from django.db.models.signals import m2m_changed, post_save
import random
import string
import decimal


def order_id_generator(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    random_id = ''.join(random.choice(chars) for _ in range(size))
    if not Order.objects.filter(order_id=random_id).exists():
        return random_id
    return order_id_generator()


class Order(models.Model):

    ORDER_STATUS_CHOICES = (("PL", "Order Placed"), ("RC", "Received"), ("PK", "Packing"),
                            ("SH", "Shipped"), ("CN", "Cancelled"))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField("carts_app.CartItem", blank=True)
    shipping_charges = models.DecimalField(max_digits=7, decimal_places=2, default=100.00)
    other_charges = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    order_id = models.CharField(max_length=32, default=order_id_generator)
    delivery_expected = models.DateTimeField(blank=True, null=True)
    bill = models.FileField(upload_to="orders/bills/", blank=True, null=True)

    line_1 = models.CharField(max_length=264, blank=True)
    line_2 = models.CharField(max_length=264, blank=True)
    locality = models.CharField(max_length=64, blank=True)
    zip_code = models.CharField(max_length=6, blank=True)
    phone = models.CharField(max_length=13, blank=True)

    uuid = models.UUIDField(default=uuid.uuid4)
    created_on = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default="PL")
    is_payed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    @property
    def get_absolute_url(self):
        return reverse_lazy("orders:detail", kwargs={"uuid": str(self.uuid)})

    @property
    def get_make_recharge_url(self):
        return reverse_lazy()


class Address(models.Model):

    ADDRESS_TYPE_CHOICES = (("SH", "Shop or Office"), ("HM", "Home"))

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    line_1 = models.CharField(max_length=264)
    line_2 = models.CharField(max_length=264)
    locality = models.CharField(max_length=64)
    city = models.CharField(max_length=64, default="Pune")
    state = models.CharField(max_length=64, default="Maharashtra")
    zip_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=13)
    address_type = models.CharField(max_length=2, choices=ADDRESS_TYPE_CHOICES)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Addresses"

    def __str__(self):
        return "{} -- {}".format(self.line_1, self.city)


def assign_amount(sender, instance, action, *args, **kwargs):
    total_amount = decimal.Decimal(0.00)
    print(type(total_amount))
    for item in instance.items.all():
        total_amount += item.amount
    if instance.total_amount != total_amount:
        instance.total_amount = total_amount
        instance.save()


m2m_changed.connect(assign_amount, sender=Order.items.through)
