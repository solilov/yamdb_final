from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):
    """ Создаем камстомную модель пользователя
        под нужды проекта. """
    ROLE_ADMIN = 'admin'
    ROLE_MODERATOR = 'moderator'
    ROLE_USER = 'user'

    ROLE_CHOICES = {
        (ROLE_ADMIN, 'админ'),
        (ROLE_MODERATOR, 'модератор'),
        (ROLE_USER, 'юзер'),
    }

    email = models.EmailField('email address', unique=True)
    password = models.CharField('password', max_length=128, blank=True)
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(verbose_name='Роль пользователя', max_length=50,
                            default=ROLE_USER, choices=ROLE_CHOICES)


class Category(models.Model):
    """ Создаем  модель категорий
           под нужды проекта. """
    name = models.CharField(max_length=200, verbose_name='Категория')
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """ Создаем  модель жанров
           под нужды проекта. """
    name = models.CharField(max_length=200, verbose_name='Жанр')
    slug = models.SlugField(unique=True, null=False)

    class Meta:
        ordering = ('name',)
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    """ Создаем  модель тайтлов
           под нужды проекта. """
    name = models.CharField(max_length=200,
                            verbose_name='Название произведения')
    year = models.PositiveSmallIntegerField(
        verbose_name='Название произведения'
    )
    description = models.TextField(verbose_name='Описание',
                                   blank=True)
    genre = models.ManyToManyField(Genre,
                                   blank=True,
                                   related_name='titles',
                                   verbose_name='Жанр')
    category = models.ForeignKey(Category,
                                 on_delete=models.SET_NULL,
                                 blank=True,
                                 null=True,
                                 related_name='titles',
                                 verbose_name='Категория')
    rating = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Названия произведений'

    def __str__(self):
        return self.name


class Review(models.Model):
    """ Создаем  модель отзывов
           под нужды проекта. """
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    score = models.PositiveSmallIntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='Unique'
            )
        ]


class Comment(models.Model):
    """ Создаем модель комментариев
           под нужды проекта. """
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
