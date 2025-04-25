from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views

router = DefaultRouter()
router.register('types', views.TypeViewSet, basename='types')
router.register('categories', views.CategoryViewSet, basename='categories')
router.register('subcategories', views.SubcategoryViewSet, basename='subcategories')

urlpatterns = [
    path('', include(router.urls))
]
