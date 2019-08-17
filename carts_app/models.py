from django.db import models


class Cart(models.Model):

    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    session_id = models.CharField(max_length=32, blank=True)

    items = models.ManyToManyField("CartItem")

    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_display_text if self.user else self.session_id


class CartItem(models.Model):
    product = models.ForeignKey("products.Product", models.PROTECT)
    rate = models.ForeignKey("products.Rate", on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField(default=1)
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return "{} * {} * {} = {}".format(self.product.get_display_text, self.quantity, self.rate.amount, self.amount)
