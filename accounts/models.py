from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class MyModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Currency(MyModel):
    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=10)

    def __str__(self):
        return self.abbreviation
    
class AccountType(MyModel):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Account(MyModel):
    name = models.CharField(max_length=200, unique=True, null=False)
    slug = models.SlugField(unique=True, db_index=True)
    amount = models.DecimalField(max_digits=16, decimal_places=2, default = 0.00, validators=[MinValueValidator(0.00)])
    curency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, related_name="accounts")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    type= models.ForeignKey(
        AccountType, on_delete=models.SET_NULL, null=True, related_name="accounts")
    number = models.BigIntegerField(default = 1000000000000000, null = True, validators=[MinValueValidator(1000000000000000),MaxValueValidator(9999999999999999)])

class AccountLogs(MyModel):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, null=True, related_name="account_logs")
    old_amount = models.DecimalField(max_digits=16, decimal_places=2, default = 0.00, validators=[MinValueValidator(0.00)])
    new_amount = models.DecimalField(max_digits=16, decimal_places=2, default = 0.00, validators=[MinValueValidator(0.00)])
    curency = models.ForeignKey(
        Currency, on_delete=models.SET_NULL, null=True, related_name="account_logs")
    difference = models.DecimalField(max_digits=16, decimal_places=2, default = 0.00)