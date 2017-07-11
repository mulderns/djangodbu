# -*- coding: utf-8 -*-
''' Ago - datetime generator helper

    ago.days(3) -> Datetime three days ago
    ...
    ago.weeks
    ago.months
    ago.years
 '''
from datetime import datetime, timedelta

def days(numdays):
    return datetime.now() - timedelta(days=numdays)

def weeks(numweeks):
    return datetime.now() - timedelta(days=numweeks*7)

def months(nummonths):
    '''uses 30 days as a month'''
    return datetime.now() - timedelta(days=nummonths*30)

def years(numyears):
    '''uses 365 days as a year'''
    return datetime.now() - timedelta(days=numyears*365)
