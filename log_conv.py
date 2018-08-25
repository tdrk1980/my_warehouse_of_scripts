# *-* coding:utf-8 *-*

import re
import datetime
import calendar


fname_list = [
    "test"
]

ch = 1 # 固定。元のログにない

for basename in fname_list:
    outfname = basename + "_conv.asc"
    fname = basename + ".log"

    with open(outfname, "w") as of:
        #
        # ファイルヘッダ部分
        # 
        expr_date = re.compile(r"date (\w+) (\w+) (\d+) ((\d+):(\d{2}):(\d{2})\.(\d{3})) (\d{4})")

        year  = 0
        weekday_str   = "Error"
        month_str = "Error"
        month = 0
        fulltime_str = "Error"
        day   = 0
        hour_12fmt  = 0
        hour_24fmt = 0
        am_pm_str = "am"
        minute  = 0
        sec     = 0
        msec    = 0

        with open(fname) as f:
            #最初の行は日時(date <WeekDay> <Month> <Date> <Fulltime> <Year>)であると決め打ちする。
            s = f.readline()
            m = expr_date.search(s)
            if m:
                # for i in range(m.lastindex+1):
                #   print(i, m.group(i))
                
                weekday_str = m.group(1)
                
                # month
                for i ,v in enumerate(calendar.month_abbr):
                    if v == m.group(2):
                        month_str = v
                        month = i
                        break
                
                day    = int(m.group(3))
                fulltime_str = m.group(4)
                hour_24fmt   = int(m.group(5))
                if hour_24fmt > 12:
                    hour_12fmt = hour_24fmt - 12
                    am_pm_str = "pm"
                minute = int(m.group(6))
                sec    = int(m.group(7))
                msec   = int(m.group(8))
                year   = int(m.group(9))
                # print(f"{year}-{month_num}-{day} {hour}:{minute}:{sec}.{msec}")
            
        fmt_date = f"{weekday_str} {month_str} {day} {hour_12fmt:02}:{minute:02}:{sec:02}.{msec:03} {am_pm_str} {year}"
        header = f"""date {fmt_date}
base hex timestamps absolute
no internal events logged
// version 9.0.0
Begin TriggerBlock {fmt_date}"""

        # print(header)
        of.write(header + "\n")


        # ログ部分の出力時に使う日時
        start_datetime = datetime.datetime(year=year, month=month, day=day, hour=hour_24fmt, minute=minute, second=sec, microsecond=msec*1000)


        #
        # ログ部分
        #

        # Start of measurementは決めうち
        # print("   0.000000 Start of measurement")
        of.write("   0.000000 Start of measurement" + "\n")

        # 20:45:34.096 t20083FFF033FFF7FFFFF
        # を↓のように正規表現でパースして、
        # 20:45:34.096 t 200 8 3F FF 03 3F FF 7F FF FF
        # いろいろやることで↓のようにする。
        #  0.586869 1  200             Rx   d 8 3F FF 03 3F FF 7F FF FF

        expr_log = re.compile(r"(\d+):(\d{2}):(\d{2})\.(\d{3}) t(...)(.)((..){8})")

        timestamp = 0.0
        can_id = 0
        dlc = 0
        data_str = ""

        with open(fname) as f:
            for s in f:
                m = expr_log.search(s)
                if m:
                    # for i in range(m.lastindex+1):
                    #     print(i, m.group(i))
                
                    tmp_hour = int(m.group(1))
                    tmp_min  = int(m.group(2))
                    tmp_sec  = int(m.group(3))
                    tmp_msec = int(m.group(4))
                    current_datetime = datetime.datetime(year=year, month=month, day=day, hour=tmp_hour, minute=tmp_min, second=tmp_sec, microsecond=tmp_msec*1000)
                    
                    timestamp = (current_datetime - start_datetime).total_seconds()
                    can_id = int(m.group(5),16)
                    dlc    = int(m.group(6))

                    data_str = m.group(7)
                    data_str = [data_str[i: i+2] for i in range(0, len(data_str), 2)]
                    data_str = " ".join(data_str)

                    fmt_log = f"{timestamp:>11.6f} {ch:<2} {can_id:3X}             Rx   d {dlc:1} {data_str}"
                    of.write(fmt_log)
                    of.write("\n")


        #
        # ファイルフッタ部分の作成
        # 
        # print("End TriggerBlock")
        of.write("End TriggerBlock")