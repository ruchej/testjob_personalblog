from django.db import models
from config import settings


USER_MODEL = settings.AUTH_USER_MODEL


class Core(models.Model):
    """Общая абстракная модель"""

    class Meta:
        abstract = True

    title = models.CharField("Заголовок", max_length=250, blank=True, null=True)
    description = models.TextField("Описание", blank=True, null=True)
    active = models.BooleanField("Активность объекта", default=True, db_index=True)

    def __str__(self):
        return self.title or ""

    def delete(self, **kwargs):
        if "force" in kwargs:
            super().delete()
        else:
            self.active = False
            self.save()


class PictureManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(active=True)


class Picture(Core):
    class Meta:
        verbose_name = "Картинка"
        verbose_name_plural = "Картинки"

    img = models.ImageField(upload_to="pictures")
    objects = PictureManager()


class Blog(Core):
    """Блог пользоваьедя с названием и описанием"""
    class Meta:
        verbose_name = "Персональный блог"
        verbose_name_plural = "Персональные блоги"

    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="bloger",
        verbose_name="Пользователь",
    )


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class Post(Core):
    """Посты пользователей"""
    class Meta:
        ordering = ("-date_created",)
        verbose_name = "Пост"
        verbose_name_plural = "Посты"

    STATUS_CHOICES = (
        ("draft", "Черновик"),
        ("published", "Опубликовано"),
    )
    slug = models.CharField(max_length=200)
    body = models.TextField("Статья", blank=True, null=True)
    date_created = models.DateTimeField("Дата создания статьи", auto_now_add=True)
    blog = models.ForeignKey(
        Blog,
        verbose_name="Привязан к объекту",
        null=True,
        blank=True,
        related_name="posts",
        on_delete=models.CASCADE,
        db_index=True
    )
    status = models.CharField(
        "Статус",
        max_length=10,
        choices=STATUS_CHOICES,
        default="draft",
    )
    published = PublishedManager()
