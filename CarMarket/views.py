from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
import xlrd
from django.views.decorators.csrf import  csrf_exempt
from django.db.models import Q

from CarMarket.models import Car


   ### With the code below, we extracted values from xls file and stored them in sqlite database as Car model.

# excelData = xlrd.open_workbook('C:\\Users\\Samsung\\Desktop\\turkey_car_market.xls')
# sheet = excelData.sheet_by_index(0)
#
#
# for r in range(2, 9000):
#     t = sheet.cell(r, 0).value.split('/')
#     d = t[2] + "-" + t[1] + "-" + t[0]
#
#     car = Car(
#         date=d,
#         brand=sheet.cell(r, 1).value,
#         model=sheet.cell(r, 2).value,
#         year=sheet.cell(r, 3).value,
#         color=sheet.cell(r, 4).value,
#         km=sheet.cell(r, 5).value,
#         price=sheet.cell(r, 6).value,
#     )
#
#     car.save()

def showCars(request):


    car_list = Car.objects.all()

    marka_array = []


    for car in car_list:

        if (not car.brand in marka_array):
            marka_array.append(car.brand)


    marka_array = sorted(marka_array)



    return render(request, "index.html", {'marka_list': marka_array})


@csrf_exempt
def model_ajax(request):
    marka = request.body.decode('utf-8')

    if "*" in marka:
        marka = marka.replace("*"," ")

    listem = list(Car.objects.filter(brand__contains = marka).order_by('model'))
    data = []
    models = []
    for car in listem:
        if(listem.index(car) != len(listem)-1 and not car.model in models ):
            data.append(car.model.strip()+"^")
            models.append(car.model.strip())

        elif(not car.model in models):
            data.append(car.model.strip())
            models.append(car.model.strip())
    return HttpResponse(data)


@csrf_exempt
def year_ajax(request):
    marka_model = request.body.decode('utf-8')
    data = []
    if not "?" in marka_model:
        if "*" in marka_model:
            marka_model = marka_model.replace("*"," ")
        marka_model = marka_model.split("_")

        #car_list = Car.objects.all()
        listem = list(Car.objects.filter(brand__contains=marka_model[0]).filter(model__contains=marka_model[1]).order_by('year'))

        years = []
        for car in listem:
            if(listem.index(car) != len(listem)-1 and not str(car.year) in years ):
                data.append(str(car.year)+"^")
                years.append(str(car.year))
            elif(not str(car.year) in years):
                data.append(str(car.year)+"^")
                years.append(str(car.year))

    else:
        if "*" in marka_model:
            marka_model = marka_model.replace("*", " ")
        marka_models = marka_model.split("?")

        years = []
        for marka_model in marka_models:
            marka_model = marka_model.split("_")

            listem = list(Car.objects.filter(brand__contains=marka_model[0]).filter(model__contains=marka_model[1]).order_by('year'))
            for car in listem:
                if(listem.index(car) != len(listem)-1 and not str(car.year) in years ):
                    data.append(str(car.year)+"^")
                    years.append(str(car.year))
                elif(not str(car.year) in years):
                    data.append(str(car.year)+"^")
                    years.append(str(car.year))


    return HttpResponse(data)



@csrf_exempt
def color_ajax(request):

    marka_model_tarih = request.body.decode('utf-8')

    if "*" in marka_model_tarih:
        marka_model_tarih = marka_model_tarih.replace("*"," ")

    if("?" in marka_model_tarih):
      marka_model_tarih = marka_model_tarih.split("?")

      marka = marka_model_tarih[0].split("_")[0]
      modeller = []
      tarihler = []

      for splitted in marka_model_tarih:    #question mark

          if (not splitted.split("_")[1] in modeller):
              modeller.append(splitted.split("_")[1])
          if (len(splitted.split("_")) == 3 and not splitted.split("_")[2] in tarihler ):
              tarihler.append(splitted.split("_")[2])

      filtered = Car.objects.filter(brand__contains=marka)

      query = Q()

      for model in modeller:
          query |= Q(model__contains = model)

      #filtered = Car.objects.filter(query)

      filtered = filtered.filter(query)

      query = Q()

      for tarih in tarihler:
          query |= Q(year__contains = int(tarih))

      filtered = filtered.filter(query)

      listem = list(filtered)


    else:
        marka_model_tarih = marka_model_tarih.split("_")
        #car_list = Car.objects.all()
        listem = list(Car.objects.filter(brand__contains=marka_model_tarih[0]).filter(model__contains=marka_model_tarih[1]).filter(year__contains=int(marka_model_tarih[2])))

    data = []
    colors = []
    for car in listem:
        if(listem.index(car) != len(listem)-1  and not car.color.strip() in colors ):
            data.append(car.color.strip()+"^")
            #colors.append(car.renk[6:-1].strip())
            colors.append(car.color.strip())

        elif (not car.color.strip() in colors):
            data.append(car.color.strip())
            #colors.append(car.renk[6:-1].strip())
            colors.append(car.color)
    return HttpResponse(data)


