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

