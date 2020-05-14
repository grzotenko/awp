from django.db import models
from enter.models import *
from django.utils import timezone
from daycalendar.models import Day
class PremiumFine(models.Model):
    Premium = "P"
    Fine = "F"
    TypeOfPremiumFine = (
        (Premium, "Премия"),
        (Fine, "Штраф"),
    )
    user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="Администратор")
    date = models.DateField(blank=False, verbose_name="Дата", default=timezone.now)
    type = models.CharField(max_length=20, verbose_name="Тип записи", blank=False, choices=TypeOfPremiumFine)
    amount = models.IntegerField(default=0, blank=True, verbose_name="Сумма")
    is_payed = models.BooleanField(default=False, verbose_name="Оплачено")
    comment = models.CharField(max_length=125,default='', verbose_name="Коммент", blank=True, null=True)

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = "Премии/Штрафы"
        verbose_name_plural = "Премии/Штрафы"
class UserSalary(models.Model):
    Shift = "Рабочая смена"
    Overtime = "Сверхурочно"
    TypeOfSalaryRecords = (
        (Shift, "Смена"),
        (Overtime, "Сверхурочно"),
    )
    user = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, blank=True, null=True, verbose_name="Администратор")
    record_type = models.CharField(max_length=20, verbose_name="Тип записи", blank=False, choices=TypeOfSalaryRecords)
    start = models.DateTimeField(blank=True, verbose_name="Время начальное", default=timezone.now)
    end = models.DateTimeField(blank=True, verbose_name="Время конечное", null=True)
    comment = models.CharField(max_length=25,default='', verbose_name="Коммент", blank=True, null=True)
    base = models.DecimalField(verbose_name="Сумма базовая", max_digits=8, decimal_places=2, blank=True, default=0)
    bonus = models.DecimalField(verbose_name="Сумма бонусная", max_digits=8, decimal_places=2, blank=True, default=0)
    amount = models.DecimalField(verbose_name="Количество", max_digits=4, decimal_places=2, blank=True, default=0)
    is_payed = models.BooleanField(default=False, verbose_name="Оплачено")
    payedProcent = models.SmallIntegerField(verbose_name="Невыплаченные деньги", default=0)

    def __str__(self):
        return self.user.user.username + " " + self.record_type


    class Meta:
        verbose_name = "Зарплатное начисление"
        verbose_name_plural = "Зарплатные начисления"

class Weekend(models.Model):
    name = models.CharField(max_length=50, blank=False, verbose_name="Название праздика")
    date = models.DateField(blank=False, verbose_name="Дата")
    def __str__(self):
        return self.name+"  "+str(self.date)
    class Meta:
        verbose_name = "Праздник"
        verbose_name_plural = "Праздники"

class MoneyOperations(models.Model):
    Income = "I"
    Expense = "E"
    TYPEOfoper = (
        (Income, "Приход"),
        (Expense, "Расход")
    )
    type = models.CharField(max_length=10, verbose_name="Тип операции", choices=TYPEOfoper, default="Расход")
    name = models.CharField(default="", verbose_name="Название денежной операции", max_length=40, blank=False)
    is_one = models.BooleanField(default=False, verbose_name="Без подтипов")
    is_hidden = models.BooleanField(default=False, verbose_name="Скрытая операция")
    is_adminpay = models.BooleanField(default=False, verbose_name="Зарплата работников")
    is_readonlyamount = models.BooleanField(default=False, verbose_name="Автоматическое формирование выплаты ордера")
    is_revenue = models.BooleanField(default=False, verbose_name="Выручка")
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Категория Ордеров"
        verbose_name_plural = "Категории Ордеров"

class TypeOfMO(models.Model):
    name =  models.CharField(default="", verbose_name="Подтип операции", max_length=20, blank=False)
    moneyoper = models.ForeignKey(MoneyOperations, on_delete=models.SET_NULL, verbose_name="Категория", null=True)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = "Подкатегория Ордеров"
        verbose_name_plural = "Подкатегории Ордеров"
