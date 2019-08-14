from django.contrib import admin
from .models import Product, Photo, Rate, SpecificationName, OrderProduct, Category, Specification

admin.site.register(Photo)
admin.site.register(Rate)
admin.site.register(OrderProduct)
admin.site.register(SpecificationName)
admin.site.register(Category)
admin.site.register(Specification)


class PhotoInline(admin.TabularInline):
    model = Photo


class RateInline(admin.TabularInline):
    model = Rate


# class SpecificationInline(admin.TabularInline):
#     model = Specification


class ProductAdmin(admin.ModelAdmin):
    inlines = [PhotoInline, RateInline]


admin.site.register(Product, ProductAdmin)
