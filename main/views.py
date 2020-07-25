from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from enter.models import *
from .forms import NewSessionForm, EditSessionForm
from django.db.models import F
from .models import *
from daycalendar.models import *
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date, timedelta
from arm.settings import TZL
from escpos.printer import Network
from transliterate import translit, get_available_language_codes
from arm.settings import STATIC_ROOT
import os
# import logging
# Create your views here.
class NewSession(View):
    template_name = 'new-session.html'
    def getcontext(self, form):
        context = {}
        form.fields["tariff"].queryset = Tariff.objects.filter(days__num = datetime.now(TZL).weekday())
        form.fields["discount"].queryset = Discount.objects.filter(days__num=datetime.now(TZL).weekday())
        context["form"] = form

        # logging.basicConfig(filename="sample.log", level=logging.INFO)
        # logging.info(Tariff.objects.filter(days__num = datetime.today().weekday()))
        # logging.info(form.base_fields.get("tariff").choices.queryset)
        # logging.info(datetime.today().weekday())
        # logging.info(Day.objects.get(day="Суббота").num)
        # for tariff in Tariff.objects.all():
        #     logging.info(tariff.name)
        #     for day in tariff.days:
        #         logging.info(day.num)
        return context

    def post(self, request, *args, **kwargs):
        newSesForm = NewSessionForm(request.POST)
        if newSesForm.is_valid():
            setting = Setting.objects.first()
            if setting.is_print:
                printer = Network(setting.network)
                listSessions = list()
            if newSesForm.cleaned_data["dep_cash"] > 0:
                simpleCash = newSesForm.cleaned_data["dep_cash"] // newSesForm.cleaned_data["count"]
                addingCash = newSesForm.cleaned_data["dep_cash"] % newSesForm.cleaned_data["count"]
            else:
                simpleCash = 0
                addingCash = 0
            if newSesForm.cleaned_data["dep_cash"] > 0:
                simpleCard = newSesForm.cleaned_data["dep_card"] // newSesForm.cleaned_data["count"]
                addingCard = newSesForm.cleaned_data["dep_card"] % newSesForm.cleaned_data["count"]
            else:
                simpleCard = 0
                addingCard = 0
            prevCompany = Company.objects.filter(date__gte = date.today().replace(day=1)).last()
            prevCompanyID = 0 if prevCompany is None else prevCompany.CID
            room = Room.objects.get(name = newSesForm.cleaned_data["room"])
            tariff = Tariff.objects.get(name = newSesForm.cleaned_data["tariff"])
            discount = None if newSesForm.cleaned_data["discount"] is None else Discount.objects.get(name = newSesForm.cleaned_data["discount"])
            countSessions = newSesForm.cleaned_data["count"]
            counter = countSessions
            countOwners = tariff.free if tariff.type == "fp" else discount.free if discount is not None else 0
            company = Company.objects.create(CID=prevCompanyID+1, count = countSessions, tariff = tariff, discount = discount)
            today = datetime.now(TZL)
            todayMonth = str(today.month) if today.month>=10 else "0"+str(today.month)
            todayDay = str(today.day) if today.day >= 10 else "0" + str(today.day)
            todayCID = str(company.CID) if company.CID >= 100 else "0" + str(company.CID) if company.CID >=10 else "00" + str(company.CID)
            partSID = str(today.year) + todayMonth + todayDay + todayCID
            while counter > 0:
                todaySID = str(counter) if counter >= 10 else "0" + str(counter)
                session = Session.objects.create(SID = partSID+str(todaySID), room=room, company=company)
                if countOwners > 0:
                    session.owner = True
                    session.save()
                    countOwners -= 1
                if counter == countSessions:
                    session.text = newSesForm.cleaned_data["text"]
                    session.dep_cash = simpleCash + addingCash
                    session.dep_card = simpleCard + addingCard
                    for us in newSesForm.cleaned_data["servicesChange"]:
                        useservice = UseService.objects.create(add=AddService.objects.get(name=us))
                        useservice.save()
                        session.services.add(useservice)
                    for ns in newSesForm.cleaned_data["includesChange"]:
                        includeservice = IncludeService.objects.get(name=ns)
                        session.includes.add(includeservice)
                else:
                    session.dep_cash = simpleCash
                    session.dep_card = simpleCard
                session.save()
                if setting.is_print:
                    listSessions.append(session)
                counter -= 1
            if setting.is_print:
                printEnteredTickets(printer, listSessions)
            return HttpResponseRedirect('/session/')
        else:
            context = self.getcontext(newSesForm)
            return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        context = self.getcontext(NewSessionForm())
        return render(request, self.template_name, context)

