#!/usr/bin/env python
import gzip
import os
import re
import pandas as pd

INPUT_DIR = "procurement"

list_logs = list()

ip = r"?P<ip>[\d.]*"
date = r"?P<date>\d+"
month = r"?P<month>\w+"
year = r"?P<year>\d+"
time = r"?P<time>\S+"
method = r"?P<method>\S+"
request = r"?P<request>\S+"
status = r"?P<status>\d+"
bodyBytesSent = r"?P<bodyBytesSent>\d+"
refer = r"""?P<refer>
        [^\"]*
        """
userAgent=r"""?P<userAgent>
        [^\"]*
        """

lineformat = re.compile(r"(%s)\ -\ -\ \[(%s)/(%s)/(%s)\:(%s)\ [\S]+\]\ \"(%s)?[\s]?(%s)?.*?\"\ (%s)\ (%s)\ \"(%s)\"\ \"(%s)\"" %( ip, date, month, year, time, method, request, status, bodyBytesSent, refer, userAgent ), re.VERBOSE)

for f in os.listdir(INPUT_DIR):
    if f.endswith(".gz"):
        logfile = gzip.open(os.path.join(INPUT_DIR, f))
    else:
        logfile = open(os.path.join(INPUT_DIR, f))

    for l in logfile.readlines():
        data = re.search(lineformat, l)
        if data:
            datadict = data.groupdict()
            ip = datadict["ip"]
            date = datadict["date"]
            month = datadict["month"]
            year = datadict["year"]
            time = datadict["time"]
            method = datadict["method"]
            request = datadict["request"]
            status = datadict["status"]
            bodyBytesSent = datadict["bodyBytesSent"]
            refer = datadict["refer"]
            userAgent = datadict["userAgent"]
            

            list_logs.append([ip, date, month, year, time, method, request, status, bodyBytesSent, refer, userAgent])
            logs_df = pd.DataFrame(list_logs)
            logs_df.to_csv (r'logs1.csv', index = None)

    logfile.close()

print(list_logs)