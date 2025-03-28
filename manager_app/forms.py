from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Profile, Genba, DailyReport

class SignUpForm(UserCreationForm):
	class Meta:
		model = User
		fields = ('username', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control w-full p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300'
		self.fields['username'].widget.attrs['placeholder'] = 'ユーザー名'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<ul class="form-text text-muted small"><li>記号、スペースなし</li><li>150文字以下</li></ul>'

		self.fields['password1'].widget.attrs['class'] = 'form-control w-full p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300'
		self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>ユーザー名と一致しない</li><li>8文字以上</li><li>数字のみ不可</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control w-full p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300'
		self.fields['password2'].widget.attrs['placeholder'] = '確認パスワード'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<ul class="form-text text-muted small"><li>再度パスワード入力</li></ul>'
    
class UserProfileForm(forms.ModelForm):
	CHOICE = [
       	('下請け', '下請け'),
        ('正社員', '正社員'),
        ('管理', '管理'),]
	fullname = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control w-1/5 mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder':'お名前スペースなし'}))
	phone = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control w-1/5 mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder':'携帯電話番号: 07012345678'}))
	note = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control w-1/5 mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder':'注意事項'}))
	contract_type = forms.ChoiceField(label="雇用形態", choices=CHOICE, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
	is_active = forms.BooleanField(label="現役中", required=False)

	class Meta:
		model = Profile
		fields = ('fullname', 'phone', 'note', 'contract_type', 'is_active')

class GenbaForm(forms.ModelForm):
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
	head_person = forms.Select(attrs={"class":"form-select mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300"})
	attendees = forms.ModelMultipleChoiceField(label="同行者", queryset=Profile.objects.all(), widget=forms.CheckboxSelectMultiple)
	name = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder': '現場名'}))
	client = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder': '取引先'}))
	address = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder': '場所'}))
	job_description = forms.CharField(label="",required=False, widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', "placeholder": "作業内容"}))
	note = forms.CharField(label="", required=False, widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', "placeholder": "連絡事項"}))
	finished = forms.BooleanField(label="完了", required=False)
	start_date = forms.DateField(label='作業開始日', widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300'}))
	end_date = forms.DateField(label='作業終了日', widget=forms.DateInput(attrs={'type': 'date', 'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300'}))
	color = forms.ChoiceField(label="カレンダー表示色", choices=COLORS, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))

	class Meta:
		model = Genba
		fields = ('head_person', 'attendees', 'name', 'client', 'address', 'job_description','note', 'finished', 'start_date', 'end_date', 'color')
		labels = {
			'head_person':'職長',
			'attendees': '同行者',
		}

class DailyReportForm(forms.ModelForm):
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
	created_by = forms.Select(attrs={"class":"form-select mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300"}),
	genba = forms.Select(attrs={"class":"form-select mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300"}),
	kentaikyo = forms.BooleanField(label="建退共", required=False),
	working_date = forms.DateField(label='作業日', widget=forms.DateInput(attrs={'type': 'date', "class": "mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300"}))
	select_types = forms.ChoiceField(label="請負・乗用", choices=SELECT_TYPES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
	shift = forms.ChoiceField(label="昼夜シフト", choices=DAY_OR_NIGHT, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
	workers = forms.ModelMultipleChoiceField(label="作業員", queryset=Profile.objects.all(), widget=forms.CheckboxSelectMultiple)
	start_time = forms.TimeField(label="作業開始時間", widget=forms.TimeInput(attrs={'type': 'time', 'class': 'mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300'}))
	end_time = forms.TimeField(label="作業終了時間", widget=forms.TimeInput(attrs={'type': 'time','class': 'mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300'}))
	break_time = forms.CharField(label="", max_length=10, required=False, widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder': '休憩時間'}))
	distance = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder':'走行距離数'}))
	highway_start = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder':'高速道路乗ったインター'}))
	highway_end = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder':'高速道路降りたインター'}))
	highway_payment = forms.ChoiceField(label="支払い方法", required=False, choices=PAYMENT_TYPES, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
	parking = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder':'駐車料金'}))
	hotel = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder':'宿泊料金'}))
	other_payment = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder':'その他お支払いもの'}))
	other_payment_amount = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder':'その他お支払い金額'}))
	paid_by = forms.Select(attrs={"class":"form-select mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300", "placeholder": "建替人"}),
	daily_details = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300','placeholder':'作業内容'}))
	daily_note = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder':'連絡事項'}))

	class Meta:
		model = DailyReport
		fields = ('created_by', 'genba', 'kentaikyo', 'working_date', 'select_types', 'shift', 'workers', 'start_time', 'end_time', 'break_time', 'distance', 'highway_start', 'highway_end', 'highway_payment', 'parking', 'hotel', 'other_payment', 'other_payment_amount', 'paid_by', 'daily_details', 'daily_note')
		labels = {
			'created_by':'作成者',
           	'genba':'現場名',
			'paid_by': '建替人',
			'kentaikyo':'建退共',
           }

# class SaunaReservationForm(forms.ModelForm):
# 	COURSE_CHOICE = [
# 		('男性', '男性'),
# 		('女性', '女性'),
# 	],
# 	user =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder': '代表者'})),
# 	num_of_people =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder': '人数'})),
# 	course_selected = forms.ChoiceField(label="ご利用されるコース", choices=COURSE_CHOICE, widget=forms.RadioSelect(attrs={'class': 'form-check-input'}))
# 	date = forms.DateField(label="予約日", widget=forms.TimeInput(attrs={'type': 'date','class': 'mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300'}))
# 	time = forms.TimeField(label="予約時間", widget=forms.TimeInput(attrs={'type': 'time','class': 'mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300'}))
# 	note = forms.CharField(label="", max_length=100, required=False, widget=forms.TextInput(attrs={'class':'form-control mb-4 p-2 bg-gray-50 rounded border border-gray-300 focus:ring-3 focus:ring-blue-300', 'placeholder':'その他ご要望'}))

# 	class Meta:
# 		model = SaunaReservation
# 		fields = ('user', 'num_of_people', 'course_selected', 'date', 'time', 'note')
	