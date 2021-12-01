from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.hashers import check_password

from . import models
from .models import User

class LoginForm(forms.Form):

    user_id = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "ID"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))

    def clean(self):
        user_id = self.cleaned_data.get("user_id")
        password = self.cleaned_data.get("password")
        print(user_id,password)
        try:
            user = models.User.objects.get(user_id=user_id)
            print(user.password)
            if check_password(password,user.password):
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is wrong"))
        except models.User.DoesNotExist:
            self.add_error("user_id", forms.ValidationError("User does not exist"))

class SignUpForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ("user_id",
                  "password",
                  "password_check",
                  "name",
                  "height",
                  "weight",
                  "age_category",
                  "gender",
                  "activity")
        widgets = {
            "user_id": forms.TextInput(attrs={"placeholder": "ID"}),
            "name": forms.TextInput(attrs={"placeholder": "이름"}),
            "height": forms.TextInput(attrs={"placeholder": "cm" }),
            "weight": forms.TextInput(attrs={"placeholder": "kg"}),
            "age_category": forms.Select(choices=models.User.AGE_CHOICES, attrs={'class': 'form-select'}),
            "gender": forms.Select(choices=models.User.GENDER_CHOICES, attrs={'class': 'form-select'}),
            "activity": forms.Select(choices=models.User.ACTIVITY_CHOISES, attrs={'class': 'form-select'}),
        }

    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password"}))
    password_check = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password confirm"}))

    def clean(self):  # 요청파라미터 값들 조회
        cleaned_data = super().clean() # dictionary 반환.
        password = cleaned_data.get('password')
        password_check = cleaned_data.get('password_check') #password 중복체크
        if password != password_check:
            self.add_error('password', '비밀번호가 일치하지 않습니다.')
            self.add_error('password_check', '비밀번호가 일치하지 않습니다.')

class UserUpdateForm(SignUpForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)

        self.fields['user_id'].disabled = True
        self.fields['name'].disabled = True

class UserChangeForm(forms.ModelForm):
    # 비밀번호 변경 폼
    password = ReadOnlyPasswordHashField(
        label='Password(암호화)'
    )

    class Meta:
        model = User
        fields = ("user_id",
                  "password",
                  "name",
                  "height",
                  "weight",
                  "age_category",
                  "gender",
                  "activity",
                  "n_code",)

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]