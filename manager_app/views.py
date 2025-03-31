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
    
@login_required(login_url='/login_user/')
def logout_user(request):
    logout(request)
    messages.success(request, ("ログアウトしました。"))
    return redirect("login_user")

@login_required(login_url='/login_user/')
def register_user(request):
    if request.user.is_superuser:
        form = SignUpForm()
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                user = authenticate(username=username, password=password)
                messages.success(request, ("プロフィールを入力してください。"))
                return redirect("update_profile", user.pk)
            else:
                messages.success(request, ("再度お試しください。"))
                return redirect("register_user")
        else:
            return render(request, "authenticate/register_user.html", {
                "form": form
            })
    else:
        messages.success(request, ("ページは管理人のみがアクセスできます。"))
        return redirect("login_user")

@login_required(login_url='/login_user/')
def update_profile(request, profile_id):
    if request.user.is_superuser:
        if request.user.is_authenticated:
            profile = Profile.objects.get(id=profile_id)
            form = UserProfileForm(request.POST or None, instance=profile)
            if form.is_valid():
                form.save()
                messages.success(request, "プロフィールを更新しました。")
                return redirect("profile_list")
            return render(request, "update_profile.html", {"form": form , "profile": profile })
        else:
            messages.success(request, "ログインしてください。")
            return redirect("login_user")
    else:
        messages.success(request, ("ページは管理人のみがアクセスできます。"))
        return redirect("login_user")

@login_required(login_url='/login_user/')
def delete_user(request, user_id):
    if request.user.is_authenticated:
        current_user = Profile.objects.get(user__id=user_id)
        current_user.delete()
        messages.success(request, "プロフィールを削除しました。")
        return redirect("profile_list")
    else:
        messages.success(request, "ログインしてください。")
        return redirect("home")
    
@login_required(login_url='/login_user/')
def profile_list(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.all().order_by('-date_created')
        contract = request.user.profile.contract_type
        if request.method == "POST":
            keyword = request.POST['keyword']
            result_list = Profile.objects.filter(fullname__contains=keyword).order_by('-date_created')
            return render(request, "profile_search_list.html", {"result_list": result_list, "keyword": keyword})
        else:
            return render(request, "profile_list.html", { "profiles": profiles, "contract": contract })
    else:
        return redirect('login_user')

@login_required(login_url='/login_user/')
def schedule(request):
    if request.user.is_authenticated:
        genba_list = Genba.objects.all().order_by('-date_created')
        genbas_today = []
        for genba in genba_list:
            date = datetime.datetime(now.year, now.month, now.day)
            start_date = datetime.datetime(genba.start_date.year, genba.start_date.month, genba.start_date.day)
            end_date = datetime.datetime(genba.end_date.year, genba.end_date.month, genba.end_date.day)
            if start_date <= date <= end_date:
                genbas_today.append(genba)
                if request.user.profile.contract_type == '下請け':
                    for genba in genbas_today:
                        if genba.head_person != request.user.profile or request.user.profile not in genba.attendees.all():
                            genbas_today.remove(genba)
    year = int(now.year)
    month = int(now.month)
    cal = calendar.HTMLCalendar().formatmonth(year, month)
    cal = cal.replace('<td ', '<td width="150" height="150" hover')
    cal = mark_safe(cal)
    if request.user.is_authenticated:
         context = {
            "genba_list": genba_list,
            "genbas_today":genbas_today,
            "year": year,
            "month": month,
            "cal": cal,
        }
         return render(request, "schedule.html", context=context)
    else:
        return redirect('login_user')

@login_required(login_url='/login_user/')
def genba_list(request):   
    if request.user.is_authenticated:
        genba_list = Genba.objects.all().order_by('-date_created')
        genbas = []
        if request.method == "POST":
            keyword = request.POST['keyword']
            result_list = Genba.objects.filter(name__contains=keyword).order_by('-date_created')
            return render(request, "genba_search_list.html", {"result_list": result_list, "keyword": keyword})
        if request.user.profile.contract_type == '下請け':
            for genba in genba_list:
                if genba.head_person == request.user.profile or request.user.profile in genba.attendees.all():
                    genbas.append(genba)
        else:
            genbas = genba_list
    return render(request, "genba_list.html", {"genbas": genbas})

@login_required(login_url='/login_user/')
def profile_genba(request):   
    if request.user.is_authenticated:
        profiles = Profile.objects.all()
        genbas = Genba.objects.all().order_by('-date_created')
    return render(request, "profile_genba.html", {"profiles": profiles, "genbas": genbas})

@login_required(login_url='/login_user/')
def genba_details(request, genba_id):
    if request.user.is_authenticated:
        genba = Genba.objects.get(id=genba_id)
        form = GenbaForm(request.POST or None, instance=genba)
        if form.is_valid():
            form.save()
            messages.success(request, "現場を更新しました。")
            return redirect("genba_list")
        return render(request, "genba_details.html", {"form": form , "genba": genba })
    else:
        messages.success(request, "ログインしてください。")
        return redirect("login_user")

@login_required(login_url='/login_user/')
def add_genba(request):
    form = GenbaForm()
    if request.method == "POST":
        form = GenbaForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("現場を追加しました。"))
            return redirect("genba_list")
        else:
            messages.success(request, ("再度お試しください。"))
            return redirect("genba_list")
    else:
        return render(request, "add_genba.html", {
            "form": form
        })

