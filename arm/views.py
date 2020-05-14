from django.shortcuts import redirect

from daycalendar.models import Setting


def daycalendar_setting(request):
    return redirect("/admin/daycalendar/setting/"+str(Setting.objects.first().id)+"/change")