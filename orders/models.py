from django.db import models
from django.db.models import Aggregate, Sum, Q, Count


class Order(models.Model):

    ORDER_STATUS_CHOICES = (("PL", "Order Placed"), ("RC", "Received"), ("PK", "Packing"),
                            ("SH", "Shipped"), ("CN", "Cancelled"))

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    items = models.ManyToManyField("carts_app.CartItem")
    address = models.ForeignKey("Address", on_delete=models.PROTECT)
    shipping_charges = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    other_charges = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)
    total_amount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    created_on = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=2, choices=ORDER_STATUS_CHOICES, default="PL")
    is_payed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_display_text

    def save(self, *args, **kwargs):
        total_amount = self.items.aggregate(Sum("amount"))
        print(total_amount)
        if self.total_amount != total_amount:
            self.total_amount = total_amount
            # super().save()
        super().save()


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
