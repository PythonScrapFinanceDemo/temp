from datetime import date, timedelta as td

d1 = date(2008, 8, 15)
d2 = date(2008, 9, 15)

delta = d2 - d1
date_list = []
for i in range(delta.days + 1):
    date_list.append(d1 + td(days=i))

print(date_list)
