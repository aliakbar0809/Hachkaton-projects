
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    INCOME = 'income'
    EXPENSE = 'expense'
    TYPE_CHOICES = [
        (INCOME, 'Доход'),
        (EXPENSE, 'Расход'),
    ]

    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f"{self.date} - {self.type} - {self.category.name}: {self.amount}"
