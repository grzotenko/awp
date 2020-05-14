from django.shortcuts import render
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from enter.models import *
from main.models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.views.generic import View
from datetime import datetime, date, timedelta
from enter.views import calculateTimeEnter, calculateSalary, toFixed
from arm.settings import TZL
from daycalendar.models import *
from .forms import RFPAuthForm
from .models import *
# Create your views here.
class addReserved(FormView):
    form_class = AuthenticationForm
    template_name = "auth.html"
    success_url = "/management/addreserved/"
    def get(self, request,adminname):
        context = {"form": addReserved()}
        return self.render_to_response(self.get_context_data())
    def post(self, request,adminname):
        userP = request.POST['username']
        passP = request.POST['password']
        if userP == adminname:
            return HttpResponseRedirect("/management/addreserved/" + adminname)
        user = authenticate(username=userP, password=passP)
        if user is not None:
            if user.is_active:
                if request.user.groups.filter(name='Админ').exists():
                    prof = Profile.objects.get(user=user)
                    prof.enter = calculateTimeEnter(prof)
                    prof.reserved = True
                    prof.save()
                    return HttpResponseRedirect("/session/")
                elif request.user.groups.filter(name='Кладовщик').exists():
                    return HttpResponseRedirect("/warehouse/")
                else:
                    return HttpResponseRedirect("/management/")
            else:
                return self.render_to_response(self.get_context_data())
        else:
            self.get_context_data()['form'].error_messages[
                'invalid_login'] = "Проверьте корректность введенных логина и пароля!"
            return self.render_to_response(self.get_context_data())

