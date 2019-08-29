from django.db import models
from django.db.models import Aggregate, Sum, Q, Count
from django.urls import reverse_lazy
from accounts.models import User
from django.db.models.signals import m2m_changed, post_save
import random
import string
import decimal


def txn_id_generator(size=6, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    random_id = ''.join(random.choice(chars) for _ in range(size))
    if not Order.objects.filter(txn_id=random_id).exists():
        return random_id
    return txn_id_generator()


class Order(models.Model):

    ORDER_STATUS_CHOICES = (("PL", "Order Placed"), ("RC", "Received"), ("PK", "Packing"),
                            ("SH", "Shipped"), ("CN", "Cancelled"))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField("carts_app.CartItem", blank=True)
    shipping_charges = models.DecimalField(max_digits=7, decimal_places=2, default=100.00)
    other_charges = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    sub_total = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    txn_id = models.CharField(max_length=32, default=txn_id_generator)
    delivery_expected = models.DateTimeField(blank=True, null=True)
    bill = models.FileField(upload_to="orders/bills/", blank=True, null=True)

    line_1 = models.CharField(max_length=264, blank=True)
    line_2 = models.CharField(max_length=264, blank=True)
    locality = models.CharField(max_length=64, blank=True)
    zip_code = models.CharField(max_length=6, blank=True)
    phone = models.CharField(max_length=13, blank=True)

    created_on = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default="PL")
    is_payed = models.BooleanField(default=False)

    def __str__(self):
        return str(self.user)

    @property
    def get_address_text(self):
        return "{}, {}, {}, {}".format(self.line_1, self.line_2, self.locality, self.zip_code)

    @property
    def get_delivery_expected(self):
        if self.delivery_expected:
            return self.delivery_expected.strftime("%d-%m-%Y")
        else:
            return "Expected Delivery Date will be informed soon"

    @property
    def get_absolute_url(self):
        return reverse_lazy("orders:detail", kwargs={"pk": str(self.id)})

    @property
    def get_created_date(self):
        return self.created_on.strftime("%d-%m-%Y")

    @property
    def get_status(self):
        return self.get_status_display()

    @property
    def get_bill_download_link(self):
        if self.bill:
            return "/bill"
        else:
            return ""

    @property
    def get_create_payment_url(self):
        return reverse_lazy("payments:paytm_create_payment", kwargs={'txn_id': self.txn_id})


def assign_amount(sender, instance, action, *args, **kwargs):
    sub_total = decimal.Decimal(0.00)
    for item in instance.items.all():
        sub_total += item.amount
    if instance.sub_total != sub_total:
        instance.sub_total = sub_total
        instance.save()


def assing_total_amount(sender, instance, *args, **kwargs):
    if instance.sub_total != 0.00:
        total_amount = instance.sub_total + decimal.Decimal(instance.shipping_charges)
        if instance.total_amount != total_amount:
            instance.total_amount = total_amount
            instance.save()


post_save.connect(assing_total_amount, sender=Order)
m2m_changed.connect(assign_amount, sender=Order.items.through)
