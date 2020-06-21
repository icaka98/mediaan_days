from django.shortcuts import render, redirect
from decimal import Decimal
from django.contrib.auth.models import User
from main_days.models import OffDay, StrVar, NumVar, WorkDay

import datetime
from pytz import timezone

VACATION_DAYS = 15

PERIODS = [
    (datetime.datetime.strptime('2018-03-09', '%Y-%d-%m'), datetime.datetime.strptime('2018-28-10', '%Y-%d-%m')),
    (datetime.datetime.strptime('2018-29-10', '%Y-%d-%m'), datetime.datetime.strptime('2019-06-01', '%Y-%d-%m')),
    (datetime.datetime.strptime('2019-07-01', '%Y-%d-%m'), datetime.datetime.strptime('2019-03-02', '%Y-%d-%m')),
    (datetime.datetime.strptime('2019-04-02', '%Y-%d-%m'), datetime.datetime.strptime('2019-07-04', '%Y-%d-%m')),
    (datetime.datetime.strptime('2019-08-04', '%Y-%d-%m'), datetime.datetime.strptime('2019-09-06', '%Y-%d-%m')),
    (datetime.datetime.strptime('2019-10-06', '%Y-%d-%m'), datetime.datetime.strptime('2019-05-07', '%Y-%d-%m'))
]

EXAMS = [
    (datetime.datetime.strptime('2018-22-10', '%Y-%d-%m'), datetime.datetime.strptime('2018-26-10', '%Y-%d-%m')),
    (datetime.datetime.strptime('2018-17-12', '%Y-%d-%m'), datetime.datetime.strptime('2018-21-12', '%Y-%d-%m')),
    (datetime.datetime.strptime('2019-01-04', '%Y-%d-%m'), datetime.datetime.strptime('2019-05-04', '%Y-%d-%m')),
    (datetime.datetime.strptime('2019-03-06', '%Y-%d-%m'), datetime.datetime.strptime('2019-07-06', '%Y-%d-%m'))
]


def get_exam_info():
    return 'Exams 1: (' + '{:%B %d %Y}'.format(EXAMS[0][0]) + '/' + '{:%B %d %Y}'.format(EXAMS[0][1]) + '); ' + \
           'Exams 2: (' + '{:%B %d %Y}'.format(EXAMS[1][0]) + '/' + '{:%B %d %Y}'.format(EXAMS[1][1]) + '); ' + \
           'Exams 3: (' + '{:%B %d %Y}'.format(EXAMS[2][0]) + '/' + '{:%B %d %Y}'.format(EXAMS[2][1]) + '); ' + \
           'Exams 4: (' + '{:%B %d %Y}'.format(EXAMS[3][0]) + '/' + '{:%B %d %Y}'.format(EXAMS[3][1]) + '); '


def get_periods_info():
    return 'Period 1: (' + '{:%B %d %Y}'.format(PERIODS[0][0]) + '/' + '{:%B %d %Y}'.format(PERIODS[0][1]) + '); ' + \
           'Period 2: (' + '{:%B %d %Y}'.format(PERIODS[1][0]) + '/' + '{:%B %d %Y}'.format(PERIODS[1][1]) + '); ' + \
           'Period 3: (' + '{:%B %d %Y}'.format(PERIODS[2][0]) + '/' + '{:%B %d %Y}'.format(PERIODS[2][1]) + '); ' + \
           'Period 4: (' + '{:%B %d %Y}'.format(PERIODS[3][0]) + '/' + '{:%B %d %Y}'.format(PERIODS[3][1]) + '); ' + \
           'Period 5: (' + '{:%B %d %Y}'.format(PERIODS[4][0]) + '/' + '{:%B %d %Y}'.format(PERIODS[4][1]) + '); ' + \
           'Period 6: (' + '{:%B %d %Y}'.format(PERIODS[5][0]) + '/' + '{:%B %d %Y}'.format(PERIODS[5][1]) + '); '


def is_off_date(date, off_periods):
    for off_period in off_periods:
        if off_period.from_day <= date.date() <= off_period.to_day:
            print('{} {}'.format(off_period.from_day, off_period.to_day))
            return True
    return False


def is_exam_week(date):
    for i in range(0, 4):
        if EXAMS[i][0] <= date <= EXAMS[i][1]:
            return True
    return False


def get_period_days_per_week(date):
    for i in range(0, 6):
        if PERIODS[i][0] <= date <= PERIODS[i][1]:
            if i in (2, 5):
                return 0, 1, 2, 3  # during 3rd or 6th period
            else:
                return 2, 3  # during regular periods with courses
    return 1, 2, 3, 4, 5  # after period 6


def get_period(date):
    for i in range(0, 6):
        if PERIODS[i][0] <= date <= PERIODS[i][1]:
            return i + 1
    return 0


def get_last_day(days):
    date = datetime.datetime.now()
    off_periods = OffDay.objects.all()

    while days > 0:
        date += datetime.timedelta(days=1)

        if date.weekday() in get_period_days_per_week(date) \
                and not is_off_date(date, off_periods) \
                and not is_exam_week(date):
            days -= 1

    return date + datetime.timedelta(days=1)


def index(request):
    all_days_off = OffDay.objects.all()
    all_work_days = WorkDay.objects.all()
    days_left = NumVar.objects.get(name='days_left')
    hours_left = str(float((days_left.value - VACATION_DAYS) * 8)).rstrip('0').rstrip('.')
    days_left_value = str(float(days_left.value) - VACATION_DAYS).rstrip('0').rstrip('.')

    last_day = get_last_day(days_left.value - VACATION_DAYS)
    week = ['MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN']
    today = datetime.datetime.now().astimezone(timezone('Europe/Amsterdam'))

    ctx = {
        'all_days_off': all_days_off,
        'all_work_days': all_work_days,
        'days_left': days_left_value,
        'hours_left': hours_left,
        'last_day': week[int(last_day.weekday())] +
                    ' ' + last_day.strftime('%d-%m-%Y'),
        'date': today.strftime('%a').upper() + ' ' + today.strftime('%d-%m-%Y'),
        'time': today.strftime('%H:%M:%S'),
        'period_num': get_period(today.replace(tzinfo=None)),
        'periods_info': get_periods_info(),
        'exams_info': get_exam_info(),
        'vacation_left': VACATION_DAYS,
        'is_not_mobile': not request.user_agent.is_mobile
    }

    return render(request, 'main_days/index.html', ctx)


def add_work_day(request):
    work_date = datetime.datetime.strptime(request.GET['date'], '%d-%m-%Y')
    hours = int(request.GET['hours'])
    WorkDay.objects.create(day=work_date, hours=hours)

    hours_var = NumVar.objects.get(name='days_left')
    hours_var.value -= Decimal(hours / 8.0)
    hours_var.save()

    return redirect('/')


def add_from_to(request):
    from_date = datetime.datetime.strptime(request.GET['from'], '%d-%m-%Y')
    to_date = datetime.datetime.strptime(request.GET['to'], '%d-%m-%Y')
    OffDay.objects.create(from_day=from_date, to_day=to_date)

    return redirect('/')
