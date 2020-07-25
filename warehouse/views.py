from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import *
from main.models import *
from django.views.decorators.csrf import csrf_exempt

from enter.models import Profile
from daycalendar.models import *
from django.db.models import Sum, F, Q, FloatField
from datetime import datetime, date, timedelta
from arm.settings import TZL
# Create your views here.
def send_telegram(text: str):
    pass
    # bot.send_message(TELEGRAM_CHAT_ID, text)
    # bot.polling(none_stop=True, timeout=123)
class MainWarehouse(View):
    initial = {'key': 'value'}
    template_name = 'warehouse.html'

    def get(self, request, *args, **kwargs):
        if request.user.groups.filter(Q(name='Кладовщик') | Q(name='Директор')).exists() or request.user.is_superuser:
            context = {}

            listsess = Session.objects.filter(end_dt=None)
            setting = Setting.objects.first()
            now = datetime.now(TZL)
            date = now - timedelta(days=7)
            listinout = WarehouseInOut.objects.filter(date__range=(date, now)).order_by('-date')
            period = WarehouseInOut.objects.filter(type_operations='Расход', date__range=(date, now)).values(
                good=F('title_goods__title'), sub=F('title_goods__subcat__subcat_title'),
                cat=F('title_goods__subcat__category__cat_title')).annotate(cost=Sum('cost'), units=Sum(
                F('amount') * F('volume'))).order_by('title_goods__subcat__category', 'title_goods__subcat')
            totalsum = 0
            for p in period:
                totalsum += p['cost']
            listOfGoods = Goods.objects.all()
            forcheck = Volumes.objects.all().values(g=F('good__title')).annotate(
                rest=Sum(F('amount') * F('volume'), output_field=FloatField()))
            volumes = Volumes.objects.all().values('volume', 'amount', g=F('good__title'),
                                                   sub=F('good__subcat__subcat_title'),
                                                   cat=F('good__subcat__category__cat_title'), yellow=F('good__yellow'),
                                                   red=F('good__red')).order_by('good__subcat__category',
                                                                                'good__subcat', 'good')
            for v in volumes:
                for f in forcheck:
                    if v['g'] == f['g']:
                        if f['rest'] <= v['red']:
                            v['color'] = 'red'
                        elif f['rest'] > v['yellow']:
                            v['color'] = 'green'
                        else:
                            v['color'] = 'orange'
            countSessions = listsess.count()
            context['cats'] = Categories.objects.all()
            context['subcats'] = Subcategories.objects.all()
            context['goods'] = listOfGoods
            context['inout'] = listinout
            context['period'] = period
            context['vol'] = volumes
            context['totalsum'] = totalsum
            context['countSessions'] = countSessions
            context['admin_groups'] = request.user.groups.filter(name='Админ').exists()
            # header.html
            resAdm = Profile.objects.filter(reserved=True).first()
            context["resAdm"] = "" if resAdm is None else "(" + str(resAdm.user.username) + ")"
            context['setting'] = setting

            return render(request, self.template_name, context)
        else:

            return HttpResponseRedirect("/session/")

@csrf_exempt
def WarehouseFilter(request):
    if (request.method == "POST"):
        if request.is_ajax():
            ThisCat = request.POST['ThisCat']
            ThisSubcat = request.POST.get('ThisSubcat', 'hide')
            aC = Categories.objects.all()
            aS = Subcategories.objects.all()
            aG = Goods.objects.all()
            allCat = set()
            allSubcat = set()
            allGood = set()
            if (ThisCat != "hide"):
                aS = aS.filter(category__cat_title=ThisCat)
                aG = aG.filter(subcat__in=aS)

            if (ThisSubcat != "hide"):
                aG = aG.filter(subcat__subcat_title=ThisSubcat)

            for cat in aC:
                allCat.add(cat.cat_title)

            for sub in aS:
                allSubcat.add(sub.subcat_title)

            for good in aG:
                allGood.add(good.title)

            allCat = list(allCat)
            allSubcat = list(allSubcat)
            allGood = list(allGood)
            return JsonResponse(wrhsDict(allCat, allSubcat, allGood))

@csrf_exempt
def WrhsIn(request):
    if (request.method == "POST"):
        if request.is_ajax():
            Good = request.POST['good']
            Volume = float(request.POST['volume'])
            Amount = int(request.POST['amount'])
            Cost = float(request.POST['cost'])
            price = round(Cost / (Volume * Amount), 4)
            aV = Volumes.objects.filter(good__title=Good)
            aC = Costs.objects.filter(good__title=Good)
            tV = 0
            tC = 0
            g = Goods.objects.get(title=Good)
            newIn = WarehouseInOut.objects.create(users=request.user, type_operations='Приход', title_goods=g,
                                                  volume=Volume, amount=Amount, cost=Cost)
            for c in aC:
                if c.price == price:
                    tC += 1
                    c.quantity += Amount * Volume
                    c.save()
                    break
            if tC == 0:
                newPrice = Costs.objects.create(good=g, quantity=Amount * Volume, price=price)
            for v in aV:
                if v.volume == Volume:
                    tV += 1
                    newA = v.amount + Amount
                    v.amount = newA
                    v.save()
                    return JsonResponse({'a': newA, 'v': Volume, 'g': Good})
            if tV == 0:
                newVol = Volumes.objects.create(good=g, volume=Volume, amount=Amount)
            return JsonResponse({'a': Amount, 'v': Volume, 'g': Good})
