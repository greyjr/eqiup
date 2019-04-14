from django.db import models


class Area(models.Model):
    name_area = models.CharField(max_length=100)
    name_select = models.CharField(max_length=32, default="area")
    picture_area = models.BinaryField()
    description_area = models.CharField(max_length=2048)

    def __str__(self):
        return self.name_select


class Ie(models.Model):
    name_ie = models.CharField(max_length=20)
    content_ie = models.CharField(max_length=65535)

    def iefile(self):
        return 'ie'+str(self.id) + '.docx'

    def __str__(self):
        return self.name_ie


class Equip(models.Model):
    type_equip = models.CharField(max_length=50)
    short_name = models.CharField(max_length=20, unique=True)
    station_number = models.IntegerField()
    picture_equip = models.BinaryField()
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)
    ie_id = models.ForeignKey(Ie, on_delete=models.CASCADE)

    def __str__(self):
        return self.short_name

    def full_title(self):
        return self.type_equip+' № '+str(self.station_number)

    def get_last_status(self):
        return Reset.objects.filter(equip_short_name_id=self.id).latest('data', 'time').new_status_id

    def get_last_background(self):
        status = Reset.objects.filter(equip_short_name_id=self.id).latest('data', 'time').new_status_id
        cell_background = '#DDDDDD'
        if (status == 5) or (status == 4):
            cell_background = '#E8A2A2'
        if status in (1, 2, 6, 7, 8):
            cell_background = '#38F5A0'
        return cell_background

    def get_last_color(self):
        status = Reset.objects.filter(equip_short_name_id=self.id).latest('data', 'time').new_status_id
        cell_color = '#404040'
        if status == 10:
            cell_color = '#DDDDDD'
        return cell_color


class Staff(models.Model):
    table_number = models.IntegerField()
    surname_name = models.CharField(max_length=255)
    profession = models.CharField(max_length=100)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)


class Status(models.Model):
    status_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.status_name


class Reset(models.Model):
    equip_short_name = models.ForeignKey(Equip, on_delete=models.CASCADE)
    new_status = models.ForeignKey(Status, on_delete=models.CASCADE)
    data = models.DateField()
    time = models.TimeField()
    comment = models.CharField(max_length=2048)

    # def get_last(self):
    #     return Reset.objects.latest('data', 'time')

    def get_area(self):
        equip_name = Equip.objects.get(short_name=self.equip_short_name)
        return Area.objects.get(name_select=equip_name.area_id)

    def get_month(self):
        return ("0" if self.data.month < 10 else "")+str(self.data.month)

    def get_day(self):
        return ("0" if self.data.day < 10 else "")+str(self.data.day)

    def get_hour(self):
        return ("0" if self.time.hour < 10 else "")+str(self.time.hour)

    def get_minute(self):
        return ("0" if self.time.minute < 10 else "")+str(self.time.minute)

    def __str__(self):
        return self.comment

    def tax_value(self):
        a0 = "ночной пуск"
        a1 = "пуск в полупик"
        a2 = "пуск в пик"
        zima = [a0, a0, a0, a0, a0, a0, a1, a1, a2, a2, a1, a1, a1, a1, a1, a1, a1, a2, a2, a2, a2, a1, a1, a0]
        vesna = [a0, a0, a0, a0, a0, a0, a1, a1, a2, a2, a1, a1, a1, a1, a1, a1, a1, a1, a2, a2, a2, a2, a1, a0]
        leto = [a0, a0, a0, a0, a0, a0, a0, a1, a2, a2, a2, a1, a1, a1, a1, a1, a1, a1, a1, a1, a2, a2, a2, a1]
        economy_start = [zima, zima, vesna, vesna, leto, leto, leto, leto, vesna, vesna, zima, zima]
        return economy_start[self.data.month-1][self.time.hour]

    def is_expensive_start(self):
        return "-" if (self.new_status != Status.objects.get(pk=1)) and \
                      (self.new_status != Status.objects.get(pk=7)) else self.tax_value()
        # pk = 1 is Пуск в атмосферу, pk = 7 is Пуск в обкатку

    def get_record(self):
        return [str(self.equip_short_name), self.data, self.time, str(self.new_status)]

    # def get_last_reset_status(self, idi):
    #     last = Reset.objects.filter(equip_short_name_id=idi).latest('data', 'time')
    #     return last.status
    #
    # def get_last_reset_background(self):
    #     cell_color = 4210752
    #     cell_background = 14540253
    #     return
