from django.contrib import admin
from .models import Currency, AccountType, Account

# Register your models here.

class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("name",)


class AccountTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)


class AccountAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}

admin.site.register(Currency, CurrencyAdmin)
admin.site.register(AccountType, AccountTypeAdmin)
admin.site.register(Account, AccountAdmin)