@csrf_exempt
def VolumeFilter(request):
    if (request.method == "POST"):
        if request.is_ajax():
            Good = request.POST['good']
            allV = set()
            aV = Volumes.objects.filter(good__title=Good)
            for v in aV:
                allV.add(v.volume)

            allV = list(allV)
            return JsonResponse({'aV' : allV})
@csrf_exempt
def AmountFilter(request):
    if (request.method == "POST"):
        if request.is_ajax():
            Good = request.POST['good']
            Volume = float(request.POST['volume'])
            Amount = Volumes.objects.get(good__title=Good, volume=Volume).amount
            return JsonResponse({'a': Amount})
@csrf_exempt
def WrhsOut(request):
    if (request.method == "POST"):
        if request.is_ajax():
            Good = request.POST['good']
            Volume = float(request.POST['volume'])
            Amount = float(request.POST['amount'])
            Comment = request.POST['comment']
            quantity = Amount*Volume
            #whatsApp = WhatsApp.objects.all().first()
            g = Goods.objects.get(title=Good)
            v = Volumes.objects.get(good__title=Good, volume=Volume)
            v.amount -= Amount
            v.save()
            rest = Amount
            allCosts = Costs.objects.filter(good=g).order_by('price')
            i = 0

            while quantity > 0:
                if allCosts.first().quantity > quantity:
                    a = Costs.objects.get(id=allCosts.first().id)
                    a.quantity -= quantity
                    a.save()
                    newout = WarehouseInOut.objects.create(users=request.user, type_operations='Расход', title_goods=g, volume=Volume, amount=rest,comment=Comment, cost=float(a.price)*quantity)
                    quantity = 0
                else:
                    quantity -= allCosts.first().quantity
                    newA = round((allCosts.first().quantity / Volume),4)
                    rest -= newA
                    newout = WarehouseInOut.objects.create(users=request.user, type_operations='Расход', title_goods=g, volume=Volume, amount=newA,comment=Comment, cost=float(allCosts.first().price)*allCosts.first().quantity)
                    allCosts[i].delete()
            rests = Volumes.objects.filter(good=g).values(g=F('good__title'),sub=F('good__subcat__subcat_title'), yellow=F('good__yellow'), red=F('good__red')).annotate(rest=Sum(F('amount') * F('volume'), output_field=FloatField()))
            rets = list(rests)
            if rets[0]['rest'] <= rets[0]['yellow']:
                if rets[0]['rest'] <= rets[0]['red']:
                    rets[0]['color'] = 'Красный'
                else :
                    rets[0]['color'] = 'Желтый'
            return JsonResponse({'a': v.amount, 'v' : Volume, 'g' : Good})
@csrf_exempt
def wrhsPeriod(request):
    if (request.method == "POST"):
        if request.is_ajax():
            start = request.POST['start']
            end = request.POST['end']
            lfP = set()
            totalsum = 0
            sD = datetime.strptime(start,'%Y-%m-%d')
            eD = datetime.strptime(end, "%Y-%m-%d") + timedelta(days=1) - timedelta(seconds= 1)
            plist = WarehouseInOut.objects.filter(type_operations='Расход', date__range=(sD, eD)).values(good=F('title_goods__title'),sub=F('title_goods__subcat__subcat_title'),cat=F('title_goods__subcat__category__cat_title')).annotate(cost=Sum('cost'), units=Sum(F('amount') * F('volume'))).order_by('title_goods__subcat__category','title_goods__subcat')
            for p in plist:
                totalsum += p['cost']
            lfP = list(plist)
            return JsonResponse({"lfP" : lfP, 'ts' : totalsum})

def wrhsExport(request):
    context = {}
    rests = Volumes.objects.all().values(g=F('good__title'),sub=F('good__subcat__subcat_title'),cat=F('good__subcat__category__cat_title'), yellow=F('good__yellow'), red=F('good__red')).annotate(rest=Sum(F('amount') * F('volume'), output_field=FloatField()))
    rrr = list(rests)
    i = 0
    while i < len(rrr) :
        if float(rrr[i]['rest']) <= float(rrr[i]['red']):
            rrr[i]['color'] = 'red'
            i +=1
        elif float(rrr[i]['rest']) > float(rrr[i]['yellow']):
            rrr.remove(rrr[i])
        else:
            rrr[i]['color'] = 'orange'
            i +=1
    context['rests']=rrr
    return render(request, 'export.html', context)

def exportClick(request):
    rests = Volumes.objects.all().values(g=F('good__title'),sub=F('good__subcat__subcat_title'),cat=F('good__subcat__category__cat_title'), yellow=F('good__yellow'), red=F('good__red')).annotate(rest=Sum(F('amount') * F('volume'), output_field=FloatField()))
    rrr = list(rests)
    i = 0
    while i < len(rrr) :
        if float(rrr[i]['rest']) <= float(rrr[i]['red']):
            rrr[i]['color'] = 'красный'
            i +=1
        elif float(rrr[i]['rest']) > float(rrr[i]['yellow']):
            rrr.remove(rrr[i])
        else:
            rrr[i]['color'] = 'желтый '
            i +=1
    mes = 'Товары, которые необходимо дозакупить:' + '\n'
    for r in rrr:
        mes +=  'Товар: ' + r['sub'] + ' ' + r['g'] + '/ уровень: ' + r['color'] + '/ остаток: ' + str(r['rest']) + '\n'
    send_telegram(mes)
    return HttpResponseRedirect('/warehouse/export/')