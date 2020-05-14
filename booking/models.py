from django.db import models
from django.utils import timezone
from datetime import datetime, time
from main.models import *
# Create your models here.
class Booking(models.Model):
    date = models.DateField(blank=False, verbose_name="Дата брони", default=timezone.now)
    time_start = models.TimeField(verbose_name="Начало", default=datetime.now)
    time_end = models.TimeField(verbose_name="Окончание", default=datetime.now)
    persons = models.PositiveSmallIntegerField(default=0, verbose_name="Кол-во человек")
    room = models.ForeignKey(Room, blank=True, null=True,on_delete=models.SET_NULL, verbose_name="Занятая комната")
    tariff = models.ForeignKey(Tariff, null=True, on_delete=models.SET_NULL, verbose_name="Тариф")
    discountB = models.ForeignKey(Discount, null=True, on_delete=models.SET_NULL, blank=True, verbose_name="Скидка")
    text = models.CharField(default="", max_length=1500, verbose_name="Текстовый комментарий", blank=True)
    includes = models.ManyToManyField(IncludeService, blank=True, verbose_name="", help_text="Выбранные бесплатные услуги")
    services = models.ManyToManyField(AddService, blank=True,help_text="Выбранные платные услуги",verbose_name="")
    name = models.CharField(default=None, max_length=50, verbose_name="Имя", blank=True)
    phone = models.CharField(default=None, max_length=10, verbose_name="Телефон", blank=True, null=True)
    dep_card = models.IntegerField(default=0, blank=True, verbose_name="Депозит картой")
    dep_cash = models.IntegerField(default=0, blank=True, verbose_name="Депозит наличными")

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"