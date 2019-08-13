from django.contrib import admin
from .models import Product, Photo, Rate, OrderOption, OrderProduct, Category, Option

admin.site.register(Photo)
admin.site.register(Rate)
admin.site.register(OrderProduct)
admin.site.register(OrderOption)
admin.site.register(Category)
admin.site.register(Option)


class PhotoInline(admin.TabularInline):
    model = Photo


class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, ]


admin.site.register(Product, ProductAdmin)