class Orders(models.Model):
    admin = models.ForeignKey(Profile, on_delete=models.SET_NULL, verbose_name="Админ", null=True, blank=True)
    date = models.DateTimeField(blank=False, verbose_name="Время операции", default=timezone.now)
    amount = models.IntegerField(default=0, blank=True, verbose_name="Сумма")
    comment = models.CharField(default="", verbose_name="Комментарий", max_length=150, blank=True)
    name = models.ForeignKey(TypeOfMO, on_delete=models.SET_NULL, verbose_name="Выберите подтип ордера", null=True, blank=True)
    def __str__(self):
        return self.name.name + " --- id:" +str(self.id)
    class Meta:
        verbose_name = "Ордер"
        verbose_name_plural = "Ордеры"

Morning = "M"
Evening = "E"
Reserve = "R"
TYPEOfShifts = (
    (Morning, "Утренняя"),
    (Reserve, "Резервная"),
    (Evening, "Вечерняя")
)

Nice = "+"
Bad = "-"
Norm = "="
TYPEOfPref = (
    (Nice, "Предпочтительно"),
    (Norm, "Все равно"),
    (Bad, "Нежелательно")
)

class CurrentPlan(models.Model):
    day = models.ForeignKey(Day, on_delete=models.SET_NULL, verbose_name="День", null=True)
    type = models.CharField(max_length=18, verbose_name="Смена", choices=TYPEOfShifts, default="Утренняя")
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, verbose_name="Администратор", null=True, blank=True)
    eveningActivity = models.BooleanField(default=False,  verbose_name="Резервная смена активна")
    def __str__(self):
        try:
            return self.day.day + " " + self.get_type_display() + " " + self.profile.user.username
        except:
            return self.day.day + " " + self.get_type_display() + "---"

    class Meta:
        verbose_name = "Текущий план смен"
        verbose_name_plural = "Текущий план смен"
        ordering = ["day"]

class FuturePlan(models.Model):
    day = models.ForeignKey(Day, on_delete=models.SET_NULL, verbose_name="День", null=True)
    type = models.CharField(max_length=18, verbose_name="Смена", choices=TYPEOfShifts, default="Утренняя")
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, verbose_name="Администратор", null=True, blank=True)
    def __str__(self):
        try:
            return self.day.day + " " + self.get_type_display() + " " + self.profile.user.username
        except:
            return self.day.day + " " + self.get_type_display() + "---"

    class Meta:
        verbose_name = "План смен на следующую неделю"
        verbose_name_plural = "План смен на следующую неделю"
        ordering = ["day"]
class Preferences(models.Model):
    Morning = "M"
    Evening = "E"
    SHORTTYPEOfShifts = (
        (Morning, "Утренняя"),
        (Evening, "Вечерняя")
    )
    day = models.ForeignKey(Day, on_delete=models.SET_NULL, verbose_name="День", null=True)
    type = models.CharField(max_length=10, verbose_name="Смена", choices=SHORTTYPEOfShifts, default="Утренняя")
    pref = models.CharField(max_length=20, verbose_name="Выбор", choices=TYPEOfPref, default="Все равно", blank=True, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, verbose_name="Администратор", null=True, blank=True, related_query_name= "preferences")

    def __str__(self):
        return self.profile.user.username + "-" + self.day.day + self.get_type_display()+ "   " + self.get_pref_display()
    class Meta:
        verbose_name = "Предпочтения"
        verbose_name_plural = "Предпочтения"

class VacantedShifts(models.Model):
    day = models.ForeignKey(Day, on_delete=models.SET_NULL, verbose_name="День", null=True)
    type = models.CharField(max_length=10, verbose_name="Смена", choices=TYPEOfShifts, default="Утренняя")
    profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, verbose_name="Администратор", null=True, blank=True)
    def __str__(self):
        try:
            return self.day.day + " " + self.get_type_display() + " " + self.profile.user.username
        except:
            return self.day.day + " " + self.get_type_display() + "---"

    class Meta:
        verbose_name = "Вакантные смены"
        verbose_name_plural = "Вакантные смены"