class EditSession(View):
    template_name = 'edit-session.html'
    def getcontext(self, form):
        context = {}
        context["form"] = form
        return context

    def post(self, request, id):
        session = get_object_or_404(Session, pk=id)
        editSesForm = EditSessionForm(request.POST, instance=session)
        if editSesForm.is_valid():
            session = editSesForm.save(commit=False)
            if editSesForm.cleaned_data["include"] is not None:
                include = IncludeService.objects.get(name=editSesForm.cleaned_data["include"])
                session.includes.add(include)
            if editSesForm.cleaned_data["service"] is not None:
                service = AddService.objects.get(name=editSesForm.cleaned_data["service"])
                useservice, created = session.services.get_or_create(add = service)
                if created:
                    session.services.add(useservice)
                else:
                    useservice.count+=1
                useservice.save()

            session.save()
            return HttpResponseRedirect('/session/')
        else:
            context = self.getcontext(editSesForm)
            return render(request, self.template_name, context)

    def get(self, request, id):
        session = get_object_or_404(Session, pk=id)
        context = self.getcontext(EditSessionForm(instance=session))
        return render(request, self.template_name, context)

def printStopAccounts(printer, listSessions):
    printer.set(align='center')
    printer.image(os.path.join(STATIC_ROOT, 'img/kamenka256.jpg'))
    printer.set(text_type='B', width=2, height=1, align='left')
    text = '\n' + "Time-Club KAMENKA" + '\n' + "VISITOR ACCOUNT" + '\n' + '\n'
    printer.text(text)
    printer.set(text_type='NORMAL', width=1, height=1, align='left')
    for session in listSessions:
        text = "SID:        " + session.SID + '\n'
        text +="K OPLATE:   " + str(session.sum) + " rub." + '\n' + "-----------------------------" + '\n'
        printer.text(text)
    printer.cut()
def printEnteredTickets(printer, listSessions):
    for session in listSessions:
        printer.set(align='center')
        printer.image(os.path.join(STATIC_ROOT, 'img/kamenka256.jpg'))
        printer.set(text_type='B', width=2, height=1, align='left')
        text = '\n' + "Time-Club KAMENKA" + '\n' + "VISITOR TICKET"
        printer.text(text)
        printer.set(text_type='NORMAL', width=1, height=1, align='left')
        text = '\n' + '\n' + "SID:        " + session.SID + '\n' + "KOMNATA:    " + translit(session.room.name,reversed=True) + '\n' + "TARIF:      " + translit(
            session.company.tariff.name, reversed=True) + '\n' + "NACHALO:    " + datetime.strftime(session.start_dt.astimezone(TZL),
                                                                                                   "%Y-%m-%d %H:%M") + '\n'
        if session.company.tariff.type == "fp":
            text += "OKONCHANIE: " + datetime.strftime(session.start_dt.astimezone(TZL) + timedelta(hours=session.company.tariff.limit.hour,
                                                                                    minutes=session.company.tariff.limit.minute),
                                                       "%Y-%m-%d %H:%M") + '\n'
        if session.services.all().count() > 0:
            text += "USLUGI:     "
            for service in session.services.all():
                text += translit(service.add.name, reversed=True) + " - " + str(
                    service.add.price * service.count) + " rub." + '\n'
        if session.dep_cash is not None:
            text += "DEPOSIT(nal):" + str(session.dep_cash) + " rub." + '\n'
        if session.dep_card is not None:
            text += "DEPOSIT(bezn):" + str(session.dep_card) + " rub." + '\n'
        printer.text(text)
        printer.cut()

