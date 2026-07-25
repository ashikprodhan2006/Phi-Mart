from django.contrib import admin
from product.models import Product, Category, Review, SubCategory, ProductImage

# Register your models here.

admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Review)
