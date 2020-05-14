from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from .models import *
from django.views.generic.edit import FormView
from daycalendar.models import *
from main.models import *
from datetime import datetime, date
from arm.settings import TZL
from management.models import *
from management.run import removeChangedPlan, buildChangedPlan
# Create your views here.

class LoginEnterForm(FormView):
    form_class = AuthenticationForm
    template_name = "auth.html"
    success_url = "/"

    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect("/session/")
        else:
            context = {}
            context["form"] = LoginEnterForm()
            return self.render_to_response(self.get_context_data())
    def post(self, request):
        userP=request.POST['username']
        passP=request.POST['password']
        user=authenticate(username=userP, password=passP)
        if user is not None:
            if user.is_active:
                login(request, user)
                setting = Setting.objects.first()
                if setting.is_build is False and date.today().weekday() <= 1:
                    removeChangedPlan()
                    setting.is_build = True
                    setting.save()
                elif setting.is_build and date.today().weekday() >= 5:
                    buildChangedPlan()
                    setting.is_build = False
                    setting.save()
                if request.user.groups.filter(name='Админ').exists():
                    prof = Profile.objects.get(user=user)
                    prof.enter = calculateTimeEnter(prof)
                    prof.save()
                    return HttpResponseRedirect("/session/")
                elif request.user.groups.filter(name='Кладовщик').exists():
                    return HttpResponseRedirect("/warehouse/")
                else:
                    return HttpResponseRedirect("/admins/")
            else:
                return self.render_to_response(self.get_context_data())
        else:
            self.get_context_data()['form'].error_messages['invalid_login'] = "Проверьте корректность введенных логина и пароля!"
            return self.render_to_response(self.get_context_data())

def calculateTimeEnter(admin):
    t_now = datetime.now(TZL)
    setting = Setting.objects.first()
    t_tra = t_now.replace(hour=setting.start.hour,minute=setting.start.minute,second=0)
    if t_now <= t_tra and (t_tra - t_now).seconds <= 600:
        return t_tra
    elif t_now >= t_tra and (t_now - t_tra).seconds <= 600:
        return t_tra
    else:
        return t_now

def toFixed(f: float, n=0):
    a, b = str(f).split('.')
    return '{}.{}{}'.format(a, b[:n], '0'*(n-len(b)))

def calculateSalary(salary, endDatetime):
    if datetime.now(TZL) > endDatetime and len(Session.objects.filter(end_dt__gte=endDatetime)) > 0:
        salary.end = endDatetime
        e_m = salary.end.minute / 60
        toFixed(e_m, 2)
        s_m = salary.start.minute / 60
        toFixed(s_m, 2)
        e = salary.end.astimezone(TZL).hour + e_m
        s = salary.start.astimezone(TZL).hour + s_m
        salary.amount = e - s
        if salary.amount < 0:
            salary.amount = 24 + salary.amount
        salary.base = salary.user.base * salary.amount
        salary.bonus = salary.user.bonus * salary.amount
        object = UserSalary.objects.create(
            user=salary.user,
            record_type="Сверхурочно", start=endDatetime, end=datetime.now(TZL))

        sverhurochno_e_m = object.end.minute / 60
        toFixed(sverhurochno_e_m, 2)
        sverhurochno_s_m = object.start.minute / 60
        toFixed(sverhurochno_s_m, 2)
        sverhurochno_e_h = object.end.astimezone(TZL).hour + sverhurochno_e_m
        sverhurochno_s_h = object.start.hour + sverhurochno_s_m
        object.amount = sverhurochno_e_h - sverhurochno_s_h
        object.base = object.user.base * object.amount * 2
        object.bonus = object.user.bonus * object.amount * 2
        object.save()
    else:
        t_now = datetime.now(TZL)
        t_tra = endDatetime
        if t_now <= t_tra and (t_tra - t_now).seconds <= 300:
            salary.end = t_tra
        elif t_now >= t_tra and (t_now - t_tra).seconds <= 600:
            salary.end = t_tra
        else:
            salary.end = t_now
        dts = salary.start.astimezone(TZL)
        e_m = salary.end.minute / 60
        toFixed(e_m, 2)
        s_m = dts.minute / 60
        toFixed(s_m, 2)
        e_h = salary.end.hour + e_m
        s_h = dts.hour + s_m
        salary.amount = e_h - s_h
        if salary.amount < 0:
            salary.amount = 24 + salary.amount
        salary.base = salary.user.base * salary.amount
        salary.bonus = salary.user.bonus * salary.amount
    salary.save()