@csrf_exempt
def km_ajax(request):

    marka_model_tarih_renk = request.body.decode('utf-8')

    if "*" in marka_model_tarih_renk:
        marka_model_tarih_renk = marka_model_tarih_renk.replace("*"," ")

    if "?" in marka_model_tarih_renk:
        marka_model_tarih_renk = marka_model_tarih_renk.split("?")

        marka = marka_model_tarih_renk[0].split("_")[0]

        modeller =[]
        tarihler = []
        renkler  =[]

        for splitted in marka_model_tarih_renk:
            if (not splitted.split("_")[1] in modeller):
                modeller.append(splitted.split("_")[1])
            if (len(splitted.split("_")) >= 3 and not splitted.split("_")[2] in tarihler):
                tarihler.append(splitted.split("_")[2])
            if (len(splitted.split("_")) == 4 and not splitted.split("_")[3] in renkler):
                renkler.append(splitted.split("_")[3])

        filtered = Car.objects.filter(brand__contains=marka)
        query = Q()

        for model in modeller:
            query |= Q(model__contains=model)

        # filtered = Car.objects.filter(query)

        filtered = filtered.filter(query)

        query = Q()

        for tarih in tarihler:
            query |= Q(year__contains=int(tarih))

        filtered = filtered.filter(query)

        query = Q()
        for renk in renkler:
            query |= Q(color__contains = renk)

        filtered = filtered.filter(query)

        listem = list(filtered)



    else:
        marka_model_tarih_renk = marka_model_tarih_renk.split("_")
        listem = list(Car.objects.filter(brand__contains=marka_model_tarih_renk[0]).filter(model__contains=marka_model_tarih_renk[1]).filter(year__contains=int(marka_model_tarih_renk[2])).filter(color__contains=marka_model_tarih_renk[3]))

    data = []
    enBuyuk = 0
    enKucuk = int(listem[0].km)

    for car in listem:
       if(int(car.km) > enBuyuk):
           enBuyuk = int(car.km)

       if(int(car.km) < enKucuk):
           enKucuk = int(car.km)

    data.append(str(enKucuk)+"^")
    data.append(enBuyuk)


    return HttpResponse(data)


@csrf_exempt
def price_ajax(request):
    marka_model_tarih_renk_km = request.body.decode('utf-8')
    buyuk = 0
    kucuk = 0

    if "*" in marka_model_tarih_renk_km:
        marka_model_tarih_renk_km = marka_model_tarih_renk_km.replace("*", " ")

    if "?" in marka_model_tarih_renk_km:
        marka_model_tarih_renk_km = marka_model_tarih_renk_km.split("?")

        marka = marka_model_tarih_renk_km[0].split("_")[0]

        modeller = []
        tarihler = []
        renkler = []
        kmler = []

        for splitted in marka_model_tarih_renk_km:
            if (not splitted.split("_")[1] in modeller):
                modeller.append(splitted.split("_")[1])
            if (len(splitted.split("_")) >= 3 and not splitted.split("_")[2] in tarihler):
                tarihler.append(splitted.split("_")[2])
            if (len(splitted.split("_")) >= 4 and not splitted.split("_")[3] in renkler):
                renkler.append(splitted.split("_")[3])
            if (len(splitted.split("_")) == 5 and not splitted.split("_")[4] in kmler):
                kmler.append(splitted.split("_")[4])

        filtered = Car.objects.filter(brand__contains=marka)
        query = Q()

        for model in modeller:
            query |= Q(model__contains=model)

        # filtered = Car.objects.filter(query)

        filtered = filtered.filter(query)

        query = Q()

        for tarih in tarihler:
            query |= Q(year__contains=int(tarih))

        filtered = filtered.filter(query)

        query = Q()
        for renk in renkler:
            query |= Q(color__contains=renk)

        filtered = filtered.filter(query)

        #filtered = filtered.filter(km__gte = kmler[0])
        #filtered = filtered.exclude(km__gte = kmler[1])

        if(int(kmler[1]) > int(kmler[0])):
            kucuk = int(kmler[0])
            buyuk = int(kmler[1])
        else:
            kucuk = int(kmler[1])
            buyuk = int(kmler[0])

        listem = list(filtered)



    else:
        marka_model_tarih_renk_km = marka_model_tarih_renk_km.split("_")
        listem = list(Car.objects.filter(brand__contains=marka_model_tarih_renk_km[0]).filter(model__contains=marka_model_tarih_renk_km[1]).filter(year__contains=int(marka_model_tarih_renk_km[2])).filter(color__contains=marka_model_tarih_renk_km[3]).filter(km__contains=int(marka_model_tarih_renk_km[4])))


    data = []
    enBuyukFiyat = 0
    enKucukFiyat = 99999999

    for car in listem:
       if int(car.price) > enBuyukFiyat and int(car.km) < buyuk: # <= ti < oldu
           enBuyukFiyat = int(car.price)

       if int(car.price) < enKucukFiyat and int(car.km) >= kucuk and int(car.km) < buyuk:
           enKucukFiyat = int(car.price)


    data.append(enKucukFiyat)
    data.append("^"+str(enBuyukFiyat))

    return HttpResponse(data)


