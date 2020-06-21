from django.db import models


class NumVar(models.Model):
    name = models.CharField(max_length=64)
    value = models.DecimalField(default=0.0, max_digits=7, decimal_places=3)

    def __str__(self):
        return self.name + ': ' + str(self.value)


class StrVar(models.Model):
    name = models.CharField(max_length=64)
    value = models.CharField(max_length=254)

    def __str__(self):
        return self.name + ': ' + self.value


class OffDay(models.Model):
    from_day = models.DateField('from day')
    to_day = models.DateField('to day')

    def __str__(self):
        return str(self.from_day) + ' - ' + str(self.to_day)


class WorkDay(models.Model):
    day = models.DateField('work day')
    hours = models.IntegerField(default=8)

    def __str__(self):
        return str(self.day) + ': ' + str(self.hours) + ' hours'
