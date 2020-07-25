from django import forms
from django.core.exceptions import ValidationError
from .models import *
from datetime import datetime
from arm.settings import TZL
class NewSessionForm(forms.ModelForm):
    includesAll = forms.ModelMultipleChoiceField(IncludeService.objects.all(), label="", required=False)
    includesChange = forms.ModelMultipleChoiceField(IncludeService.objects.all(), required=False, label="")
    servicesAll = forms.ModelMultipleChoiceField(AddService.objects.all(), label="", required=False)
    servicesChange = forms.ModelMultipleChoiceField(AddService.objects.all(), required=False, label="")
    count = forms.IntegerField(label="Количество человек",initial = 1,
                                       widget=forms.TextInput(attrs={'min': 0, 'type': 'number'}))
    tariff = forms.ModelChoiceField(queryset=Tariff.objects.all(), label="Тариф")
    discount = forms.ModelChoiceField(queryset=Discount.objects.all(), label="Скидка", required=False)
    class Meta:
        model = Session
        fields = ('room', 'text','dep_cash','dep_card',)
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Комментарий'}),
            'room': forms.Select(attrs={'placeholder': 'Комната'}),
            'dep_cash': forms.NumberInput(attrs={'placeholder': 'Депозит наличными'}),
            'dep_card': forms.NumberInput(attrs={'placeholder': 'Депозит картой'}),
        }

class EditSessionForm(forms.ModelForm):
    include = forms.ModelChoiceField(IncludeService.objects.all(), label="Бесплатные услуги", required=False)
    service = forms.ModelChoiceField(AddService.objects.all(), label="Платные услуги", required=False)
    class Meta:
        model = Session
        fields = ('room', 'text','dep_cash','dep_card',)
        widgets = {
            'text': forms.TextInput(attrs={'placeholder': 'Комментарий'}),
            'room': forms.Select(attrs={'placeholder': 'Комната'}),
            'dep_cash': forms.NumberInput(attrs={'placeholder': 'Депозит наличными'}),
            'dep_card': forms.NumberInput(attrs={'placeholder': 'Депозит картой'}),
        }






