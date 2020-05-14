from django import forms
from django.core.exceptions import ValidationError
from .models import *
from daycalendar.models import Setting
from datetime import datetime
from arm.settings import TZL
class EditBookingForm(forms.ModelForm):
    duration = forms.TimeField(label="Длительность", widget=forms.TimeInput(attrs={'type': 'time','step': 1800, 'min': "00:00", 'max': "24:00"}))
    shift = forms.TimeField(label="Начало смены", widget=forms.TimeInput(attrs={'type': 'time','step': 1800, 'min': "00:00", 'max': "24:00"}))

    def __init__(self, *args, **kwargs):
        super(EditBookingForm, self).__init__(*args, **kwargs)
        dn = datetime.now(TZL)
        delta = datetime(dn.year, dn.month, dn.day, self.initial['time_end'].hour, self.initial['time_end'].minute, 0, tzinfo=TZL) - datetime(
            dn.year, dn.month, dn.day, self.initial['time_start'].hour, self.initial['time_start'].minute, 0, tzinfo=TZL)
        duration = datetime(dn.year, dn.month, dn.day, int(delta.seconds / 3600), int(delta.seconds % 3600 / 60), 0,
                            tzinfo=TZL)
        self.fields['duration'].initial = duration.time()
        self.fields['shift'].initial = Setting.objects.first().start

    class Meta:
        model = Booking
        fields = ('date', 'time_start','time_end','persons','room','discountB', 'tariff','text','name','phone','dep_card','dep_cash','includes','services')
        widgets = {
            'date': forms.SelectDateWidget(attrs={'type': 'date'}),
            'time_start': forms.TimeInput(
                attrs={'type': 'time', 'step': 1800, 'min': "00:00", 'max': "24:00"}),
            'time_end': forms.TimeInput(
                attrs={'type': 'time', 'step': 1800, 'min': "00:00", 'max': "24:00"}),
            'persons': forms.TextInput(attrs={'type': 'number', 'min': 1}),
            'room': forms.Select(attrs={'placeholder': 'Комната'}),
            'tariff': forms.Select(attrs={'placeholder': 'Тариф'}),
            'discountB': forms.Select(attrs={'placeholder': 'Скидка'}),
            'text': forms.TextInput(attrs={'placeholder': 'Комментарий'}),
            'name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон (без +7)'}),
            'dep_cash': forms.NumberInput(attrs={'placeholder': 'Депозит наличными'}),
            'dep_card': forms.NumberInput(attrs={'placeholder': 'Депозит картой'}),
            'services': forms.SelectMultiple(attrs={},),
            'includes': forms.SelectMultiple(attrs={}, ),
        }


class NewBookingForm(forms.ModelForm):
    duration = forms.TimeField(label="Длительность", widget=forms.TimeInput(attrs={'type': 'time','step': 1800, 'min': "00:00", 'max': "24:00"}))
    shift = forms.TimeField(label="Начало смены", widget=forms.TimeInput(attrs={'type': 'time','step': 1800, 'min': "00:00", 'max': "24:00"}))
    includesBook = forms.ModelMultipleChoiceField(IncludeService.objects.all(), label="", required=False, help_text="Бесплатные услуги")
    servicesBook = forms.ModelMultipleChoiceField(AddService.objects.all(), label="", required=False, help_text="Платные услуги")

    def __init__(self, *args, **kwargs):
        super(NewBookingForm, self).__init__(*args, **kwargs)

        self.fields['shift'].initial = Setting.objects.first().start

    class Meta:
        model = Booking
        fields = ('date', 'time_start','time_end','persons','room','discountB', 'tariff','text','name','phone','dep_card','dep_cash','includes','services')
        widgets = {
            'date': forms.SelectDateWidget(attrs={'type': 'date'}),
            'time_start': forms.TimeInput(
                attrs={'type': 'time', 'step': 1800, 'min': "00:00", 'max': "24:00"}),
            'time_end': forms.TimeInput(
                attrs={'type': 'time', 'step': 1800, 'min': "00:00", 'max': "24:00"}),
            'persons': forms.TextInput(attrs={'type': 'number', 'min': 1}),
            'room': forms.Select(attrs={'placeholder': 'Комната'}),
            'tariff': forms.Select(attrs={'placeholder': 'Тариф'}),
            'discountB': forms.Select(attrs={'placeholder': 'Скидка'}),
            'text': forms.TextInput(attrs={'placeholder': 'Комментарий'}),
            'name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефон (без +7)'}),
            'dep_cash': forms.NumberInput(attrs={'placeholder': 'Депозит наличными'}),
            'dep_card': forms.NumberInput(attrs={'placeholder': 'Депозит картой'}),
        }