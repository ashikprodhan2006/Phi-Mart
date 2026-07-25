from django.urls import path
from product import views

urlpatterns = [
    path('', views.SubCategoryList.as_view(), name='subcategory-list'),
    path('<int:pk>/', views.SubCategoryDetails.as_view(), name='subcategory-detail'),
]