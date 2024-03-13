from django.contrib import admin
from .models import Post, Tag, Itinerary, Mission, Comment


admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(Itinerary)
admin.site.register(Mission)
admin.site.register(Comment)
