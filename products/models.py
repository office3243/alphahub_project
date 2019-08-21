from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.urls import reverse_lazy
from products.validators import validate_nonzero


class Category(models.Model):
    name = models.CharField(max_length=64)
    is_rate_qty = models.BooleanField(verbose_name="Allow only rate quantities", default=False)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    @property
    def get_display_text(self):
        return self.name.title()

    @property
    def get_absolute_url(self):
        return reverse_lazy("products:category_products_list", kwargs={"id": self.id})


class Rate(models.Model):
    quantity = models.PositiveSmallIntegerField(default=1, validators=[validate_nonzero, ])
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    per_piece_amount = models.DecimalField(max_digits=7, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return "{} Rs for {} Pieces".format(self.amount, self.quantity)

    @property
    def get_per_piece_price(self):
        return "{} Rupees".format(self.per_piece_amount)


def add_per_piece_amount(sender, instance, *args, **kwargs):
    per_piece_amount = round(instance.amount/instance.quantity, 2)
    if per_piece_amount != instance.per_piece_amount:
        instance.per_piece_amount = per_piece_amount
        instance.save()


post_save.connect(add_per_piece_amount, sender=Rate)


# class SpecificationName(models.Model):
#     name = models.CharField(max_length=64)
#     unit = models.CharField(max_length=32)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name

class Photo(models.Model):

    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="products/photos/")
    is_base_photo = models.BooleanField(default=False)

    def __str__(self):
        return self.product.get_display_text

    @property
    def get_photo_url(self):
        return self.photo.url


class Product(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(blank=True)
    headline = models.CharField(max_length=264, blank=True)
    product_code = models.CharField(max_length=32, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    extra_info = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def get_absolute_url(self):
        return reverse_lazy("products:detail", kwargs={"slug": self.slug})

    @property
    def get_specifications(self):
        return self.specification_set.all()

    @property
    def get_display_text(self):
        return self.name

    @property
    def get_headline(self):
        return self.headline

    @property
    def get_photos(self):
        photos = self.photo_set.all()
        return photos

    @property
    def get_base_photo(self):
        photo = self.photo_set.filter(is_base_photo=True).first()
        if not photo:
            photo = self.photo_set.first()
        return photo

    @property
    def get_display_price(self):
        return "{} Rs".format(self.rate_set.filter(quantity__lte=1000).order_by("-quantity").first().per_piece_amount)


def add_slug_with_name(sender, instance, *args, **kwargs):
    slug = slugify(instance.name)
    if instance.slug != slug:
        instance.slug = slug
        instance.save()


pre_save.connect(add_slug_with_name, sender=Product)


class Specification(models.Model):
    # specification_name = models.ForeignKey(SpecificationName, on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=128)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return "{} = {}".format(self.name, self.value)


