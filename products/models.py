from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Rate(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=1)
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    def __str__(self):
        return "{} for {} Rupees".format(self.amount, self.quantity)



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

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def get_display_text(self):
        return self.name

    @property
    def get_headline(self):
        return self.headline

    @property
    def get_photos(self):
        return self.photo_set.all().order_by("preference")

    @property
    def get_base_photo(self):
        return self.photo_set.filter(is_base_photo=True).order_by("preference").first()


def add_slug_with_name(sender, instance, *args, **kwargs):
    slug = slugify(instance.slug)
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


