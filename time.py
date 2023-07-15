import adafruit_datetime

t = "2023-06-27T17:00:00+00:00"

z = adafruit_datetime.datetime.fromisoformat(t)
print(z)
tt = z.timetuple()
print(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'][tt[6]])