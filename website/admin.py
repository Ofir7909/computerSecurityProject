from django.contrib import admin
from .models import Token, User, Client, PasswordHistory

# Register your models here.
admin.site.register(User)
admin.site.register(Client)
admin.site.register(Token)
admin.site.register(PasswordHistory)
