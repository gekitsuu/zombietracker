from flask import Flask, render_template
from models import Database

APP = Flask(__name__)
APP.secret_key = '225B6F5A-8622-45E5-8FEF-4A913D8FF0F8'
DB = Database()


@APP.route('/')
def index():
    """Main Page"""
    mapurl = DB.get_sighting_map()
    return render_template('index.html',
        mapurl=mapurl,
        headers={'content-type': 'application/vnd.google-earth.kml+xml'})


def main():
    '''Main'''
    APP.debug = True
    APP.run(host='0.0.0.0', port=80)

if __name__ == "__main__":
    main()
