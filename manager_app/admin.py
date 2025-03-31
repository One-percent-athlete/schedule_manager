from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Genba, Notification, DailyReport

admin.site.register(Profile)
admin.site.register(Genba)
