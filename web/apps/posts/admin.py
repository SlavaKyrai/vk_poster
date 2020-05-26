from django.contrib import admin

# Register your models here.
from apps.posts.models import VKToken, Community, Post

admin.site.register(VKToken)
admin.site.register(Community)
admin.site.register(Post)