class payFinal(View):
    initial = {'key': 'value'}
    template_name = 'payfinal.html'

    def get(self, request, payment):
        context = {}
        context['payment'] = payment
        return render(request, self.template_name, context)

class MainSession(View):
    initial = {'key': 'value'}
    template_name = 'session.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        context = {}
        #header.html
        resAdm = Profile.objects.filter(reserved = True).first()
        context["resAdm"] = "" if resAdm is None else "(" + str(resAdm.user.username) + ")"
        #session.html
        sessions = Session.objects.filter(is_active=True).defer("cash","card").order_by("SID")
        for session in sessions:
            session.fullservsCount = 0
            session.fullservsText = ""
            for service in session.services.all():
                session.fullservsText += service.add.name
                if service.count == 1:
                    session.fullservsText += ","
                else:
                    session.fullservsText += "-" + str(service.count) + "шт.,"
                session.fullservsCount += service.count * service.add.price
            session.fullservsText = session.fullservsText[:-1]
        countSessions = sessions.count()
        rooms = Room.objects.all()
        companies = Company.objects.filter(count__gt = F('payed'))
        setting = Setting.objects.first()

        # calendar.html
        today = datetime.now(TZL)
        start = today.replace(hour=setting.start.hour,minute=setting.start.minute)
        end = today
        if today.time() < setting.start:
            today += timedelta(days=1)
            start -= timedelta(days=1)
        # inactive sessions
        status = request.GET.get("status", "-")
        if status == "inactive":
            context['inactive'] = True
            listOffSess = Session.objects.filter(is_active=False, start_dt__range=(start, end)).order_by("SID")
            for session in listOffSess:
                session.fullpay = 0
                if session.card is not None:
                    session.cardpay = session.card.amount
                    session.fullpay += session.cardpay
                if session.cash is not None:
                    session.cashpay = session.cash.amount
                    session.fullpay += session.cashpay
                session.fullservsCount = 0
                session.fullservsText = ""
                for service in session.services.all():
                    session.fullservsText += service.add.name
                    if service.count == 1:
                        session.fullservsText += ","
                    else:
                        session.fullservsText += "-" + str(service.count) + "шт.,"
                    session.fullservsCount += service.count * service.add.price
                session.fullservsText = session.fullservsText[:-1]
            context['listOffSess'] = listOffSess

        context["nowDate"] = today.date().strftime("%Y-%m-%d")
        context['countSessions'] = countSessions
        context['sessions'] = sessions
        context['setting'] = setting
        context['rooms'] = rooms
        context['companies'] = companies
        return render(request, self.template_name, context)

@csrf_exempt
def deleteView(request):
    if (request.method == "POST"):
        if request.is_ajax():
            sessionsId = request.POST["sessions"].split(",")
            tzlNow = datetime.now(TZL)
            setting = Setting.objects.first()
            for ID in sessionsId:
                session = Session.objects.get(id = ID)
                company = session.company
                session.end_dt = tzlNow
                tDelta = int((session.end_dt.astimezone(TZL) - session.start_dt.astimezone(TZL)).seconds / 60)
                if tDelta <= setting.delete_time:
                    if session.card is not None:
                        session.card.delete()
                    if session.cash is not None:
                        session.cash.delete()
                    for service in session.includes.all():
                        service.delete()
                    session.delete()
                companyCount = Session.objects.filter(company = company).count()
                if companyCount == 0:
                    company.delete()
                else:
                    company.count = companyCount
                    company.save()
            return JsonResponse({"type": "delete"})


