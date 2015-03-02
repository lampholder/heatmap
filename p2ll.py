import sys, csv
from lib.postcode import parse_uk_postcode

outcodes = {}
donations = {}
populations = {}

# 1,AB10,57.131086,-2.122482
with open('data/postcodes.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    outcodes = {outcode: (lat, lng) for _, outcode, lat, lng in reader}
    donation_totals = {outcode: 0 for outcode in outcodes}

# arthur smith,389 chiswick High Road,w44al,YES,447890123123,5.00,SMS
with open('input.csv', 'rb') as datafile:
    reader = csv.reader(datafile)
    donations = [(parse_uk_postcode(postcode, strict=False)[0], int(float(tarrif))) for (name, address, postcode, giftaid, msisdn, tarrif, method) in reader]
    for outcode, tarrif in donations:
        if outcode in donation_totals:
            donation_totals[outcode] += tarrif

with open('data/2011_population.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile)
    reader.next()
    populations = {outcode: int(population) for outcode, population, men, women in reader}

writer = csv.writer(sys.stdout)
writer.writerow(['lat', 'lon', 'value'])
for outcode, total in donation_totals.iteritems():
    if total > 0:
        lat, lng = outcodes[outcode]
        writer.writerow([lat, lng, total])
        #if outcode in populations:
        #    writer.writerow([lat, lng, float(total) / populations[outcode]])
