from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("create/", views.post_create, name="post_create"),
    path("detailPage/", views.post_detail_list, name="post_detail_list"),
    path("<int:pk>/", views.post_detail, name="post_detail"),
    path("<int:pk>/update/", views.post_update, name="post_update"),
    path("<int:pk>/delete/", views.post_delete, name="post_delete"),
    path("predict/", views.predict_view, name="predict_view"),
    path("delete_comment/<int:comment_id>/", views.delete_comment, name="delete_comment"),
    path("update_comment/<int:comment_id>/", views.update_comment, name="update_comment"),
    path("add_reply/<int:comment_id>/", views.add_reply, name="add_reply"),
    path('toggle_favorite/<int:pk>/', views.toggle_favorite, name='toggle_favorite'),
    path('get_ai_response/', views.get_ai_response, name='get_ai_response'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)