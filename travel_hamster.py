import sys
import csv
import json
from datetime import datetime
import itertools
import urllib2
import urllib
import httplib

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
            elif part.endswith('days'):
                hours += float(part[:-4])*24
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

    def get_numbeo_info(self, dest):
        mapping = {
                'New-Orleans': ('New Orleans, LA', 'United States'),
                'Denver': ('Denver, CO', 'United States'),
                'Miami': ('Miami, FL', 'United States'),
                'New-York': ('New York, NY', 'United States'),
                'Seattle': ('Seattle, WA', 'United States'),
                'Chicago': ('Chicago, IL', 'United States'),
                'San-Diego': ('San Diego, CA', 'United States'),
                'Phoenix': ('Phoenix, AZ', 'United States'),
                'Las-Vegas': ('Las Vegas, NV', 'United States'),
            }
        f = {}
        try:
            f['city'], f['country'] = mapping[dest]
        except KeyError:
            return {}
        uri = 'http://www.numbeo.com/hotel-prices/city_result.jsp?%s' % urllib.urlencode(f)

        httplib.HTTPConnection._http_vsn = 10
        httplib.HTTPConnection._http_vsn_str = 'HTTP/1.0'
        data = urllib2.urlopen(uri).read()
        httplib.HTTPConnection._http_vsn = 11
        httplib.HTTPConnection._http_vsn_str = 'HTTP/1.1'

        info = {'numbeo_source': uri}
        for line in data.splitlines():
            if 'Backpacker estimated cost' in line:
                for part in line.split('<p/>')[1:]:
                    part = part.replace('&nbsp;&#36;', '')
                    cost = part.split(' = ')[-1]
                    if 'Backpacker' in part:
                        info['backpacker_cost_per_day'] = cost
                    if 'Business or' in part:
                        info['business_cost_per_day'] = cost
        return info

    def gen_options(self):
        for dest in plan['to']:
            numbeo = self.get_numbeo_info(dest)
            currplan = dict(plan)
            currplan['from'] = plan['home']
            currplan['to'] = dest
            r2r_options = self.parse_r2r(currplan)
            for opt in r2r_options:
                rowdata = dict(currplan)
                rowdata.update(opt)
                rowdata.update(numbeo)
                rowdata['has_car'] = rowdata['modes'].endswith('car')
                leaved = datetime.strptime(rowdata['leave_date'], '%Y-%m-%d').date()
                returnd = datetime.strptime(rowdata['return_date'], '%Y-%m-%d').date()
                rowdata['duration'] = (returnd - leaved).total_seconds()/(60*60*24)
                yield rowdata

    def print_options(self):
        cols = ['to', 'mode_desc', 'modes', 'travel_hours', 'travel_price_min', 'travel_price_max', 'leave_date', 'return_date', 'duration', 'has_car', 'source', 'backpacker_cost_per_day', 'business_cost_per_day', 'numbeo_source']
        writer = csv.DictWriter(sys.stdout, cols, extrasaction='ignore')
        writer.writeheader()

        for opt in self.gen_options():
            writer.writerow(opt)


plan = json.load(open(sys.argv[1]))
h = Hamster(plan)
h.print_options()
