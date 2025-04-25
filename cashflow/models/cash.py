from django.db import models
from django.utils.timezone import now
from category.models import Category, Subcategory, Type
from common.models import BaseModel
from users.models import User
from .status import Status


class CashFlow(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cashflow')
    date = models.DateTimeField(default=now)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Record {self.id} -- {self.date}"

    class Meta:
        db_table = 'cash_flow'
        ordering = ('-id',)