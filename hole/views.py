from django.shortcuts import render
from hole.models import Reset, Ie, Status, Equip, Area
from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse
from datetime import datetime
from operator import itemgetter
import xlwt


def index(request):
    reset = Reset.objects.all()
    crv_1 = Equip.objects.all()[53:56]
    tk_ck_1 = Equip.objects.all()[4:22]
    tk_ck_2 = Equip.objects.all()[22:28]
    ktk = Equip.objects.all()[28:39]
    tg = Equip.objects.all()[39:53]
    ska = Equip.objects.all()[67:70]
    vru = Equip.objects.all()[:4]
    cks_1 = Equip.objects.all()[56:60]
    cks_2 = Equip.objects.all()[62:64]
    kvu = Equip.objects.all()[60:62]
    atk = Equip.objects.all()[65:67]
    ktk1 = Equip.objects.all()[64]
    return render(request, "hole/homepage.html",
                  context={"reset": reset,
                           "vru": vru,
                           "crv_1": crv_1,
                           "tk_ck_1": tk_ck_1,
                           "tk_ck_2": tk_ck_2,
                           "ktk": ktk,
                           "tg": tg,
                           "cks_1": cks_1,
                           "cks_2": cks_2,
                           "kvu": kvu,
                           "atk": atk,
                           "ktk1": ktk1,
                           "ska": ska})


def resume(request):
    reset = Reset.objects.all()
    equip = Equip.objects.all()
    stat = Status.objects.all()
    area = Area.objects.all()
    crv_1 = Equip.objects.all()[53:56]
    tk_ck_1 = Equip.objects.all()[4:22]
    tk_ck_2 = Equip.objects.all()[22:28]
    ktk = Equip.objects.all()[28:39]
    tg = Equip.objects.all()[39:53]
    ska = Equip.objects.all()[67:70]
    vru = Equip.objects.all()[:4]
    cks_1 = Equip.objects.all()[56:60]
    cks_2 = Equip.objects.all()[62:64]
    kvu = Equip.objects.all()[60:62]
    atk = Equip.objects.all()[65:67]
    ktk1 = Equip.objects.all()[64]
    time = [i for i in range(1, 30)]
    return render(request, 'hole/resume.html',
                  context={"reset": reset,
                           "vru": vru,
                           "crv_1": crv_1,
                           "tk_ck_1": tk_ck_1,
                           "tk_ck_2": tk_ck_2,
                           "ktk": ktk,
                           "tg": tg,
                           "cks_1": cks_1,
                           "cks_2": cks_2,
                           "kvu": kvu,
                           "atk": atk,
                           "ktk1": ktk1,
                           "ska": ska,
                           "equip": equip,
                           "status": stat,
                           "area": area,
                           "time": time})


# def get_month_biography(request):
#     d = []
#     unit_object_list = Reset.objects.filter(equip_short_name_id=13)
#     for i in range(1, 30):
#         pass
#     return d
#
#
# def get_day_biography(unit_object_list, day):
#
#     status = 'В резерве'
#     return status


def analysis(request):
    equip = Equip.objects.all()
    res = Reset.objects.all()
    return render(request, "hole/analysis.html", context={'all_resets': res, "all_equip": equip})


def analysis_unit(request):
    all_records = []
    unit = Equip.objects.get(id=1)
    if request.method == "POST":
        unit = Equip.objects.get(short_name=request.POST.get('short_name'))
        filtered_units = Reset.objects.filter(equip_short_name_id=unit.id)
        if len(filtered_units) == 0:
            all_records = [{'datetime': 'нет данных', 'status': 'нет даных', 'duration': 'нет даных',
                            'comment': "No comments", 'remark': ""}]
        elif len(filtered_units) == 1:
            single = filtered_units.first()
            all_records = [{'datetime': datetime.combine(single.data, single.time),
                            'status': single.new_status, 'duration': 'В процессе',
                            'comment': single.comment, 'remark': ""}]
        else:
            statuses = {1: 'пуск', 2: 'в работе', 3: 'резерв', 4: 'аварийная остановка',
                        5: 'ремонт', 6: 'на сбросе', 7: 'обкатка', 8: 'выход на режим',
                        9: 'отогрев/осушка', 10: 'не эксплуатируется'}
            for i in filtered_units:
                st = statuses.get(i.new_status_id)
                all_records.append({'datetime': datetime.combine(i.data, i.time),
                                    'status': st, 'duration': "В процессе",
                                    'comment': i.comment, 'remark': i.is_expensive_start})
            all_records = sorted(all_records, key=itemgetter('datetime'), reverse=True)
            previous = all_records[0]
            for j in all_records[1:]:
                j.update({'duration': previous['datetime']-j['datetime']})
                previous = j
    return render(request, "hole/analysis_unit.html", context={'records': all_records, 'unit': unit})


