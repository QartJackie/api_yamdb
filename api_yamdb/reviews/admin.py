from django.contrib import admin

from reviews.models import Category, Comment, Genre, Title, Review


class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'slug'

    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-Пусто-'


class CommentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'text',
        'pub_date'
    )
    list_display_links = ('text',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-Пусто-'


class GenreAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'slug'
    )
    list_display_links = ('name',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = '-Пусто-'


class TitleAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'name',
        'category',
        'description',
        'year'


    )
    search_fields = ('name', 'description', 'year', 'category', 'get_genre')
    list_filter = ('category', 'year')
    empty_value_display = '-Пусто-'


class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title_id',
        'pub_date',
        'text',
        'score'
    )
    search_fields = ('aurhor', 'text', 'score')
    list_filter = ('pub_date',)
    empty_value_display = '-Пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
