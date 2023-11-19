from django.contrib import admin
from .models import Post
import djanngo.apps# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_at', 'update_at', 'author')
    # fields = ('title', 'body')
    fieldsets = (
        ('Post Information', {

admin.site.register(Post, PostAdmin)

class PostAdminSite(admin.AdminSite):
    site_header = "MY:Admin Panel"


post_site = PostAdminSite(name='Postadmin')
post_site.register(Post, PostAdmin)
