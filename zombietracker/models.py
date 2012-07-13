from pymongo import Connection
import json
import os.path

dbconfig = json.loads(open(os.path.expanduser('~/zombietracker/configs/dbcreds.json')).read())


def gmaps_img(points):
    GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=800x400&sensor=true"
    pointlist = ""
    for point in points:
        pointlist += "&markers={0},{1}".format(point[0], point[1])

    return GMAPS_URL + pointlist


class Database:
    def __init__(self):
        mongo_loc = dbconfig['mongouri']
        for x in ['\%PASSWORD\%', '\%USERNAME\%', '\%IP\%']:
            if x in mongo_loc:
                raise ValueError("%s hasn't been set in db config file" % x)
        self.db = Connection(host=mongo_loc).zombietracker

    def add_sighting(self, sighting):
        cur = self.db.sightings.find_one({'name': 'zombietracker'})
        try:
            cur['sightings'].append(sighting)
        except KeyError:
            cur['sightings'] = [sighting]
        self.db.sightings.update({'name': 'zombietracker'}, cur)

    def get_sighting_map(self, query={}):
        cur = self.db.sightings.find_one(query)
        return gmaps_img(cur['sightings'][:20])

    def get_sightings(self, query={}):
        return self.db.sightings.find_one(query)['sightings']
