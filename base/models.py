from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

TRANSACTION_TYPES = [
     ("Expense","Expense"),
     ("Revenue","Revenue")
 ]

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    title = models.CharField(max_length = 200)
    description = models.TextField(null = True, blank = True)
    action_type = models.CharField(max_length = 10, choices = TRANSACTION_TYPES)
    quantity = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
        
    def calculate_balance(self):
        expense, revenue = 0, 0
        if self.filter(action_type='Revenue'):
            revenue = self.filter(action_type='Revenue').aggregate(Sum('quantity'))['quantity__sum']
        if self.filter(action_type='Expense'):
            expense = self.filter(action_type='Expense').aggregate(Sum('quantity'))['quantity__sum']
        return revenue - expense

    def __str__ (self):
        return self.title
