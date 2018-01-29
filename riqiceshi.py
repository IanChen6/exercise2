# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     
   Description :
   Author :       ianchen
   date：          
-------------------------------------------------
   Change Activity:
                   2017/11/22:
-------------------------------------------------
"""

import datetime


def getYesterday():
    today = datetime.date.today()
    oneday = datetime.timedelta(days=92)
    yesterday = today - oneday
    return yesterday,today


# 输出
y,t=getYesterday()
print(y,t)
y=y.strftime("%Y%m%d")
t=t.strftime("%Y%m%d")
print(y,t)
pass

# def get_now_time():
#     now = datetime.datetime.now()
#     thisyear = int(now.year)
#     thismon = int(now.month)
#     thisday = int(now.day)
#     thishour = int(now.hour)
#     thisminute = int(now.minute)
#     thissecond = int(now.second)
#     return thisyear, thismon, thisday, thishour, thisminute, thissecond
#
#
# def get_year_and_month(n=0):
#     '''
#     get the year, month, days from today before or after n months
#     '''
#     now = datetime.datetime.now()
#     thisyear, thismon, thisday, thishour, thisminute, thissecond = get_now_time()
#     totalmon = thismon+n
#
#     if(n>=0):
#         if(totalmon<=12):
#             days = str(get_days_of_month(thisyear,totalmon))
#             totalmon = add_zero(totalmon)
#             return (thisyear, totalmon, days, thishour, thisminute, thissecond, thisday)
#         else:
#             i = totalmon/12
#             j = totalmon%12
#             if(j==0):
#                 i-=1
#                 j=12
#             thisyear += i
#             days = str(get_days_of_month(thisyear,j))
#             j = add_zero(j)
#             return (str(thisyear),str(j),days, thishour,thisminute, thissecond, thisday)
#     else:
#         if((totalmon>0) and (totalmon<12)):
#             days = str(get_days_of_month(thisyear,totalmon))
#             totalmon = add_zero(totalmon)
#             return (thisyear,totalmon,days, thishour, thisminute, thissecond, thisday)
#         else:
#             i = totalmon/12
#             j = totalmon%12
#             if(j==0):
#                 i-=1
#                 j=12
#             thisyear +=i
#             days = str(get_days_of_month(thisyear,j))
#             j = add_zero(j)
#             return (str(thisyear),str(j),days, thishour, thisminute, thissecond, thisday)
#
# def get_days_of_month(year,mon):
#     return calendar.monthrange(year, mon)[1]
#
# def add_zero(n):
#     '''
#     add 0 before 0-9
#     return 01-09
#     '''
#     nabs = abs(int(n))
#     if (nabs < 10):
#         return "0" + str(nabs)
#     else:
#         return nabs
#
#
# def get_today_months(n=0):
#     year, mon, d, hour, minute, second, day = get_year_and_month(n)
#     arr = (year, mon, d, hour, minute, second, day)
#     print(arr)
#     if (int(day) < int(d)):
#         arr = (year, mon, day, hour, minute, second)
#     return "-".join("%s" % i for i in arr)
#
# get_today_months(-3)