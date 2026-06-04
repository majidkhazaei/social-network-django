from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Profile


class UserRegisterForm(forms.Form):
    username = forms.CharField(label='نام کاربری')
    email = forms.EmailField(label='ایمیل')
    password = forms.CharField(label='رمز عبور',widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='تکرار رمز عبور',widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('ایمیل قبلا ثبت نام شده است')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username).exists()
        if user:
            raise ValidationError('ایمیل قبلا ثبت نام شده است')
        return username

    def clean(self):
        cd = super().clean()
        p1 = cd.get('password')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('رمز عبور باید یکسان باشد.')


class UserLoginForm(forms.Form):
    username = forms.EmailField(label='نام کاربری(ایمیل)')
    password = forms.CharField(label='رمز عبور', widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class EditUserForm(forms.ModelForm):
    email = forms.EmailField()
    class Meta:
        model = Profile
        fields = ['age', 'address']