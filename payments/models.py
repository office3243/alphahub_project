from django.db import models


class Payment(models.Model):

    GATEWAY_CHOICES = (("PT", "Paytm"), )
    STATUS_CHOICES = (("IN", "Initiated"), ("SC", "Success"), ("FL", "Failed"))

    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    order_id = models.CharField(max_length=32)
    txnid = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    product_info = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    gateway = models.CharField(max_length=2, choices=GATEWAY_CHOICES)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES)

    def __str__(self):
        return "{} -- {} -- {}".format(self.user.get_display_name, self.amount, self.order_id)
