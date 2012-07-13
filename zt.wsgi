activate_this = '/home/zombietracker/.virtualenvs/zombietracker/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

from zombietracker.views import APP as application
application.debug = True
