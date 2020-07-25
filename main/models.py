from django.db import models
from enter.fields import ColorField
from datetime import datetime, time
from daycalendar.models import Day
from django.utils import timezone
from django.utils.html import format_html

# Create your models here.
class Room(models.Model):
    name = models.CharField(default="", max_length=50, verbose_name="Названия комнаты", blank=False, unique=True)
    color = ColorField('Цвет комнаты', default='#FF0000')
    font = ColorField('Цвет шрифта', default='#FFFFFF')
    capasity = models.PositiveSmallIntegerField(default=1, verbose_name="Вместимость")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
        ordering = ["id"]
    def colortile(self):
        if self.color:
            return format_html('<div style="background-color: {0}; \
                height: 20px; width: 20px"></div>', self.color)
        return 'пусто'
    colortile.short_description = "Цвет комнаты"
    def colorfont(self):
        if self.color:
            return format_html('<div style="background-color: {0}; \
                height: 20px; width: 20px"></div>', self.font)
        return 'пусто'
    colortile.short_description = "Цвет шрифта"

class AddService(models.Model):
    name = models.CharField(default="", max_length=300, verbose_name="Названия услуг", blank=False, unique=True)
    price = models.PositiveSmallIntegerField(default=0, verbose_name="Стоимость услуги в рублях")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Платная услуга"
        verbose_name_plural = "Платные услуги"

