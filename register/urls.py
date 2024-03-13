from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

# login, logout 이름 사용 X
# 이런 용어들은 전부 다 장고에 기본으로 들어가 있어서 login, logout 이름으로 사용하지 않는다(user_login, uesr_logout으로 사용한 것처럼)

urlpatterns = [
    path("signup/", views.user_signup, name="user_signup"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("profile/", views.user_profile, name="user_profile"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)