from django.db import models
from .fields import ColorField
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    base = models.PositiveSmallIntegerField(verbose_name="Базовая ставка", default=45)
    bonus = models.PositiveSmallIntegerField(verbose_name="Бонусная ставка", default=25)
    procent = models.SmallIntegerField(verbose_name="Процент от выручки", default=2)
    enter = models.DateTimeField(blank=True, verbose_name="Время входа", null=True, default=None)
    countG = models.IntegerField(verbose_name="Счётчик предпочтительных смен", blank=False, default=0)
    countB = models.IntegerField(verbose_name="Счётчик нежелательных смен", blank=False, default=0)
    restB = models.IntegerField(verbose_name="Осталось нежелательных смен", blank=False, default=0)
    color = ColorField('Цвет админа', default='#FF0000')
    reserved = models.BooleanField(default=False, verbose_name="Работает в резерв")
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def colortile(self):
        if self.color:
            return format_html('<div style="background-color: {0}; \
                height: 20px; width: 20px"></div>', self.color)
        return 'пусто'
    colortile.short_description = "Цвет админа"
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Администратор "
        verbose_name_plural = "Администраторы"