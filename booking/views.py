from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from enter.models import *
from daycalendar.models import *
from main.models import *
from .models import *
from .forms import EditBookingForm,NewBookingForm
from datetime import datetime, date, timedelta
from escpos.printer import Network
from arm.settings import TZL
from main.views import printEnteredTickets
# Create your views here.
class MainBooking(View):
    initial = {'key': 'value'}
    template_name = 'booking.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        context = {}
        # header.html
        resAdm = Profile.objects.filter(reserved=True).first()
        context["resAdm"] = "" if resAdm is None else "(" + str(resAdm.user.username) + ")"

        #booking.html
        sessions = Session.objects.filter(is_active=True).defer("cash","card").order_by("SID")
        listBooking = Booking.objects.all().order_by("date","room", "time_start")
        for booking in listBooking:
            booking.dep = booking.dep_cash + booking.dep_card
            booking.info = ""
            booking.info1 = ""
            if booking.name is not None and booking.name is not "":
                booking.info += booking.name + ", "
            if booking.phone is not None and booking.phone is not "":
                booking.info += booking.phone + ", "
            if booking.text is not None and booking.text is not "":
                booking.info += booking.text + ", "
            for service in booking.services.all():
                booking.info1 += service.name + ", "
            for service in booking.includes.all():
                booking.info1 += service.name + ", "
        countSessions = sessions.count()
        setting = Setting.objects.first()
        #calendar.html
        today = datetime.now(TZL)
        if today.time() < setting.start:
            today += timedelta(days=1)
        context["nowDate"] = today.date().strftime("%Y-%m-%d")
        context['countSessions'] = countSessions
        context['setting'] = setting
        context['bookings'] = listBooking

        return render(request, self.template_name, context)


class EditBooking(View):
    template_name = 'edit-booking.html'
    def getcontext(self, form):
        context = {}
        context["form"] = form
        return context

    def post(self, request, id):
        booking = get_object_or_404(Booking, pk=id)
        if 'booking_delete' in request.POST:
            booking.delete()
            return HttpResponseRedirect('/booking/')
        else:
            editBookForm = EditBookingForm(request.POST, instance=booking)
            if editBookForm.is_valid():
                booking = editBookForm.save(commit=False)
                for ns in booking.services.all():
                    booking.services.remove(ns)
                for ns in editBookForm.cleaned_data["services"]:
                    service = AddService.objects.get(name=ns)
                    booking.services.add(service)
                for ns in booking.includes.all():
                    booking.includes.remove(ns)
                for ns in editBookForm.cleaned_data["includes"]:
                    includeservice = IncludeService.objects.get(name=ns)
                    booking.includes.add(includeservice)
                booking.save()
                if 'booking_activate' in request.POST:
                    setting = Setting.objects.first()
                    if setting.is_print:
                        printer = Network(setting.network)
                        listSessions = list()
                    simpleCash, addingCash, simpleCard, addingCard = 0, 0, 0, 0
                    if booking.dep_cash > 0:
                        simpleCash = booking.dep_cash // booking.persons
                        addingCash = booking.dep_cash % booking.persons
                    if booking.dep_card > 0:
                        simpleCard = booking.dep_card // booking.persons
                        addingCard = booking.dep_card % booking.persons
                    prevCompany = Company.objects.filter(date__gte=date.today().replace(day=1)).last()
                    prevCompanyID = 0 if prevCompany is None else prevCompany.CID
                    room = booking.room
                    tariff = booking.tariff
                    discount = booking.discountB
                    countSessions = booking.persons
                    counter = countSessions
                    countOwners = tariff.free if tariff.type == "fp" else discount.free if discount is not None else 0
                    company = Company.objects.create(CID=prevCompanyID + 1, count=countSessions, tariff=tariff,
                                                     discount=discount)
                    today = datetime.now(TZL)
                    todayMonth = str(today.month) if today.month >= 10 else "0" + str(today.month)
                    todayDay = str(today.day) if today.day >= 10 else "0" + str(today.day)
                    todayCID = str(company.CID) if company.CID >= 100 else "0" + str(
                        company.CID) if company.CID >= 10 else "00" + str(company.CID)
                    partSID = str(today.year) + todayMonth + todayDay + todayCID
                    while counter > 0:
                        todaySID = str(counter) if counter >= 10 else "0" + str(counter)
                        session = Session.objects.create(SID=partSID + str(todaySID), room=room, company=company)
                        if countOwners > 0:
                            session.owner = True
                            session.save()
                            countOwners -= 1
                        if counter == countSessions:
                            session.text = booking.text
                            session.dep_cash = simpleCash + addingCash
                            session.dep_card = simpleCard + addingCard
                            for us in booking.services.all():
                                useservice = UseService.objects.create(add=us)
                                useservice.save()
                                session.services.add(useservice)
                            for ns in booking.includes.all():
                                session.includes.add(ns)
                        else:
                            session.dep_cash = simpleCash
                            session.dep_card = simpleCard
                        session.save()
                        if setting.is_print:
                            listSessions.append(session)
                        counter -= 1
                    booking.delete()
                    if setting.is_print:
                        printEnteredTickets(printer, listSessions)
                    return HttpResponseRedirect('/session/')
                else:
                    return HttpResponseRedirect('/booking/')
            else:
                context = self.getcontext(editBookForm)
                return render(request, self.template_name, context)

    def get(self, request, id):
        booking = get_object_or_404(Booking, pk=id)
        context = self.getcontext(EditBookingForm(instance=booking))
        return render(request, self.template_name, context)

class NewBooking(View):
    template_name = 'new-booking.html'
    def getcontext(self, form, date, tFrom, tTo,duration, room):
        context = {}
        form.fields["room"].initial = room
        form.fields["duration"].initial = duration
        form.fields["time_start"].initial = tFrom
        form.fields["time_end"].initial = tTo
        form.fields["date"].initial = date
        context["form"] = form
        return context

    def get(self, request):
        needdate = request.GET.get("date", "-")
        needduration = request.GET.get("duration", "-").split("-")
        needto = request.GET.get("to", "-").split("-")
        needfrom = request.GET.get("from", "-").split("-")
        needroom = request.GET.get("room", "-")
        needDate = datetime(int(needdate.split("-")[0]), int(needdate.split("-")[1]), int(needdate.split("-")[2]), 0, 0,
                            tzinfo=TZL)
        needFrom = time(hour=int(needfrom[0]), minute=int(needfrom[1]))
        needTo = time(hour=int(needto[0]), minute=int(needto[1]))
        needDuration = time(hour=int(needduration[0]), minute=int(needduration[1]))
        needRoom = Room.objects.get(id = int(needroom))
        context = self.getcontext(NewBookingForm(), needDate, needFrom, needTo, needDuration, needRoom)
        return render(request, self.template_name, context)

    def post(self, request):
        newBookForm = NewBookingForm(request.POST)
        if newBookForm.is_valid():
            booking = newBookForm.save()

            for ns in newBookForm.cleaned_data["servicesBook"]:
                service = AddService.objects.get(name=ns)
                booking.services.add(service)
            for ns in newBookForm.cleaned_data["includesBook"]:
                includeservice = IncludeService.objects.get(name=ns)
                booking.includes.add(includeservice)
            booking.save()
            return HttpResponseRedirect('/booking/')
        else:
            context = self.getcontext(newBookForm)
            return render(request, self.template_name, context)