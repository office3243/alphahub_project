from django.db import models
from django.db.models.signals import post_save
from products.validators import validate_nonzero
from django.core.validators import ValidationError
from django.shortcuts import get_list_or_404
from django.http import Http404
import uuid
from django.urls import reverse_lazy


class Cart(models.Model):

    user = models.OneToOneField("accounts.User", on_delete=models.CASCADE, blank=True, null=True)
    uuid = models.UUIDField(default=uuid.uuid4)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.phone if self.user else str(self.uuid)


class CartItem(models.Model):
    product = models.ForeignKey("products.Product", models.PROTECT)
    rate = models.ForeignKey("products.Rate", on_delete=models.PROTECT, blank=True, null=True)
    quantity = models.PositiveSmallIntegerField(default=1, validators=[validate_nonzero])
    amount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {} X {} = {}".format(self.product.get_display_text, self.get_unit_rate, self.quantity, self.amount)

    @property
    def get_amount(self):
        return self.amount if hasattr(self, "amount") else "Unknown"

    @property
    def get_unit_rate(self):
        if self.rate is not None:
            return self.rate.per_piece_amount
        return "Unknown"

    def clean(self):
        if self.product.category.is_rate_qty:
            allowed_quantities = self.product.rate_set.order_by("quantity").values_list("quantity", flat=True)
            if self.quantity not in allowed_quantities:
                raise ValidationError(
                    "Quantity Not Allowed"
                )
        else:
            qty = self.product.rate_set.order_by("quantity").first().quantity
            if self.quantity < qty:
                raise ValidationError(
                    "Minimum allowed quantity is {}".format(qty)
                )

    def save(self, *args, **kwargs):
        if self.rate is not None:
            amount = self.quantity * self.rate.per_piece_amount
            if self.amount != amount:
                self.amount = amount
                super().save()
        super().save()


def assign_rate(sender, instance, *args, **kwargs):
    rate = instance.product.rate_set.filter(quantity__lte=instance.quantity).order_by("-quantity").first()
    if not hasattr(instance, "rate") or instance.rate != rate:
        instance.rate = rate
        instance.save()


def assign_amount(sender, instance, *args, **kwargs):
    if instance.rate is not None:
        try:
            amount = instance.quantity * instance.rate.per_piece_amount
            if instance.amount != amount:
                instance.amount = amount
                instance.save()
        except:
            instance.save()


post_save.connect(assign_rate, sender=CartItem)
post_save.connect(assign_amount, sender=CartItem)
