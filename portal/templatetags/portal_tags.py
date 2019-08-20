from django import template
from products.models import Category

register = template.Library()


@register.simple_tag
def get_category_url_by_name_contains(name):
    qs = Category.objects.filter(name__icontains=name)
    if qs.exists():
        return qs.first().get_absolute_url
