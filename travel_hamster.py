import sys
import csv
import json
import itertools
import urllib2

from bs4 import BeautifulSoup

class Hamster(object):
    def __init__(self, plan):
        self.plan = plan

    def parse_duration(self, dur):
        hours = 0
        for part in dur.split(' '):
            if part.endswith('hrs'):
                hours += float(part[:-3])
            elif part.endswith('min'):
                hours += float(part[:-3])/60.0
            else:
                raise ValueError
        return hours

    def parse_r2r(self, p):
        uri = 'http://free.rome2rio.com/s/{from}/{to}'.format(**p)
        uri += '?dates={leave_date}/{return_date}'.format(**p)
        page = urllib2.urlopen(uri)
        soup = BeautifulSoup(page.read())
        itins = soup.findAll('li', {'class': 'itinerary'})
        options = []
        for i in itins:
            dl = i.find('div', {'class': 'itinerary-short'}).find('dl')
            data = {}
            data['source'] = uri
            for dd in dl.findAll('dd'):
                cl = dd.get('class')[0]
                if cl == 'itinerary-title':
                    data['mode_desc'] = dd.text
                elif cl == 'itinerary-time':
                    data['travel_hours'] = self.parse_duration(dd.text)
                elif cl == 'itinerary-price':
                    parts = dd.text.split(u'\xa0-\xa0')
                    data['travel_price_min'] = parts[0]
                    data['travel_price_max'] = parts[1]
                elif cl == 'itinerary-mode':
                    modes = []
                    for img in dd.findAll('i'):
                        mode = img.get('class')[0].replace('icon-', '').replace('-sprite', '')
                        modes.append(mode)
                    data['modes'] = ', '.join(modes)
            options.append(data)
        return options

    def gen_options(self):
        for dest in plan['to']:
            currplan = dict(plan)
            currplan['from'] = plan['home']
            currplan['to'] = dest
            r2r_options = self.parse_r2r(currplan)
            for opt in r2r_options:
                rowdata = dict(currplan)
                rowdata.update(opt)
                rowdata['has_car'] = rowdata['modes'].endswith('car')
                yield rowdata

    def print_options(self):
        cols = ['to', 'mode_desc', 'modes', 'travel_hours', 'travel_price_min', 'travel_price_max', 'leave_date', 'return_date', 'has_car', 'source']
        writer = csv.DictWriter(sys.stdout, cols, extrasaction='ignore')
        writer.writeheader()

        for opt in self.gen_options():
            writer.writerow(opt)


plan = json.load(open(sys.argv[1]))
h = Hamster(plan)
h.print_options()
