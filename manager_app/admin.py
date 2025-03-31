from django.contrib import admin
from django.contrib.auth.models import User
from .models import Profile, Genba, Notification, DailyReport

admin.site.register(Profile)
admin.site.register(Genba)
admin.site.register(Notification)
admin.site.register(DailyReport)

class ProfileInline(admin.StackedInline):
    model = Profile

class UserAdmin(admin.ModelAdmin):
    model = User
    fields = ['username']
    inlines = [ProfileInline]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)