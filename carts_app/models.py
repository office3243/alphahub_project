from django.db import models
from django.db.models.signals import post_save


class Cart(models.Model):

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    session_id = models.CharField(max_length=32, blank=True)

    items = models.ManyToManyField("CartItem")

    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_display_text if self.user else self.session_id


class CartItem(models.Model):
    product = models.ForeignKey("products.Product", models.PROTECT)
    rate = models.ForeignKey("products.Rate", on_delete=models.PROTECT, blank=True)
    quantity = models.PositiveSmallIntegerField(default=1)
    amount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return "{} * {} * {} = {}".format(self.product.get_display_text, self.quantity, self.rate.amount, self.amount)

    def save(self, *args, **kwargs):
        rate = self.product.rate_set.filter(quantity__lte=1000).order_by("-quantity").first()
        if not hasattr(self, "rate") or self.rate != rate:
            print(rate)
            self.rate = rate
            super().save()
        # amount = self.rate.get_per_piece_price * self.quantity
        # if self.amount != amount:
        #     self.amount = amount
        #     super().save()
        # super().save()

#     def assign_rate(self, *args, **kwargs):
#         rate = self.product.rate_set.filter(quantity__lte=1000).order_by("-quantity").first()
#         if not hasattr(self, "rate") or self.rate != rate:
#             print(rate)
#             self.rate = rate
#             self.save()
#
#     def assign_amount(self, *args, **kwargs):
#         amount = self.rate.get_per_piece_price * self.quantity
#         if self.amount != amount:
#             self.amount = amount
#             self.save()
#
#
# def valid_item(sender, instance, *args, **kwargs):
#     if not instance.rate:
#         instance.assign_rate()
#         instance.save()
#     amount = instance.amount
#     if instance.amount != amount:
#         instance.assign_amount()
#
#
# post_save.connect(valid_item, sender=CartItem)