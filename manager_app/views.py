from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.safestring import mark_safe
from django.http import HttpResponse, FileResponse
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.contrib.auth.models import User
import calendar
import csv, urllib
import os
import datetime
now = datetime.datetime.now()

from .models import Profile, Genba, Notification, DailyReport
from .forms import SignUpForm, UserProfileForm, GenbaForm, DailyReportForm

@login_required(login_url='/login_user/')
def home(request):
    if request.user.is_authenticated:
        genba_list = Genba.objects.all().order_by('-date_created')
        genbas = []
        for genba in genba_list:
            date = datetime.datetime(now.year, now.month, now.day)
            start_date = datetime.datetime(genba.start_date.year, genba.start_date.month, genba.start_date.day)
            end_date = datetime.datetime(genba.end_date.year, genba.end_date.month, genba.end_date.day)
            if start_date <= date <= end_date:
                genbas.append(genba)
                if request.user.profile.contract_type == '下請け':
                    for genba in genbas:
                        if genba.head_person != request.user.profile or request.user.profile not in genba.attendees.all():
                            genbas.remove(genba)
        if request.method == "POST":
            content = request.POST.get("content")
            author = User.objects.get(id=request.user.id)
            notification = Notification.objects.create(content=content, author=author)
            notification.save()
        notifications = Notification.objects.all().order_by('-date_created')
        return render(request, "home.html", {"genba_list":genba_list, "genbas": genbas, "notifications": notifications})
    else:
        messages.success(request, "ログインしてください。")
        return redirect("login_user")
    
@login_required(login_url='/login_user/')
def delete_notification(request, notification_id):
    if request.user.is_authenticated:
        notification = Notification.objects.get(id=notification_id)
        notification.delete()
        messages.success(request, "連絡事項を削除しました。")
        return redirect("home")
    else:
        messages.success(request, "ログインしてください。")
        return redirect("login_user")
    
def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.profile:
                messages.success(request, (f"{user.profile} さん, お帰りなさい。"))
            else:
                messages.success(request, ("お帰りなさい。"))
            return redirect("home")
        else:
            messages.success(request, ("ユーザー名、またはパスワードが違います。再度お試しください。"))
            return redirect("login_user")
    else:
        return render(request, "authenticate/login.html", {})  