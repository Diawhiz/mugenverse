from django.contrib import admin

# Register your models here.
from django_summernote.admin import SummernoteModelAdmin
from .models import Post, Comment, Category

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('title', 'slug', 'status', 'posted_on')
    list_filter = ('status', 'category')
    search_fields = ['title']
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Post, PostAdmin)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)