import BeautifulSoup
import re
import urllib2
import simplekml
from geoloc import get_cords
from models import Database

conn = Database()
BASEURL = "http://minecraft-server-list.com/page/%d/"


def findsightings():
    for x in range(1, 21):
        url = BASEURL % x
        opener = BeautifulSoup.BeautifulSoup(urllib2.urlopen(url))
        for elems in opener.findAll('tr'):
            host = elems.find('strong')
            cords = None
            try:
                result = host.text
                result = re.sub('^IP:', '', result)
                cords = get_cords(result)
            except:
                pass

            if cords:
                conn.add_sighting(cords)


# print conn.get_sighting_map()

def make_kml(filename):
    kml = simplekml.Kml()
    result = []
    sightings = conn.get_sightings()
    for sighting in sightings:
        newpoint = kml.newpoint()
        newpoint.name = 'Zombie Sighting'
        print sighting
        newpoint.coords = [sighting]
    kml.save("static/" + filename)

make_kml('zombies.kml')