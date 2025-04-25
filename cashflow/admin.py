from django.contrib import admin
from .models import CashFlow, Status

@admin.register(CashFlow)
class CashFlowAdmin(admin.ModelAdmin):
    pass

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    pass