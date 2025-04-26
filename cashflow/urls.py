from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views

router = DefaultRouter()
router.register('cashflow', views.CashFlowRecordViewSet, basename='cashflow')
router.register('status', views.StatusViewSet, basename='status')
router.register('stats', views.FilteredStatsViewSet, basename='filtered-stats')

urlpatterns = [
    path('', include(router.urls))
]
