from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Profile(models.Model):
    CONTRACT_TYPES = (
        ('下請け', '下請け'),
        ('正社員', '正社員'),
        ('管理', '管理'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contract_type = models.CharField("雇用形態", max_length=50, choices=CONTRACT_TYPES, default='正社員')
    fullname = models.CharField("お名前", max_length=20, blank=True)
    phone = models.CharField("携帯電話", max_length=20, blank=True)
    note = models.CharField("備考", max_length=500, blank=True)
    is_active = models.BooleanField("現役中", default=True)
    date_created = models.DateTimeField("作成日", auto_now_add=True)
    updated_at = models.DateTimeField("更新日", auto_now=True)

    def __str__(self):
        return f"{self.fullname}"
    

def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()

post_save.connect(create_profile, sender=User)

class Genba(models.Model):
    COLORS = (
        ('#808080', '灰色'),
        ('#ff6961', '赤色'),
        ('#ffb480', '橙色'),
        ('#f8f38d', '黄色'),
        ('#42d6a4', '緑色'),
        ('#08cad1', '水色'),
        ('#59adf6', '青色'),
        ('#9d94ff', '紫色'),
        ('#c780e8', '桃色'),
    )
    head_person = models.ForeignKey(Profile, related_name="head_person", on_delete=models.CASCADE, null=True)
    attendees = models.ManyToManyField(Profile, related_name="attendees", blank=True)
    name = models.CharField("現場", max_length=255)
    client = models.CharField("取引先", max_length=255)
    address = models.CharField("住所", max_length=255)
    color = models.CharField("現場色", max_length=30, choices=COLORS)
    job_description = models.CharField("作業内容", max_length=255, blank=True, null=True)
    note = models.CharField("備考", max_length=255, blank=True, null=True)
    start_date = models.DateTimeField("作業開始日")
    end_date = models.DateTimeField("作業終了日")
    finished = models.BooleanField("終了", default=False)
    date_created = models.DateTimeField("作成日", auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.client}"
    
    @property
    def Is_past(self):
        today = date.today()
        if self.end_date.date() < today:
            text = "Past"
        else:
            text = "Future"
        return text

class Notification(models.Model):
    author = models.ForeignKey(User, related_name="notification", on_delete=models.CASCADE)
    content = models.CharField("内容", max_length=500)
    date_created = models.DateTimeField("作成日", auto_now_add=True)
    
    def __str__(self):
        return f"{self.content} - {self.author} - {self.created_at}"

class DailyReport(models.Model):
    PAYMENT_TYPES = (
        ('現金','現金'),
        ('カード', 'カード'),
        ('電子マネー', '電子マネー'),
        ('会社ETC', '会社ETC'),
        ('無', '無'),
        )
    DAY_OR_NIGHT = (
        ('日勤','日勤'),
        ('夜勤', '夜勤'),
        )
    SELECT_TYPES = (
        ('請負','請負'),
        ('常傭', '常傭'),
    )
    genba = models.ForeignKey(Genba, related_name="genba", on_delete=models.CASCADE)
    workers = models.ManyToManyField(Profile, related_name="workers", blank=True)
    distance = models.CharField("距離", max_length=10)
    highway_start = models.CharField("高速乗り", max_length=100, blank=True)
    highway_end = models.CharField("高速降り", max_length=100, blank=True)
    highway_payment = models.CharField("高速料金", max_length=50, choices=PAYMENT_TYPES, blank=True)
    select_types = models.CharField("請負乗用", max_length=50, choices=SELECT_TYPES, blank=True)
    parking = models.CharField("駐車料金", max_length=100, blank=True)
    hotel = models.CharField("宿泊料金", max_length=100, blank=True)
    paid_by = models.ForeignKey(Profile, related_name="paid_by", on_delete=models.CASCADE, null=True, blank=True)
    other_payment = models.CharField("その他支払い", max_length=100, blank=True)
    other_payment_amount = models.CharField("その他支払い金額", max_length=100, blank=True)
    daily_details = models.CharField("作業内容", max_length=500, blank=True)
    shift = models.CharField("日勤夜勤", max_length=50, choices=DAY_OR_NIGHT, default='日勤')
    daily_note = models.CharField("備考", max_length=500, blank=True)
    date_created = models.DateTimeField("作成日", auto_now_add=True)
    created_by = models.ForeignKey(Profile, related_name="created_by", on_delete=models.CASCADE, null=True, blank=True)
    working_date = models.DateField("作業日", blank=True, null=True)
    kentaikyo = models.BooleanField("建退共", default=False)
    start_time = models.TimeField('作業開始時間')
    end_time = models.TimeField('作業終了時間')
    break_time = models.CharField("休憩時間", max_length=10, blank=True)

    @property
    def Is_past(self):
        today = date.today()
        if self.date_created.date() < today:
            text = "Past"
        else:
            text = "Future"
        return text

    def __str__(self):
        return f"{self.genba}"