def tax(request):
    return render(request, "hole/tax_zone.html")


def one_more(request):
    return render(request, "hole/one_more.html")


def ie_temp(request):
    instr = Ie.objects.all()
    sps = {'ie_all': instr}
    return render(request, "hole/manual.html", context=sps)


def faq(request):
    return render(request, "hole/FAQ.html")


def krz(request):
    return render(request, "hole/krz.html")


def reset_review(request):
    reset = Reset.objects.all()
    return render(request, 'hole/reset_review.html', context={'all_resets': reset})


def reset_new(request):
    equip = Equip.objects.all()
    res = Reset.objects.all()
    status = Status.objects.all()
    return render(request, "hole/reset_new.html", context={'all_resets': res, 'all_status': status, "all_equip": equip})


def create(request):
    if request.method == "POST":
        try:
            reset = Reset()
            reset.equip_short_name = Equip.objects.get(short_name=request.POST.get("short_name"))
            reset.data = request.POST.get("data")
            if reset.data == "":
                reset.data = datetime.today().date()
            reset.time = request.POST.get("time")
            if reset.time == "":
                reset.time = datetime.today().time()
            reset.new_status = Status.objects.get(status_name=request.POST.get("new_status"))
            reset.comment = request.POST.get("comment")
            reset.save()
        except Reset.DoesNotExist:
            return HttpResponseNotFound("<h2>Ошибка ввода</h2>")
    return HttpResponseRedirect("/reset_review")


def rewrite(request):
    if request.method == "POST":
        reset = Reset()
        reset.id = request.POST.get("id")
        reset.equip_short_name = Equip.objects.get(short_name=request.POST.get("short_name"))
        reset.data = request.POST.get("data")
        reset.time = request.POST.get("time")
        reset.new_status = Status.objects.get(status_name=request.POST.get("new_status"))
        reset.comment = request.POST.get("comment")
        reset.save()
    return HttpResponseRedirect("/reset_review")


def edit(request, idi):
    area = Area.objects.all()
    equip = Equip.objects.all()
    stat = Status.objects.all()
    try:
        res = Reset.objects.get(id=idi)
        return render(request, "hole/reset_edit.html", context={"reset": res, "equip": equip,
                                                                "status": stat, "area": area})
    except Reset.DoesNotExist:
        return HttpResponseNotFound("<h2>Переключение not found</h2>")


def delete(request, idi):
    res = Reset.objects.all()
    try:
        reset = Reset.objects.get(id=idi)
        reset.delete()
        return render(request, "hole/reset_review.html", context={'all_resets': res})
    except Reset.DoesNotExist:
        return HttpResponseNotFound("<h2>Переключение not found</h2>")


def export_unit(request, idi):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="equip.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['оборудование', 'дата', 'время', 'новый статус', 'комментарий']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    filtered_units = Reset.objects.filter(equip_short_name_id=idi)
    rows = filtered_units.values_list('equip_short_name__short_name', 'data', 'time',
                                      'new_status__status_name', 'comment')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response


def export_all(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="equip.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['equip_short_name', 'data', 'time', 'new_status', 'comment']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = Reset.objects.all().values_list('equip_short_name__short_name', 'data',
                                           'time', 'new_status__status_name', 'comment')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    return response
