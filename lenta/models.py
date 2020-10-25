from django.db import models
from config import settings
from blog.models import Blog, Post


USER_MODEL = settings.AUTH_USER_MODEL


class SubscriptionManager(models.Manager):
    def ger_queryset(self):
        return super().get_queryset().filter(signed=True)


class Subscription(models.Model):
    """Подписки пользоватлей на блоги"""
    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"

    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Подписчик",
        db_index=True
    )
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Блог",
    )
    signed = models.BooleanField("Подписан", default=True)
    objects = SubscriptionManager()

    def __str__(self):
        return f"Пользователь {self.user} подписан на {self.blog}"

    def delete(self, **kwargs):
        if "force" in kwargs:
            super().delete()
        else:
            self.signed = False
            self.save()


class SubscriptionPosts(models.Model):
    """Статьи по подписке"""
    class Meta:
        verbose_name = "Статья по подписке"
        verbose_name_plural = "Статьи по подписке"
    
    
    user = models.ForeignKey(
        USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Подписчик",
        db_index=True
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Посты",
    )
    seen = models.BooleanField("Просмотренно", default=False, db_index=True)