from django.contrib import admin
from .models import Expense, User
# Register your models here.

admin.site.register([
    Expense, User
])