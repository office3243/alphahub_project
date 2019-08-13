from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=64)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Rate(models.Model):
    amount = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.PositiveSmallIntegerField(default=1)
    unit_name = models.CharField(max_length=32, default="Pieces")

    def __str__(self):
        return "{} {} for {} Rupees".format(self.amount, self.unit_name, self.quantity)


class Option(models.Model):
    name = models.CharField(max_length=64)
    unit = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Photo(models.Model):

    product = models.ForeignKey("Product", on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    photo = models.ImageField(upload_to="products/photos/")
    preference = models.PositiveSmallIntegerField(default=10)

    is_base_photo = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def get_photo_url(self):
        return self.photo.url


class Product(models.Model):
    name = models.CharField(max_length=128)
    headline = models.CharField(max_length=264, blank=True)
    rates = models.ManyToManyField(Rate)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    options = models.ManyToManyField(Option)

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


class OrderOption(models.Model):
    option = models.ForeignKey(Option, on_delete=models.PROTECT)
    value = models.CharField(max_length=128)

    def __str__(self):
        return "{} = {}".format(self.option.name, self.value)


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, models.PROTECT)
    order_options = models.ManyToManyField(OrderOption)
    rate = models.ForeignKey(Rate, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.product.get_display_text