@login_required(login_url='/login_user/')
def delete_genba(request, genba_id):
    if request.user.is_authenticated:
        current_genba = Genba.objects.get(id=genba_id)
        current_genba.delete()
        messages.success(request, "現場を削除しました。")
        return redirect("genba_list")
    else:
        messages.success(request, "ログインしてください。")
        return redirect("login_user")

@login_required(login_url='/login_user/')
def report_list(request):
    if request.user.is_authenticated:
        reports_list = DailyReport.objects.all().order_by('-date_created')
        reports = []
        if request.method == "POST":
            keyword = request.POST['keyword']
            result_list = DailyReport.objects.filter(date_created__contains=keyword).order_by('-date_created')
            return render(request, "report_search_list.html", {"result_list": result_list, "keyword": keyword})
        if request.user.profile.contract_type == '下請け':
            for report in reports_list:
                if report.genba.head_person == request.user.profile or request.user.profile in report.genba.attendees.all():
                    reports.append(report)
        else:
            reports = reports_list
    return render(request, "report_list.html", { 'reports': reports })

@login_required(login_url='/login_user/')
def export_searched(request, keyword):
    if request.user.is_authenticated:
        result_list = DailyReport.objects.filter(date_created__contains=keyword).order_by('-date_created')
        f = "現場毎作業日報" + "_" + keyword + ".csv"
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        filename = urllib.parse.quote((f).encode('utf-8'))
        response['Content-Disposition'] = f'attachment; filename*=UTF-8\'\'{filename}'
        writer = csv.writer(response)
        print(result_list)
        if result_list:
            writer.writerow(["作成日", "作業日", "作成者", "現場名", "取引先", "建退共", "作業員","人数", "シフト", "場所", "開始時間", "終了時間", "休憩時間", "走行距離数", "高速道路乗り", "高速道路降り", "高速支払い方法", "駐車場料金", "宿泊料金", "その他支払い", "建替人", "作業内容", "連絡事項"])
            for report in result_list:
                attendees = []
                for a in report.workers.all():
                    attendees.append(a.fullname)
                if report.kentaikyo:
                    writer.writerow([report.date_created.strftime("%Y/%m/%d"), report.working_date, report.created_by, report.genba.name, report.genba.client, "有", ' '.join([a for a in attendees]), len(attendees), report.shift, report.genba.address, report.start_time, report.end_time, report.break_time, report.distance, report.highway_start, report.highway_end, report.highway_payment, report.parking, report.hotel, f"{report.other_payment} {report.other_payment_amount}", report.paid_by, report.daily_details, report.daily_note ])
                else:
                    writer.writerow([report.date_created.strftime("%Y/%m/%d"), report.working_date, report.created_by, report.genba.name, report.genba.client, "無", ' '.join([a for a in attendees]), len(attendees), report.shift, report.genba.address, report.start_time, report.end_time, report.break_time, report.distance, report.highway_start, report.highway_end, report.highway_payment, report.parking, report.hotel, f"{report.other_payment} {report.other_payment_amount}", report.paid_by, report.daily_details, report.daily_note ])
            return response
        else:
            messages.success(request, "データがありません。")
            return redirect("report_list")

@login_required(login_url='/login_user/')
def add_report(request):
    form = DailyReportForm()
    if request.method == "POST":
        form = DailyReportForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, ("作業日報を追加しました。"))
            return redirect("report_list")
        else:
            messages.success(request, ("再度お試しください。"))
            return redirect("report_list")
    else:
        return render(request, "add_report.html", {
            "form": form
        })
    
@login_required(login_url='/login_user/')
def report_details(request, report_id):
    if request.user.is_authenticated:
        report = DailyReport.objects.get(id=report_id)
        form = DailyReportForm(request.POST or None, instance=report)
        if form.is_valid():
            form.save()
            messages.success(request, "作業日報を更新しました。")
            return redirect("report_list")
        return render(request, "report_details.html", {"form": form , "report": report })
    else:
        messages.success(request, "ログインしてください。")
        return redirect("login_user")