class IncludeService(models.Model):
    name = models.CharField(default="", max_length=300, verbose_name="Названия услуг", blank=False, unique=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Включенная в стоимость услугу"
        verbose_name_plural = "Включенные в стоимость услуги"

class UseService(models.Model):
    add = models.ForeignKey(AddService, blank=True, null=True,verbose_name="Услуга", on_delete=models.SET_NULL)
    count = models.IntegerField(verbose_name="Кол-во", default=1)

    def __str__(self):
        return "SID клиента:  " + str(Session.objects.filter(services=self).first()) + " - " +str(self.add.name)
    class Meta:
        verbose_name = "Оказанная услуга"
        verbose_name_plural = "Оказанные услуги"

class Discount(models.Model):
    days = models.ManyToManyField(Day, blank=True, verbose_name="Дни недели")
    name = models.CharField(default="", max_length=50, verbose_name="Название скидки", blank=False, unique=True)
    multiplier = models.DecimalField(max_digits=3, decimal_places=2, default=1.0, verbose_name="Множитель")
    limit_gt = models.PositiveSmallIntegerField(default=2, verbose_name="Минимальное Кол-во людей")
    limit_lt = models.PositiveSmallIntegerField(default=2, verbose_name="Максимальное Кол-во людей")
    free = models.PositiveSmallIntegerField(default=1, verbose_name="Кол-во людей бесплатно")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Скидки"
        verbose_name_plural = "Скидки"

class Tariff(models.Model):
    TypeTime = "tp"
    TypePlace = "fp"
    TYPEOfTariffs = (
        (TypeTime, "Повременная оплата"),
        (TypePlace, "Фиксированный прайс")
    )

    name = models.CharField(default="", max_length=135, verbose_name="Названия тарифа", blank=False,unique=True)
    type = models.CharField(max_length=25, verbose_name="Тип", blank=False, choices=TYPEOfTariffs, default="Повременная оплата")
    price = models.PositiveSmallIntegerField(default=0, verbose_name="Цена минуты")
    days = models.ManyToManyField(Day, blank=True, verbose_name="Дни недели")
    fix = models.PositiveSmallIntegerField(default=0, verbose_name="Фиксированная цена")
    limit = models.PositiveSmallIntegerField(default=1, verbose_name="Минимальное кол-во людей")
    free = models.PositiveSmallIntegerField(default=0, verbose_name="Кол-во людей бесплатно")
    time = models.TimeField(default=time(), verbose_name="Ограничение по времени", null=True, blank=True)
    discounts = models.ManyToManyField(Discount, blank=True, verbose_name="Возможные скидки при данном тарифе")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы"
class CashPay(models.Model):
    amount = models.IntegerField(default=0, blank=True, verbose_name="Оплата наличными")
    time = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Время оплаты")
    is_payed = models.BooleanField(default=False, verbose_name="Учтено в ордере Выручки")
    is_usersalary = models.BooleanField(default=False, verbose_name="Учтено в зарпалатном начислении")
    def __str__(self):
        try:
            return "SID клиента:  " + str(Session.objects.get(cash = self))+ " = " + str(self.amount)  + " р."
        except:
            return str(self.time)
    class Meta:
        verbose_name = "Оплата наличными"
        verbose_name_plural = "Оплаты наличными"

class CardPay(models.Model):
    amount = models.IntegerField(default=0, blank=True, verbose_name="Оплата картой")
    time = models.DateTimeField(default=datetime.now, blank=True, verbose_name="Время оплаты")
    is_payed = models.BooleanField(default=False, verbose_name="Учтено в ордере Выручки")
    is_usersalary = models.BooleanField(default=False, verbose_name="Учтено в зарпалатном начислении")
    def __str__(self):
        try:
            return "SID клиента:  " + str(Session.objects.get(card = self)) + " = " + str(self.amount) + " р."
        except:
            return str(self.time)
    class Meta:
        verbose_name = "Оплата картой"
        verbose_name_plural = "Оплаты картой"

class Company(models.Model):
    CID = models.IntegerField(verbose_name="CID")
    tariff = models.ForeignKey(Tariff, null=True, on_delete=models.SET_NULL, verbose_name="Тариф")
    discount = models.ForeignKey(Discount, null=True, on_delete=models.SET_NULL, blank=True, verbose_name="Скидка")
    count = models.IntegerField(default=0, blank=True, verbose_name="Общее кол-во человек")
    payed = models.IntegerField(default=0, blank=True, verbose_name="Кол-во оплаченных человек")
    date = models.DateField(blank=False, verbose_name="Дата", default=timezone.now)
    def __str__(self):
        return str(self.CID)
    class Meta:
        verbose_name = "Компания"
        verbose_name_plural = "Компании"

class Session(models.Model):
    SID = models.CharField(verbose_name="SID", max_length=100)
    room = models.ForeignKey(Room, blank=False, null=True,verbose_name="Занятая комната", on_delete=models.SET_NULL)
    start_dt = models.DateTimeField(verbose_name="Начало сеанса", default=timezone.now)
    end_dt = models.DateTimeField(null=True, blank=True, verbose_name="Окончание сеанса")
    sum = models.IntegerField(default=0, null=True, blank=True, verbose_name="Чек-лист")
    is_active = models.BooleanField(default=True, verbose_name="Пользователь активен", blank=False)
    cash = models.ForeignKey(CashPay, blank=True, verbose_name="Наличные", on_delete=models.CASCADE, default=None,null=True)
    card = models.ForeignKey(CardPay, blank=True, verbose_name="Безнал", on_delete=models.CASCADE, default=None,null=True)
    services = models.ManyToManyField(UseService, blank=True, verbose_name="Оказанные услуги")
    text = models.CharField(default="", max_length=1500, verbose_name="Текстовый комментарий", blank=True)
    includes = models.ManyToManyField(IncludeService, blank=True, verbose_name="Включенные в стоимость услуги")
    dep_card = models.IntegerField(default=0, blank=True, verbose_name="Депозит картой")
    dep_cash = models.IntegerField(default=0, blank=True, verbose_name="Депозит наличными")
    owner = models.BooleanField(verbose_name="Особые права при оплате", default=False)
    company = models.ForeignKey(Company, blank=True, null=True,on_delete=models.CASCADE, verbose_name="Компания")
    def __str__(self):
        return str(self.start_dt)[0:16] + "_" + str(self.company.CID) + "_" + str(self.SID)

    class Meta:
        verbose_name = "Сессия"
        verbose_name_plural = "Сессии"
