from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # CustomUser 모델을 임포트합니다.

class CustomUserCreationForm(UserCreationForm):
    nickname = forms.CharField(max_length=30, required=False)
    profile_image = forms.ImageField(required=False)
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser  # User 대신 CustomUser를 참조합니다.
        fields = UserCreationForm.Meta.fields + ('nickname', 'profile_image',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.nickname = self.cleaned_data.get('nickname')
        user.email = self.cleaned_data.get('email')
        if self.cleaned_data.get('profile_image'):
            user.profile_image = self.cleaned_data.get('profile_image')
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])    
        if commit:
            user.save()
        return user

class CustomUserUpdateForm(forms.ModelForm):
    nickname = forms.CharField(max_length=30, required=False)
    profile_image = forms.ImageField(required=False, help_text='프로필 이미지를 업데이트 하려면 선택하세요.')
    password1 = forms.CharField(widget=forms.PasswordInput(), label="새 비밀번호", required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="새 비밀번호 확인", required=False)

    class Meta:
        model = CustomUser
        fields = ['nickname', 'profile_image']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password1')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("비밀번호가 일치하지 않습니다.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        if self.cleaned_data['password1']:
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user