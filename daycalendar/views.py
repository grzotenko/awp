from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from enter.models import *
from main.models import *
from booking.models import *
from .models import *
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, date, timedelta
from arm.settings import TZL
# Create your views here.
class MainCalendar(View):
    initial = {'key': 'value'}
    template_name = 'calendar.html'

    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponseRedirect("/")
        context = {}
        # header.html
        resAdm = Profile.objects.filter(reserved=True).first()
        context["resAdm"] = "" if resAdm is None else "(" + str(resAdm.user.username) + ")"

        #calendar.html
        sessions = Session.objects.filter(is_active=True).defer("cash","card").order_by("SID")
        countSessions = sessions.count()
        nowDate = datetime.now(TZL)
        setting = Setting.objects.first()
        getterTime = setting.start
        if ((nowDate.hour < getterTime.hour) or (
                nowDate.hour == getterTime.hour and nowDate.minute < getterTime.minute)):
            nowDate -= timedelta(days=1)
        rooms = Room.objects.all()
        today = datetime.now(TZL)
        operativeTime = today.replace(hour=getterTime.hour, minute=getterTime.minute, second=0, microsecond=0)
        massiv = []
        for i in range(48):
            dictionary = dict()
            for room in rooms:
                smalldictionary = dict()

                smalldictionary.update({"status": "cellFree"})
                smalldictionary.update({"time": operativeTime})
                smalldictionary.update({"room": room.pk})
                smalldictionary.update({"info": ""})
                smalldictionary.update({"id": ""})
                smalldictionary.update({"fullinfo": ""})
                smalldictionary.update({"visible": False})
                smalldictionary.update({"color": room.color})
                smalldictionary.update({"font": room.font})
                dictionary.update({room.name: smalldictionary})
            massiv.append(dictionary)
            operativeTime += timedelta(minutes=30)
        needdate = request.GET.get("date", "-")
        needDate = datetime(int(needdate.split("-")[0]), int(needdate.split("-")[1]), int(needdate.split("-")[2]), 0, 0, tzinfo=TZL)
        if today.time() < getterTime:
            needDate += timedelta(days=1)
        endPoint = today.replace(minute=0, second=0, microsecond=0) if today.time().minute < 30 else today.replace(
            minute=30, second=0, microsecond=0)
        operativeTime = today.replace(hour=getterTime.hour, minute=getterTime.minute, second=0, microsecond=0)
        if needDate.date() == today.date():#если выбран текущий день
            sessions = Session.objects.filter(is_active=True).distinct("company").distinct("room")
            for session in sessions:
                elem = operativeTime - session.start_dt if session.start_dt.time() >= getterTime else session.start_dt - operativeTime
                elem = int(elem.seconds / 1800)
                obj = massiv[elem].get(session.room.name)
                startPoint = obj.get("time")
                while startPoint < endPoint:
                    massiv[elem].get(session.room.name).update({"status": "cellSession"})
                    startPoint += timedelta(minutes=30)
                    elem += 1
        bookings = Booking.objects.filter(date = needDate.date())
        for booking in bookings:
            bookingStart = operativeTime.replace(hour = booking.time_start.hour, minute = booking.time_start.minute)
            bookingEnd = operativeTime.replace(hour = booking.time_end.hour, minute = booking.time_end.minute)
            if bookingEnd.time() < getterTime:
                bookingEnd += timedelta(days=1)
            elem = bookingStart - operativeTime if booking.time_start >= getterTime else operativeTime - bookingStart
            elem = int(elem.seconds / 1800)
            obj = massiv[elem].get(booking.room.name)
            startPoint = obj.get("time")
            fullinfo = ""
            name = ""
            servs = ""
            if booking.name is not None and booking.name != "":
                fullinfo += booking.name + ","
                name = booking.name
            fullinfo += str(booking.persons) + " чел.,"
            if booking.phone is not None and booking.phone != "":
                fullinfo += booking.phone + ","
            for include in booking.includes.all():
                fullinfo += include.name + ","
                servs += include.name + ","
            for services in booking.services.all():
                fullinfo += services.name + ","
                servs += services.name + ","
            counter = 0
            while startPoint < bookingEnd:
                if counter == 0:
                    massiv[elem].get(booking.room.name).update({"visible": True})
                    massiv[elem].get(booking.room.name).update({"info": name})
                if counter == 1:
                    massiv[elem].get(booking.room.name).update({"visible": True})
                    massiv[elem].get(booking.room.name).update({"info": servs})
                massiv[elem].get(booking.room.name).update({"fullinfo": fullinfo})
                counter += 1
                bookingId = "booking" + str(counter) + "-" +str(booking.id)
                massiv[elem].get(booking.room.name).update({"id": bookingId})
                massiv[elem].get(booking.room.name).update({"status": "cellBooking"})
                startPoint += timedelta(minutes=30)
                elem += 1
        context["rooms"] = massiv[0]
        context["nowDate"] = needDate.date().strftime("%Y-%m-%d")
        context['countSessions'] = countSessions
        context['setting'] = setting
        context['massiv'] = massiv
        return render(request, self.template_name, context)

