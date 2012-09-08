import BeautifulSoup
import re
import urllib2
from zombietracker.geoloc import get_cords
from zombietracker.models import Database

conn = Database()
BASEURL = "http://minecraft-server-list.com/page/%d/"


def findsightings():
    for x in range(1, 5):
        url = BASEURL % x
        opener = BeautifulSoup.BeautifulSoup(urllib2.urlopen(url))
        for elems in opener.findAll('tr'):
            host = elems.find('div', {'class': 'adressen online'})
            print(host)
            cords = None
            try:
                result = host.text
                result = re.sub('^IP:', '', result)
                cords = get_cords(result)
            except:
                pass

            if cords:
                conn.add_sighting(cords)


findsightings()
