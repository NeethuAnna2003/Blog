from django.contrib import admin
from django.utils.html import format_html
from .models import Category, BlogPost, Comment, UserProfile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ('created_at', 'updated_at')
    fields = ('author', 'content', 'created_at', 'updated_at')

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'updated_at', 'get_categories')
    list_filter = ('created_at', 'updated_at', 'categories', 'author')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInline]
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('categories',)

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.categories.all()])
    get_categories.short_description = 'Categories'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_at', 'truncated_content')
    list_filter = ('created_at', 'author')
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at')

    def truncated_content(self, obj):
        return obj.content[:75] + '...' if len(obj.content) > 75 else obj.content
    truncated_content.short_description = 'Content'

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'get_profile_picture')
    search_fields = ('user__username', 'bio')
    readonly_fields = ('created_at',)

    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html('<img src="{}" width="50" height="50" style="border-radius: 50%;" />', obj.profile_picture.url)
        return "No profile picture"
    get_profile_picture.short_description = 'Profile Picture'
