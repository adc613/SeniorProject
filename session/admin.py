from django.contrib import admin

from .models import AppSession, ConditionalSession

admin.site.register(AppSession)
admin.site.register(ConditionalSession)
