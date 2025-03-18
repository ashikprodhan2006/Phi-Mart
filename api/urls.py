from django.urls import path, include
# from rest_framework.routers import DefaultRouter #SimpleRouter
from product.views import ProductViewSet, CategoryViewSet, ReviewViewSet, ProductImageViewSet
from order.views import CartViewSet, CartItemViewSet, OrderViewset
from rest_framework_nested import routers


# router = SimpleRouter()
# router = DefaultRouter()
router = routers.DefaultRouter()
# router.register('products', ProductViewSet)
router.register('products', ProductViewSet, basename='products')
router.register('categories', CategoryViewSet)
router.register('carts', CartViewSet, basename='carts')
router.register('orders', OrderViewset, basename='orders')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-review')
product_router.register('images', ProductImageViewSet, basename='product-images')


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
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]