@csrf_exempt
def send_ajax(request):

    marka_model_tarih_renk_km_price = request.body.decode('utf-8')
    if "*" in marka_model_tarih_renk_km_price:
        marka_model_tarih_renk_km_price = marka_model_tarih_renk_km_price.replace("*", " ")

    if "?" in marka_model_tarih_renk_km_price:
        marka_model_tarih_renk_km_price = marka_model_tarih_renk_km_price.split("?")

        marka = marka_model_tarih_renk_km_price[0].split("_")[0]

        modeller = []
        tarihler = []
        renkler = []
        kmler = []
        priceler = []

        for splitted in marka_model_tarih_renk_km_price:
            if (not splitted.split("_")[1] in modeller):
                modeller.append(splitted.split("_")[1])
            if (len(splitted.split("_")) >= 3 and not splitted.split("_")[2] in tarihler):
                tarihler.append(splitted.split("_")[2])
            if (len(splitted.split("_")) >= 4 and not splitted.split("_")[3] in renkler):
                renkler.append(splitted.split("_")[3])
            if (len(splitted.split("_")) >= 5 and not splitted.split("_")[4] in kmler):
                kmler.append(splitted.split("_")[4])
            if(len(splitted.split("_")) == 6 and not splitted.split("_")[5] in priceler):
                priceler.append(splitted.split("_")[5])

        filtered = Car.objects.filter(brand__contains=marka).order_by('date')
        query = Q()

        for model in modeller:
            query |= Q(model__contains=model)

        # filtered = Car.objects.filter(query)

        filtered = filtered.filter(query)

        query = Q()

        for tarih in tarihler:
            query |= Q(year__contains=int(tarih))

        filtered = filtered.filter(query)

        query = Q()
        for renk in renkler:
            query |= Q(color__contains=renk)

        filtered = filtered.filter(query)

        km_kucuk = 0
        km_buyuk = 0

        fiyat_kucuk = 0
        fiyat_buyuk = 0

        if(int(kmler[1]) > int(kmler[0])):
            km_kucuk = int(kmler[0])
            km_buyuk = int(kmler[1])
        else:
            km_kucuk = int(kmler[1])
            km_buyuk = int(kmler[0])

        if(int(priceler[1]) > int(priceler[0])):  #eşit olma ihtimali
            fiyat_kucuk = int(priceler[0])
            fiyat_buyuk = int(priceler[1])
        else:
            fiyat_kucuk = int(priceler[1])
            fiyat_buyuk = int(priceler[0])

        data = []
                                                    # marka  6 -1   aractipgrubu 6 -1     modelyil 7 -2    renk 6 -1     km 7 -2 fiyat 7 -2
        for car in filtered:
            if(int(car.km) >= km_kucuk and int(car.km) < km_buyuk):
                if(int(car.price) >= fiyat_kucuk and int(car.price) < fiyat_buyuk ):
                    data.append(str(car.date)+"_"+car.brand + "_" + car.model + "_" + str(car.year) + "_" + car.color + "_" +str(car.km)+"_"+ str(car.price))

        data = "|".join(data)



    return HttpResponse(data)



