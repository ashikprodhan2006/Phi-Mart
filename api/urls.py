from django.urls import path, include
# from rest_framework.routers import DefaultRouter #SimpleRouter
from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet
from order.views import CartViewSet, CartItemViewSet
from rest_framework_nested import routers


# router = SimpleRouter()
# router = DefaultRouter()
router = routers.DefaultRouter()
# router.register('products', ProductViewSet)
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet)
router.register('carts', CartViewSet, basename='carts')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-review')


cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-item')


# urlpatterns = [
#     path('products/', include('product.product_urls')),
#     path('categorys/', include('product.category_urls')),
# ]

# urlpatterns = router.urls


urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls))
]



