#!/usr/bin/env python3
# SPDX-FileCopyrightText: Copyright (c) 2022 Evin Dunn
# SPDX-License-Identifier: MIT

import adafruit_ntp
import wifi
import socketpool
import time
import rtc

from adafruit_datetime import datetime

try:
    from tzdb import timezone
except ImportError:
    from sys import path as sys_path
    from pathlib import Path

    sys_path.insert(0, str(Path(__file__).parent.parent))
    from tzdb import timezone


def main():
    TARGETS = [
        "America/Chicago",
        "America/Detroit",
    ]
    
    pool = socketpool.SocketPool(wifi.radio)
    ntp = adafruit_ntp.NTP(pool, tz_offset=0)
    rtc.RTC().datetime = ntp.datetime

    while True:
        # First use adafruit_ntp to fetch the current utc time & update the board's
        # RTC

        utc_now = time.time()
        utc_now_dt = datetime.fromtimestamp(utc_now)

        print("UTC: {}".format(utc_now_dt.ctime()))

        for target in TARGETS:
            localtime = utc_now_dt + timezone(target).utcoffset(utc_now_dt)
            print("{}: {}".format(target, localtime.ctime()))
            
        time.sleep(1)




if __name__ == "__main__":
    main()