@csrf_exempt
def stopView(request):
    if (request.method == "POST"):
        if request.is_ajax():
            sessionsId = request.POST["sessions"].split(",")
            sessionsSum = list()
            tzlNow = datetime.now(TZL)
            allprice = 0
            for ID in sessionsId:
                session = Session.objects.get(id = ID)
                session.end_dt = tzlNow
                tDelta = int((session.end_dt.astimezone(TZL) - session.start_dt.astimezone(TZL)).seconds / 60)
                if session.company.tariff.type == "tp":
                    if session.company.discount is None:
                        session.sum = int(tDelta * session.company.tariff.price)
                    else:
                        session.sum = 0 if session.owner else int(tDelta*session.company.tariff.price*session.company.discount.multiplier)
                elif session.company.tariff.type == "fp":
                    session.sum = 0 if session.owner else session.company.tariff.fix
                    externalTime = tDelta - (session.company.tariff.time.hour*60 + session.company.tariff.time.minute)
                    if externalTime > 0:
                        session.sum += externalTime * session.company.tariff.price
                for service in session.services.all():
                    session.sum += service.add.price * service.count
                session.sum -= (session.dep_card + session.dep_cash)
                allprice += session.sum
                session.save()
                sessionsSum.append(session.sum)

            return JsonResponse({"allPrice": allprice, "sessions": sessionsSum, "type": "stop"})

@csrf_exempt
def printView(request):
    if (request.method == "POST"):
        if request.is_ajax():
            sessionsId = request.POST["sessions"].split(",")
            setting = Setting.objects.first()
            if setting.is_print:
                printer = Network(setting.network)
                listSessions = list()
                for ID in sessionsId:
                    session = Session.objects.get(id = ID)
                    listSessions.append(session)
                printStopAccounts(printer, listSessions)
            return JsonResponse({"type": "print"})


@csrf_exempt
def tariffChange(request, id):
    if (request.method == "POST"):
        if request.is_ajax():
            pk = int(id)
            tariff = Tariff.objects.get(id = pk)
            dict = {}
            i = 0
            for discount in tariff.discounts.filter(days__num = datetime.today().weekday()):
                dict.update({i: {"id": discount.id, "name": discount.name}})
                i += 1
            return JsonResponse({"discounts": dict, "type": "tariffs", "count": len(dict), "minimum": tariff.limit})

@csrf_exempt
def discountChange(request, id):
    if (request.method == "POST"):
        if request.is_ajax():
            pk = int(id)
            discount = Discount.objects.get(id = pk)
            return JsonResponse({"type": "discounts", "minimum": discount.limit_gt, "maximum": discount.limit_lt})


def printFinalCheck(printer, listSessions, printVSEGO, printPRED, printKOPLATE, printCASH, printCARD, paymentClient):
    printer.set(align='center')
    printer.image(os.path.join(STATIC_ROOT, 'img/kamenka256.jpg'))
    printer.set(text_type='B', width=2, height=1, align='left')
    text = '\n' + "Time-Club KAMENKA" + '\n' + "VISITOR CHECK"
    printer.text(text)
    for session in listSessions:
        printer.set(text_type='NORMAL', width=1, height=1, align='left')
        text = '\n' + '\n' + "SID:        " + session.SID + '\n' + "KOMNATA:    " + translit(session.room.name,reversed=True) + '\n' + "TARIF:      " + translit(
            session.company.tariff.name, reversed=True) + '\n' + "NACHALO:    " + datetime.strftime(session.start_dt.astimezone(TZL),
                                                                                                   "%Y-%m-%d %H:%M") + '\n'
        text += "OKONCHANIE: " + datetime.strftime(session.end_dt.astimezone(TZL),"%Y-%m-%d %H:%M") + '\n'
        text += "VREMYA:     " + str(
            int((session.end_dt.astimezone(TZL) - session.start_dt.astimezone(TZL)).seconds / 60)) + " min." + '\n'
        if session.services.all().count() > 0:
            text += "USLUGI:     "
            for service in session.services.all():
                text += translit(service.add.name, reversed=True) + " - " + str(
                    service.add.price * service.count) + " rub." + '\n'
        fullSum = 0
        if session.cash is not None:
            fullSum += session.cash.amount
        if session.card is not None:
            fullSum += session.card.amount
        text += "K OPLATE: " + str(fullSum) + " rub." + '\n' + '\n' + '\n'
        printer.text(text)
    printer.set(text_type='B', width=2, height=1, align='center')
    text = "SUMMA VSEGO: " + str(printVSEGO) + " rub." + '\n'
    text += "PREDOPLATA:  " + str(printPRED) + " rub." + '\n'
    text += "K OPLATE:    " + str(printKOPLATE) + " rub." + '\n'
    printer.text(text)
    printer.set(text_type='NORMAL', width=1, height=1, align='left')
    text = "VNESENO NALICH: " + str(printCASH) + " rub." + '\n'
    text += "VNESENO KARTOY: " + str(printCARD) + " rub." + '\n'
    text += "SDACHA:         " + str(paymentClient) + " rub." + '\n'
    printer.text(text)
    printer.set(text_type='B', width=4, height=2, align='center')
    printer.text("CHECK PAYED!")
    printer.cut()
    printer.set(text_type='NORMAL', width=1, height=1, align='left')


