# *-* coding:utf-8 *-*

import re
import datetime
import calendar

# 20:09:51.225 t 200 8 3F FF 03 3F FF 7F FF FF
expr_log = re.compile(r"(\d+:\d{2}:\d{2}\.\d{3}) t(...)(.)((..){8})")

expr_date = re.compile(r"date (\w+) (\w+) (\d+) ((\d+):(\d{2}):(\d{2})\.(\d{3})) (\d{4})")

fname = "test.asc"

year  = 0
weekday   = "Error"
month_str = "Error"
month_num = 0
fulltime = "Error"
day   = 0
hour  = 0
am_pm = "am"
minute  = 0
sec     = 0
msec    = 0

datefmt = f"date {weekday} {month_str} {day} {fulltime} {am_pm} {year}"

with open(fname) as f:
    #最初の行は日時(date <WeekDay> <Month> <Date> <Fulltime> <Year>)であると決め打ちする。
    s = f.readline()
    m = expr_date.search(s)
    if m:
        # weekday = m.group(1)
        # monthを数値へ変換(e.g.Jul→7)
        # for i ,v in enumerate(calendar.month_abbr):
        #     if v == m.group(2):
        #         month_str = v
        #         month_num = i
        #         break
        
        # day    = int(m.group(3))
        # fulltime = m.group(4)
        # hour   = int(m.group(4))
        # if hour > 12:
        #     hour -= 12
        #     am_pm = "pm"

        # minute = int(m.group(4))
        # sec    = int(m.group(6))
        # msec   = int(m.group(7))
        # year   = int(m.group(8))
        # print(f"{year}-{month_num}-{day} {hour}:{minute}:{sec}.{msec}")
        
        for i in range(m.lastindex):
            print(m.group(i))



header = \
f"""
base hex timestamps absolute
no internal events logged
// version 7.2.1"""

print(header)


with open(fname) as f:
    for s in f:
        m = expr_log.search(s)
        if m:
            print(m.group(1), m.group(2), m.group(3), m.group(4))
            time = m.group(1)
            can_id =  m.group(2)

        
