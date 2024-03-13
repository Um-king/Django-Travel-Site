from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import (
    LoginView,
    LogoutView,
    )
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from django.contrib import messages


import openai
from django.conf import settings

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'register/signup.html'
    success_url = reverse_lazy('post_list')  # 사용자를 리디렉션할 URL

    def form_valid(self, form):
        # User 객체를 생성하고 데이터베이스에 저장합니다.
        user = form.save()
        
        # authenticate 함수를 사용하여 사용자를 인증합니다.
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')  # UserCreationForm은 password1 필드를 사용합니다.
        user = authenticate(username=username, password=password)
        
        # user 객체가 유효하면 로그인 처리를 합니다.
        if user is not None:
            login(self.request, user)
            # 로그인 후 사용자를 success_url로 리디렉션합니다.
            return super().form_valid(form)
        else:
            # 인증에 실패한 경우 에러를 추가하고 폼 유효성 검사에 실패한 것으로 처리합니다.
            form.add_error(None, "Authentication failed.")
            return self.form_invalid(form)


class UserLoginView(LoginView):
    template_name = 'register/login.html'
    redirect_authenticated_user = True  # 이미 인증된 사용자는 success_url로 리디렉션합니다.

    def get_success_url(self):
        return reverse_lazy('post_list')  # 'user_profile'은 로그인 성공 후 리디렉션할 URL 이름입니다.

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # OpenAI API를 사용하여 사용자의 인사말 생성
    #     openai.api_key = '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'  # API 키를 직접 코드에 넣는 것은 보안상 좋지 않습니다. 환경 변수 등을 사용하세요.
    #     response = openai.ChatCompletion.create(
    #         model="gpt-3.5-turbo",
    #         messages=[
    #             {'role': 'user', 'content': "안녕"}
    #         ]
    #     )

    #     # 응답에서 메시지 내용에 접근하기
    #     greeting = response.choices[0].message['content'].strip()
    #     print(greeting)

    #     return context
        

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('user_login')


@login_required # 로그인이 된 사용자만 유저 프로필을 볼 수 있도록
def user_profile(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            old_password = request.user.password  # 현재 비밀번호 저장
            form.save()
            new_password = form.cleaned_data.get('password1')  # 변경된 비밀번호
            if new_password and old_password != new_password:
                # 비밀번호가 변경되었는지 확인
                user = authenticate(request, username=request.user.username, password=new_password)
                if user is not None:
                    login(request, user)  # 사용자를 로그인 상태로 만듬
            messages.success(request, '프로필이 성공적으로 업데이트 되었습니다.')
            return redirect('user_profile')
    else:
        form = CustomUserUpdateForm(instance=request.user)
    return render(request, 'register/user_profile.html', {'form': form})


user_signup = SignUpView.as_view()
user_login = UserLoginView.as_view()
user_logout = UserLogoutView.as_view()