@csrf_exempt
def payView(request):
    if (request.method == "POST"):
        if request.is_ajax():
            sessionsId = request.POST["sessions"].split(",")
            setting = Setting.objects.first()
            tzlNow = datetime.now(TZL)

            payInfo = request.POST["payInfo"].split(",")
            allSum = payInfo[0]
            cashPay = payInfo[1]
            cardPay = payInfo[2]

            if (len(cashPay) == 0):
                cashPay = "0"
            cashPay = int(cashPay)
            if (len(cardPay) == 0):
                cardPay = "0"
            cardPay = int(cardPay)
            if (len(allSum) == 0):
                allSum = "0"
            allSum = int(allSum)
            printKOPLATE = allSum
            printCASH = cashPay
            printCARD = cardPay
            printPRED = 0
            paySessionsList = list()
            for ID in sessionsId:
                session = Session.objects.get(id=ID)
                cardPay += session.dep_card
                cashPay += session.dep_cash
                allSum += session.dep_card + session.dep_cash
                session.sum += session.dep_card + session.dep_cash
                printPRED += session.dep_card + session.dep_cash
                session.save()
                paySessionsList.append(session)
            printVSEGO = allSum
            paymentClient = allSum - (cashPay+cardPay)
            if paymentClient > 0:
                return JsonResponse({"info": "error", "type": "pay"})
            for session in paySessionsList:
                while (session.sum > 0):
                    if (cardPay > 0):
                        if (session.card == None):
                            pay = CardPay(time=tzlNow)
                        else:
                            pay = session.card
                        if (cardPay >= session.sum):
                            pay.amount = session.sum
                            cardPay -= pay.amount
                            session.sum = 0
                        else:
                            pay.amount = cardPay
                            session.sum -= pay.amount
                            cardPay = 0
                        pay.save()
                        session.card = pay
                    elif (cashPay > 0):
                        if (session.cash == None):
                            pay = CashPay(time=tzlNow)
                        else:
                            pay = session.cash
                        if (cashPay >= session.sum):
                            pay.amount = session.sum
                            cashPay -= pay.amount
                            session.sum = 0
                        else:
                            pay.amount = cashPay
                            session.sum -= pay.amount
                            cashPay = 0

                        setting.cash_now += pay.amount
                        pay.save()
                        session.cash = pay
                session.is_active = False
                company = session.company
                company.payed += 1
                company.save()
                session.save()
            setting.save()
            if setting.is_print:
                printer = Network(setting.network)
                printFinalCheck(printer, paySessionsList, printVSEGO, printPRED, printKOPLATE, printCASH, printCARD, -paymentClient)

            if paymentClient == 0:
                return JsonResponse({"info": "equal", "type": "pay", "payment": -paymentClient})
            else:
                return JsonResponse({"info": "dolg", "type": "pay", "payment": -paymentClient})

