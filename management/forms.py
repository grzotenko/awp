from datetime import datetime
from arm.settings import TZL
from daycalendar.models import *
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms.widgets import TimeInput

class RFPAuthForm(AuthenticationForm):
    transferTime = forms.TimeField(widget=TimeInput(attrs={'type': 'time'}), label="Время пересмены:")
    def __init__(self, *args, **kwargs):
        super(RFPAuthForm, self).__init__(*args, **kwargs)
        t_now = datetime.now(TZL)
        t_tra = t_now.replace(hour=Setting.objects.first().transfer.hour,
                              minute=Setting.objects.first().transfer.minute)
        if t_now <= t_tra and (t_tra - t_now).seconds <= 600:
            self.fields['transferTime'].initial = t_tra.time().strftime("%H:%M")
        elif t_now >= t_tra and (t_now - t_tra).seconds <= 600:
            self.fields['transferTime'].initial = t_tra.time().strftime("%H:%M")
        else:
            self.fields['transferTime'].initial = t_now.time().strftime("%H:%M")
