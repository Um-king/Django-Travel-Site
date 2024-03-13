from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic.base import RedirectView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('', RedirectView.as_view(pattern_name='post_list'), name='root'), # RedirectView.as_view: tube의 post_list로 보내주겠다 
    path("post/", include("post.urls")),
    path("register/", include("register.urls"))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)