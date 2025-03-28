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
    

