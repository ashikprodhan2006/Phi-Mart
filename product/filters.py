# from django_filters.rest_framework import FilterSet
import django_filters
from product.models import Product



# class ProductFilter(FilterSet):
#     class Meta:
#         model = Product
#         fields = {
#             'category_id': ['exact'],
#             'price': ['gt', 'lt']
#         }


# class ProductFilter(FilterSet):
#     class Meta:
#         model = Product
#         fields = {
#             'subcategory_id': ['exact'],
#             'subcategory__category_id': ['exact'],
#             'price': ['gt', 'lt'],
#         }

class ProductFilter(django_filters.FilterSet):
    category_id = django_filters.NumberFilter(
        field_name="subcategory__category_id"
    )

    class Meta:
        model = Product
        fields = {
            "subcategory_id": ["exact"],
            "price": ["gt", "lt"],
        }