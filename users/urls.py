from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register('', views.LoginViewSet, basename='login')
router.register('', views.RegisterViewSet, basename='register')
router.register('', views.ForgotPasswordViewSet, basename='forgot_password')
router.register('', views.RestorePasswordViewSet, basename='restore_password')
router.register('', views.LogoutViewSet, basename='logout')
urlpatterns = [
    path('', include(router.urls))
]
