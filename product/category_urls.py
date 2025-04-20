from django.urls import path
from product import views


urlpatterns = [
    # path('', views.view_categories, name='categories-list'),
    # path('', views.ViewCategories.as_view(), name='categories-list'),
    path('', views.CategoryList.as_view(), name='categories-list'),
    # path('<int:id>/', views.view_specific_category, name='view-specific-category'),
    # path('<int:id>/', views.ViewSpecificCategory.as_view(), name='view-specific-category'),
    path('<int:pk>/', views.CategoryDetails.as_view(), name='view-specific-category'),
]