def exitAll(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect("/")
    admin = Profile.objects.get(user=request.user)
    datetimeTZL = datetime.now(TZL)
    setting = Setting.objects.first()
    startDate = date(admin.enter.astimezone(TZL).year, admin.enter.astimezone(TZL).month, admin.enter.astimezone(TZL).day)
    endDatetime = datetimeTZL.replace(hour=setting.end.hour, minute=setting.end.minute, second=0)
    weekends = Weekend.objects.filter(date=startDate + timedelta(days=1))
    if weekends.count() > 0:
        endDatetime = datetimeTZL.replace(hour=setting.weekend.hour, minute=setting.weekend.minute, second=0)
    if endDatetime < datetimeTZL.replace(hour=setting.start.hour, minute=setting.start.minute, second=0):
        endDatetime += timedelta(days=1)

    if admin.user.groups.filter(name='Админ').exists():
        salary = UserSalary.objects.create(user=admin, record_type="Рабочая смена",
                                           start=admin.enter.astimezone(TZL),
                                           end=None)
        calculateSalary(salary, endDatetime)
    admin.save()
    if Profile.objects.filter(reserved=True).count() > 0:
        res_object = Profile.objects.get(reserved=True)
        startDate = date(res_object.enter.astimezone(TZL).year, res_object.enter.astimezone(TZL).month,
                         res_object.enter.astimezone(TZL).day)

        if request.user.groups.filter(name='Админ').exists():
            salary = UserSalary.objects.create(user=res_object, record_type="Рабочая смена",
                                               start=res_object.enter.astimezone(TZL),
                                               end=None)
            calculateSalary(salary, endDatetime)
        res_object.reserved = False
        res_object.save()
    context = reportCalculate(admin)
    logout(request)
    return render(request, "report.html", context)

def reportCalculate(profile):
    dictionary = {}
    datetimeTZL = datetime.now(TZL)

    setting = Setting.objects.first()
    if datetimeTZL.time() < setting.start:
        cashYesterday = list(CashPay.objects.filter(is_payed=False,
                                                    time__date=datetimeTZL.date() - timedelta(
                                                        days=1)).filter(time__time__gt=setting.start))
        cashToday = list(CashPay.objects.filter(is_payed=False, time__date=datetimeTZL.date()))
        cashToday += cashYesterday
        cardYesterday = list(CardPay.objects.filter(is_payed=False,
                                                    time__date=datetimeTZL.date() - timedelta(
                                                        days=1)).filter(time__time__gt=setting.start))
        cardToday = list(CardPay.objects.filter(is_payed=False, time__date=datetimeTZL.date()))
        cardToday += cardYesterday
        listSes = list(Session.objects.filter(end_dt__date=datetimeTZL.date()))
        listSes += list(Session.objects.filter(end_dt__date=datetimeTZL.date() - timedelta(days=1),
                                               end_dt__time__gt=setting.start))
        listZP = UserSalary.objects.filter(
            Q(end__date=datetimeTZL.date()) | Q(end__date=datetimeTZL.date() - timedelta(days=1),
                                                   end__time__gt=setting.start))
    else:
        cardToday = list(
            CardPay.objects.filter(is_payed=False, time__date=datetimeTZL.date(), time__time__gt=setting.start))
        cashToday = list(
            CashPay.objects.filter(is_payed=False, time__date=datetimeTZL.date(), time__time__gt=setting.start))
        listSes = list(Session.objects.filter(end_dt__date=datetimeTZL.date(), end_dt__time__gte=setting.start))
        listZP = UserSalary.objects.filter(end__date=datetimeTZL.date(), end__time__gt=setting.start)
    _listZP = dict()
    for l in listZP:
        _listZP[l.user.user.username] = 0
    cashMoney = 0
    for cash in cashToday:
        cash.is_payed = True
        cash.save()
        cashMoney += cash.amount
    cardMoney = 0
    for card in cardToday:
        card.is_payed = True
        card.save()
        cardMoney += card.amount
    if cashMoney + cardMoney > 0:
        revenue = Orders.objects.create(admin=profile, date=datetimeTZL, amount=cashMoney + cardMoney,
                                        name=TypeOfMO.objects.get(
                                            moneyoper=MoneyOperations.objects.get(is_revenue=True)),
                                        comment="Нал.: " + str(cashMoney) + " руб., Картой: " + str(
                                            cardMoney) + " руб.")
        if datetimeTZL.time() < setting.start:
            revenue.date -= timedelta(days=1)
            revenue.save()
    for s in listSes:
        price = 0
        if s.cash is not None and s.cash.is_usersalary is False:
            price += s.cash.amount
            s.cash.is_usersalary = True
            s.cash.save()
        if s.card is not None and s.card.is_usersalary is False:
            price += s.card.amount
            s.card.is_usersalary = True
            s.card.save()
        admins = listZP.filter(start__lte=s.end_dt, end__gte=s.start_dt)
        lenAdmins = admins.count()
        for admin in admins:
            _listZP[admin.user.user.username] = _listZP.get(admin.user.user.username) + (
                        price * (admin.user.procent / 100)) / lenAdmins
    userReportList = ''
    for admin in listZP.distinct('user'):
        admin.payedProcent = int(_listZP.get(admin.user.user.username))
        admin.save()
        userReportList += admin.user.user.username + ' - ' + str(admin.amount) + ' ч., '
    userReportList = userReportList[:-2]
    dictionary["card"] = cardMoney
    dictionary["cash"] = cashMoney
    dictionary["full"] = cashMoney + cardMoney
    dictionary["ses"] = listSes
    dictionary["admins"] = userReportList
    return dictionary
class reportAll(View):
    initial = {'key': 'value'}
    template_name = 'report.html'

    def get(self, request, *args, **kwargs):
        prof_object = Profile.objects.get(user=User.objects.get(username=request.user))
        context = reportCalculate(prof_object)
        # logout(request)
        return render(request, self.template_name, context)


class exitMenu(View):
    initial = {'key': 'value'}
    template_name = 'exit.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        context = {}
        # header.html
        resAdm = Profile.objects.filter(reserved=True).first()
        context["resAdm"] = "" if resAdm is None else "(" + str(resAdm.user.username) + ")"

        return render(request, self.template_name, context)

def removeReserved(request):
    res_object = Profile.objects.get(reserved=True)
    if request.user.groups.filter(name='Админ').exists():
        salary = UserSalary.objects.create(user=res_object, record_type="Рабочая смена",
                                             start=res_object.enter.astimezone(TZL),
                                             end=None)
        datetimeTZL = datetime.now(TZL)
        setting = Setting.objects.first()
        startDate = date(salary.start.year, salary.start.month, salary.start.day)
        endDatetime = datetimeTZL.replace(hour=setting.end.hour, minute=setting.end.minute, second=0)
        weekends = Weekend.objects.filter(date = startDate+timedelta(days=1))
        if weekends.count() > 0:
            endDatetime = datetimeTZL.replace(hour=setting.weekend.hour, minute=setting.weekend.minute, second=0)
        if endDatetime < datetimeTZL.replace(hour=setting.start.hour, minute=setting.start.minute, second=0):
            endDatetime += timedelta(days=1)
        calculateSalary(salary, endDatetime)
    res_object.reserved = False
    res_object.save()
    return HttpResponseRedirect("/session/")

class transferAdmin(FormView):
    form_class = RFPAuthForm
    template_name = "transfer.html"
    success_url = "/management/transfer/<str:adminname>/"
    def get(self, request,adminname):
        context = {"form": transferAdmin()}
        return self.render_to_response(self.get_context_data())
    def post(self, request,adminname):
        userP = request.POST['username']
        passP = request.POST['password']
        timeEndTr = request.POST['transferTime']
        if userP == adminname:
            return HttpResponseRedirect("/management/transfer/" + adminname)
        shift = Setting.objects.first()
        datetimeEndTr = datetime.now(TZL).replace(hour=int(timeEndTr.split(":")[0]), minute=int(timeEndTr.split(":")[1]), second=0)
        prof_object = Profile.objects.get(user=User.objects.get(username=adminname))
        obj = UserSalary.objects.create(user=prof_object,
                                        record_type="Рабочая смена",
                                        start=prof_object.enter.astimezone(TZL),
                                        end=datetimeEndTr)
        dts = obj.start.astimezone(TZL)
        e_m = obj.end.minute / 60
        toFixed(e_m, 2)
        s_m = dts.minute / 60
        toFixed(s_m, 2)
        e_h = obj.end.hour + e_m
        s_h = dts.hour + s_m
        obj.amount = e_h - s_h
        if obj.amount < 0:
            obj.amount = 24 + obj.amount
        obj.base = obj.user.base * obj.amount
        obj.bonus = obj.user.bonus * obj.amount
        obj.save()
        logout(request)
        user = authenticate(username=userP, password=passP)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.groups.filter(name='Админ').exists():
                    prof = Profile.objects.get(user=user)
                    prof.enter = calculateTimeEnter(prof)
                    prof.save()
                    return HttpResponseRedirect("/session/")
                elif user.groups.filter(name='Кладовщик').exists():
                    return HttpResponseRedirect("/warehouse/")
                else:
                    return HttpResponseRedirect("/management/")
            else:
                return self.render_to_response(self.get_context_data())
        else:
            self.get_context_data()['form'].error_messages[
                'invalid_login'] = "Проверьте корректность введенных логина и пароля!"
            return self.render_to_response(self.get_context_data())

class MainManagement(View):
    initial = {'key': 'value'}
    template_name = 'schedule.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        context = {}
        # header.html
        resAdm = Profile.objects.filter(reserved=True).first()
        context["resAdm"] = "" if resAdm is None else "(" + str(resAdm.user.username) + ")"

        #schedule.html
        thisUser = Profile.objects.get(user = User.objects.get(username = request.user))
        planM = CurrentPlan.objects.filter(type="M")
        startHoliday = datetime.today() + timedelta(
            days=(datetime.today().weekday() - 2 * (datetime.today().weekday()) + 1))
        endHoliday = datetime.today() + timedelta(days=(7 - datetime.today().weekday()))
        fullHolidays = Weekend.objects.filter(date__gte=startHoliday).exclude(date__gt=endHoliday)

        for plan in planM:
            if VacantedShifts.objects.filter(type=plan.type, day=plan.day).count() > 0:
                plan.myshift = "vacanted-shift"
            elif plan.profile is not None and thisUser == plan.profile:
                plan.myshift = "my-shift"

        planE = CurrentPlan.objects.filter(type="E")
        i = 0
        for plan in planE:
            plan.isPreHoliday = True if fullHolidays.filter(date=startHoliday + timedelta(days=i)).count() > 0 else False
            if VacantedShifts.objects.filter(type=plan.type, day=plan.day).count() > 0:
                plan.myshift = "vacanted-shift"
            elif plan.profile is not None and thisUser == plan.profile:
                plan.myshift = "my-shift"
            i += 1

        planR = CurrentPlan.objects.filter(type="R")
        i = 0
        for plan in planR:
            plan.isPreHoliday = True if fullHolidays.filter(
                date=startHoliday + timedelta(days=i)).count() > 0 else False
            if VacantedShifts.objects.filter(type=plan.type, day=plan.day).count() > 0:
                plan.myshift = "vacanted-shift"
            elif plan.profile is not None and thisUser == plan.profile:
                plan.myshift = "my-shift"
            i += 1

        context['isSunday'] = False if FuturePlan.objects.first().profile is None else True
        context['planM'] = planM
        context['planE'] = planE
        context['planR'] = planR
        context['weekendTime'] = Setting.objects.first().weekend

        context['prefsM'] = Preferences.objects.filter(type="M", profile=thisUser).order_by("day")
        prefsE = Preferences.objects.filter(type="E", profile=thisUser).order_by("day")
        i = 0
        for pref in prefsE:
            pref.isPreHoliday = True if fullHolidays.filter(
                date=startHoliday + timedelta(days=i)).count() > 0 else False
            i += 1
        context['prefsE'] = prefsE

        futureE = FuturePlan.objects.filter(type="E").order_by("day")
        futureR = FuturePlan.objects.filter(type="R").order_by("day")
        startHoliday += timedelta(days=7)
        endHoliday += timedelta(days=7)
        fullHolidays = Weekend.objects.filter(date__gte=startHoliday).exclude(date__gt=endHoliday)

        i = 0
        for plan in futureE:
            plan.isPreHoliday = True if fullHolidays.filter(
                date=startHoliday + timedelta(days=i)).count() > 0 else False
            i += 1
        i = 0
        for plan in futureR:
            plan.isPreHoliday = True if fullHolidays.filter(
                date=startHoliday + timedelta(days=i)).count() > 0 else False
            i += 1

        context['futureM'] = FuturePlan.objects.filter(type="M").order_by("day")
        context['futureE'] = futureE
        context['futureR'] = futureR
        BaseSum, BonusSum, PremiumSum, FineSum = 0, 0, 0, 0
        listSalary = UserSalary.objects.filter(user = thisUser, is_payed = False)
        listPremFine = PremiumFine.objects.filter(user=thisUser, is_payed=False)
        for elem in listSalary:
            BaseSum += elem.base
            BonusSum += elem.bonus
            BonusSum += elem.payedProcent
        for elem in listPremFine:
            if elem.type == "P":
                PremiumSum += elem.amount
                elem.type = 'Премия'
            else:
                FineSum += elem.amount
                elem.type = 'Штраф'
        BonusSum += PremiumSum - FineSum
        if BonusSum < 0:
            BonusSum = 0
        totalRate = BonusSum + BaseSum
        context['BonusSum'] = BonusSum
        context['BaseSum'] = BaseSum
        context['totalSum'] = totalRate
        context['salary'] = listSalary
        context['premium'] = listPremFine

        return render(request, self.template_name, context)

@csrf_exempt
def giveVacant(request):
    if request.POST:
        Free = request.POST['dict'].split(',')[:-1]
        for free in Free:
            parsefree = free.split("-")
            vac = VacantedShifts.objects.create(day=Day.objects.get(id=parsefree[1]), type=parsefree[0],
                                                profile=Profile.objects.get(user=request.user))
            vac.save()
        return JsonResponse({"key": "give"})

@csrf_exempt
def takeVacant(request):
    if request.POST:
        pr = Profile.objects.get(user=request.user)
        Free = request.POST['dict'].split(',')[:-1]
        com = dict()
        c = 0
        for free in Free:
            parsefree = free.split("-")
            vac = VacantedShifts.objects.get(day=Day.objects.get(id=parsefree[1]), type=parsefree[0])
            if parsefree[0] == "E" and CurrentPlan.objects.get(day=Day.objects.get(id=parsefree[1]),
                                                             type="R").profile == pr or parsefree[
                0] == "R" and CurrentPlan.objects.get(day=Day.objects.get(id=parsefree[1]), type="E").profile == pr:
                pass
            else:
                tp = CurrentPlan.objects.get(day=Day.objects.get(id=parsefree[1]), type=parsefree[0])
                tp.profile = pr
                tp.save()
                vac.delete()
                com.update({c: free})
                c += 1
        return JsonResponse({"key": "take", "user": pr.user.username, "com": com, "color": pr.color})

@csrf_exempt
def savePrefs(request):
    if request.POST:
        Nice = request.POST['dict'].split(';')[:-1]
        i = 0
        countMinus = 0
        shift = "M"
        daysAll = Day.objects.all()
        profile = Profile.objects.get(user=User.objects.get(username=request.user))
        prof = Preferences.objects.filter(profile = profile)
        for n in Nice:
            obj = prof.filter(day=daysAll[i], type=shift).first()
            obj.pref = n
            obj.save()
            if n == "-":
                countMinus += 1
            i += 1
            if i == 7:
                shift = "E"
                i = 0
        profile.restB = countMinus
        profile.save()
        return JsonResponse({"key": "save"})
