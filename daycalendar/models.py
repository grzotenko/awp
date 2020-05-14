from django.db import models

# Create your models here.
class Day(models.Model):
    day = models.CharField(max_length=15)
    num = models.IntegerField(default=0, verbose_name="Порядковый номер")

    def __str__(self):
        return self.day
    class Meta:
        verbose_name = "Дни недели"
        verbose_name_plural = "Дни недели"

class Setting(models.Model):
    cash_now = models.IntegerField(default=0, blank=True, verbose_name="Сейчас в кассе")
    delete_time = models.PositiveIntegerField(verbose_name="Кол-во минут, при котором можно удалить посетителя",default=10)
    is_print = models.BooleanField(verbose_name="Принтер подключен", default=False)
    network = models.CharField(verbose_name="Network", default="", max_length=50)
    start = models.TimeField(verbose_name="Обычное время начала смены")
    end = models.TimeField(verbose_name="Обычное время конца смены", null=True, default=None)
    weekend = models.TimeField(verbose_name="Предпраздничное время конца смены", null=True, default=None)
    transfer = models.TimeField(verbose_name="Обычное время пересмены", null=True, default=None)
    is_build = models.BooleanField(verbose_name="График построен", default=False)

    def __str__(self):
        return "Настройки"
    class Meta:
        verbose_name = "Настройки"
        verbose_name_plural = "Настройки"