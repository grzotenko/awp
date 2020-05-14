import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arm.settings")

import time
from management.models import *
from daycalendar.models import Setting
def removeChangedPlan():
    planChanged = FuturePlan.objects.all().order_by("day", "type")
    for pc in planChanged:
        obj = CurrentPlan.objects.get(day = pc.day, type = pc.type)
        obj.profile = pc.profile
        obj.save()
        pc.profile = None
        pc.save()
    VacantedShifts.objects.all().delete()
def buildChangedPlan():
    admins = Profile.objects.all()
    shifts = FuturePlan.objects.exclude(type="R")
    for shift in shifts:
        admin = admins.filter(preferences__day = shift.day, preferences__type = shift.type, preferences__pref = "+").distinct("id").order_by("countG", "countB", "-restB").first()
        if admin is not None:
            shift.profile = admin
            shift.save()
            admin.countG += 1
            admin.save()
    shifts = FuturePlan.objects.exclude(type="R").filter(profile = None)
    for shift in shifts:
        admin = admins.filter(preferences__day=shift.day, preferences__type=shift.type, preferences__pref="=").distinct("id").order_by("countG", "countB", "-restB").first()
        if admin is not None:
            shift.profile = admin
            shift.save()
            admin.countG += 1
            admin.save()
    shifts = FuturePlan.objects.exclude(type="R").filter(profile = None)
    for shift in shifts:
        admin = admins.filter(preferences__day = shift.day, preferences__type = shift.type).exclude(id=FuturePlan.objects.get(day=shift.day, type="M").profile.id).distinct("id").order_by("countG", "countB", "-restB").first()
        if admin is not None:
            # if admin == PlanChanged.objects.filter(day = shift.day, type = "M"):
            shift.profile = admin
            shift.save()
            admin.countG += 1
            admin.countB += 1
            admin.restB -= 1
            admin.save()
    shifts = FuturePlan.objects.exclude(type="R").filter(profile=None)
    for shift in shifts:
        admin = admins.filter(preferences__day = shift.day, preferences__type = shift.type).distinct("id").order_by("countG", "countB", "-restB").first()
        shift.profile = admin
        shift.save()
        admin.countG += 1
        admin.countB += 1
        admin.restB -= 1
        admin.save()
    shifts = FuturePlan.objects.filter(type="R")
    for shift in shifts:
        admin = admins.filter(preferences__day=shift.day, preferences__type="E").exclude(id=FuturePlan.objects.get(day=shift.day, type="E").profile.id).distinct("id").order_by("-countG", "-countB", "restB")
        for a in admin:
            if a.prefs.get(day=shift.day, type="E").pref != "-":
                shift.profile = a
                shift.save()
                a.countG+=1
                a.save()
                if a.prefs.get(day=shift.day, type="E").pref == "+":
                    break
    for shift in shifts.filter(profile = None):
        admin = admins.filter(preferences__day=shift.day, preferences__type="E").exclude(id=FuturePlan.objects.get(day=shift.day, type="E").profile.id).distinct("id").order_by("countB", "-restB", "countG").first()
        shift.profile = admin
        shift.save()
        admin.countG += 1
        admin.countB += 1
        admin.restB -= 1
        admin.save()
    for admin in Profile.objects.all():
        admin.countG = 0
        admin.countB = 0
        admin.restB = 0
        admin.save()
    for pref in Preferences.objects.all():
        pref.pref = "="
        pref.save()
