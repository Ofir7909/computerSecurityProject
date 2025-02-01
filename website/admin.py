from django.contrib import admin
from .models import Token, User, Client, PasswordHistory

admin.site.register(User)
admin.site.register(Client)
admin.site.register(Token)
admin.site.register(PasswordHistory)
