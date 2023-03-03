from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User


class Category(models.Model):
    """Модель категории."""
    name = models.CharField('Название категории', max_length=256)
    slug = models.SlugField(
        'Слаг категории',
        unique=True,
        max_length=50
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель жанра."""
    name = models.CharField('Название жанра', max_length=256)
    slug = models.SlugField(
        'Слаг жанра',
        max_length=50,
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """Модель произведения."""
    name = models.CharField('Название', max_length=256, db_index=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Категория'
    )
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        null=True,
        related_name='titles',
        verbose_name='Жанр'
    )
    year = models.IntegerField('Год публикации')

    class Meta:
        ordering = ['-year']
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return f'{self.name}({self.year})'


class Review(models.Model):
    title = models.ForeignKey(
        Title, related_name='reviews', on_delete=models.CASCADE)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Автор'
    )
    pub_date = models.DateTimeField('Дата отзыва', auto_now_add=True)
    text = models.TextField()
    score = models.IntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(10)],
        error_messages={'required': 'Введите оценку от 1 до 10.'})

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['author', 'title'],
                                    name='unique_author_title')
        ]
        ordering = ['-pub_date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments',
        help_text='Ревью'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ['-pub_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
