from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy import func
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable, SearchQueryMixin, search
from geoalchemy2 import Geometry, Geography, WKTElement

from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://jinpark:password1@localhost:5432/flask_fts_local'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

make_searchable()

class DocumentQuery(BaseQuery, SearchQueryMixin):
    pass

class Document(db.Model):
    query_class = DocumentQuery
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    description = db.Column(db.Text)
    search_vector = db.Column(TSVectorType('title', 'description'))

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return '<Document %r>' % self.title

class PlaceQuery(BaseQuery, SearchQueryMixin):
    pass

class Place(db.Model):
    query_class = PlaceQuery
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    description = db.Column(db.Text)
    search_vector = db.Column(TSVectorType('title', 'description'))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    point = db.Column(Geography(geometry_type='POINT', srid=4326))

    def __init__(self, title, description, latitude, longitude):
        self.title = title
        self.description = description
        self.latitude = latitude
        self.longitude = longitude
        self.point = "SRID=4326;POINT({} {})".format(latitude, longitude)

    def __repr__(self):
        return '<Place %r>' % self.title


@app.route('/search', methods=['GET', 'POST'])
def search_text():
    if request.method == 'POST':
        search_term = request.form['search_term']
        results = Document.query.search(search_term)
        return render_template('search_results.html', results=results, search_term=search_term)
    else:
        return render_template('search.html')

@app.route('/search_place', methods=['GET', 'POST'])
def search_place():
    if request.method == 'POST':
        search_term = request.form['search_term']
        distance = request.form['distance']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        point = WKTElement('POINT({0} {1})'.format(latitude, longitude), srid=4326)
        results = search(db.session.query(Place).filter(func.ST_DWithin(Place.point, point, float(distance))), search_term)
        return render_template('search_place_results.html', results=results, search_term=search_term, distance=distance, latitude=latitude, longitude=longitude)
    else:
        return render_template('search_place.html')


if __name__ == '__main__':
    app.debug = True
    # app.run()
    manager.run()
