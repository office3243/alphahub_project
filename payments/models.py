from django.db import models


class Payment(models.Model):

    GATEWAY_CHOICES = (("PT", "Paytm"), )
    STATUS_CHOICES = (("SC", "Success"), ("FL", "Failed"))

    order = models.OneToOneField("orders.Order", on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)
    payment_order_id = models.CharField(max_length=32)
    txnid = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    created_on = models.DateTimeField(auto_now_add=True)
    gateway = models.CharField(max_length=2, choices=GATEWAY_CHOICES, default="PT")
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default="IN")

    def __str__(self):
        return "{} -- {} -- {}".format(self.user.phone, self.amount, self.payment_order_id)
