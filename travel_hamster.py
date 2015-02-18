import sys
import json
import urllib2

from bs4 import BeautifulSoup

class Hamster(object):
    def __init__(self, plan):
        self.plan = plan

    def parse_r2r(self, p):
        uri = 'http://free.rome2rio.com/s/{from}/{to}'.format(**p)
        page = urllib2.urlopen(uri)
        soup = BeautifulSoup(page.read())
        itins = soup.findAll('li', {'class': 'itinerary'})
        options = []
        for i in itins:
            dl = i.find('div', {'class': 'itinerary-short'}).find('dl')
            data = {}
            for dd in dl.findAll('dd'):
                cl = dd.get('class')[0]
                if cl == 'itinerary-title':
                    data['mode_desc'] = dd.text
                elif cl == 'itinerary-time':
                    data['travel_time'] = dd.text
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
            print data
            options.append(data)

    def print_options(self):
        for dest in plan['to']:
            currplan = plan
            currplan['to'] = dest
            r2r_data = self.parse_r2r(currplan)
            #print currplan


plan = json.load(open(sys.argv[1]))
h = Hamster(plan)
h.print_options()
