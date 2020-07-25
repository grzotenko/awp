from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone


class Categories(models.Model):
    cat_title = models.CharField(default="", max_length=20, blank=False, verbose_name="Название категории")

    def __str__(self):
        return self.cat_title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Subcategories(models.Model):
    subcat_title = models.CharField(default="", max_length=20, verbose_name="Название подкатегории", blank=False)
    category = models.ForeignKey(Categories, on_delete=models.DO_NOTHING, blank=False, verbose_name="Категория")

    def __str__(self):
        return self.subcat_title

    class Meta:
        verbose_name = "Подкатегория "
        verbose_name_plural = "Подкатегории"


class Goods(models.Model):
    title = models.CharField(default="", max_length=20, verbose_name="Название расходника", blank=False)
    subcat = models.ForeignKey(Subcategories, on_delete=models.DO_NOTHING, blank=False,
                               verbose_name="Подкатегория товара")
    yellow = models.FloatField(default=0, blank=False, verbose_name="Желтый уровень")
    red = models.FloatField(default=0, blank=False, verbose_name="Красный уровень")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"


class Volumes(models.Model):
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, blank=False, verbose_name="Товар")
    volume = models.FloatField(default=0, blank=False, verbose_name="Объем упаковки")
    amount = models.PositiveIntegerField(default=0, blank=False, verbose_name="Кол-во упаковок")


class Costs(models.Model):
    good = models.ForeignKey(Goods, on_delete=models.CASCADE, blank=False, verbose_name="Товар", default=None)
    quantity = models.FloatField(default=0, blank=False, verbose_name="Количество единиц товара")
    price = models.FloatField(default=0, verbose_name="Цена", blank=False)


class WarehouseInOut(models.Model):
    TypeIncome = "Приход"
    TypeOutcome = "Расход"
    TypeOperation = (
        (TypeIncome, "Приход"),
        (TypeOutcome, "Расход"),
    )
    date = models.DateTimeField(default=timezone.now, blank=False, verbose_name="Дата операции")
    users = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=False, verbose_name="User ID")
    type_operations = models.CharField(default="Приход", max_length=20, verbose_name="Тип операции", blank=False,
                                       choices=TypeOperation)
    title_goods = models.ForeignKey(Goods, on_delete=models.DO_NOTHING, blank=False, verbose_name="Товар")
    volume = models.FloatField(default=0, blank=False, verbose_name="Объем упаковки")
    amount = models.FloatField(default=0, blank=False, verbose_name="Кол-во упаковок")
    cost = models.DecimalField(default=0, decimal_places=2, max_digits=8, verbose_name="Потрачено денег")
    comment = models.CharField(default="", max_length=30, verbose_name="Комментарий", blank=True)

    def get_price(self):
        return round((float(self.cost) / (self.amount * self.volume)), 4)

    price = property(get_price)

    def __str__(self):
        return self.type_operations + " " + self.title_goods.title

    class Meta:
        verbose_name = "Движение на складе"
        verbose_name_plural = "Движения на складе"


class WhatsApp(models.Model):
    account_sid = models.CharField(default='', blank=False, max_length=50, verbose_name='SID')
    auth_token = models.CharField(default='', blank=False, max_length=50, verbose_name='Токен')
    send_to = models.CharField(default='', blank=False, max_length=20, verbose_name='Номер получателя')
    send_from = models.CharField(default='', blank=False, max_length=20, verbose_name='Номер отправителя')

    class Meta:
        verbose_name = "WhatsApp"
        verbose_name_plural = "WhatsApp"


def wrhsDict(allC, allS, allG):
    dict = {
        'aC': allC,
        'aS': allS,
        'aG': allG,
    }
    return dict
