from django.contrib import admin
from django.db import models
from django.forms import Textarea  # to override field in admin django

# Register your models here.

from blog.models import PostCategory, Post, Comment


# to create admin model

@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    search_fields = ['name', 'title']  # to add auto-completion search field on category post


@admin.register(Post)  # to associate to model Post
class PostAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'category',
                    'published',
                    'date',
                    'comments_count',
                    )

    list_filter = (
        'category__name',
        'published'
    )

    #  to make autocompletion

    autocomplete_fields = ['category', ]

    #  to override a widget in django admin
    formfield_overrides = {
        models.TextField: {"widget": Textarea(attrs={'rows': 20, 'cols': 90})},
    }

    # comment_count is not a field of the Post model then we crate a function to get it
    def comments_count(self, obj):
        return Comment.objects.filter(post=obj).count()

    # name to print in admin site
    comments_count.short_description = 'Comments'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post',
                    'author_name',
                    'text',
                    'status',
                    'moderation_text',
                    'created_at',
                    )
    list_editable = ('status',
                     'moderation_text',)
    list_filter = ('status',)
    #  to add search bare to comment view
    search_fields = ['post__title', 'author_name']
