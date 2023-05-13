from django.contrib import admin
from .models import Post, Location, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'text',
        'is_published',
        'pub_date',
        'author',
        'location',
        'category',
        'created_at',
    )
    list_editable = ('is_published', 'pub_date')
    search_fields = ('title',)
    list_filter = (
        'author',
        'location',
        'category',
    )
    empty_value_display = 'Планета Земля'


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published', )
    search_fields = ('name', )


class PostInline(admin.StackedInline):
    model = Post
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    inlines = (
        PostInline,
    )
    list_display = (
        'title',
        'description',
        'slug',
        'is_published',
        'created_at',
    )
    list_editable = ('is_published', )
    search_fields = ('title', 'slug', )
    list_filter = ('title', 'slug', )
