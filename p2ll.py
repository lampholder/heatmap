import sys, csv
from postcode import parse_uk_postcode

outcodes = {}

# 1,AB10,57.131086,-2.122482
with open('postcodes.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    outcodes = {outcode: (lat, lng) for _, outcode, lat, lng in reader}

# arthur smith,389 chiswick High Road,w44al,YES,447890123123,5.00,SMS
with open('data/good.csv', 'rb') as datafile:
    reader = csv.reader(datafile)
    donations = [(parse_uk_postcode(postcode, strict=False)[0], tarrif) for (name, address, postcode, giftaid, msisdn, tarrif, method) in reader]

writer = csv.writer(sys.stdout)
writer.writerow(['lat', 'lon', 'value'])
for outcode, tarrif in donations:
    if outcode in outcodes:
        lat, lng = outcodes[outcode]
        writer.writerow([lat, lng, 1])
