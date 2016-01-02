from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy_searchable import SearchQueryMixin
from sqlalchemy_utils.types import TSVectorType
from sqlalchemy_searchable import make_searchable

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
    __table_name__ = 'documenttest'
    query_class = DocumentQuery
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), unique=True)
    description = db.Column(db.Text)
    cat = db.Column(db.Text)

    search_vector = db.Column(TSVectorType('title', 'description'))

    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __repr__(self):
        return '<Document %r>' % self.title


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form['search_term']
        results = Document.query.search(search_term)
        return render_template('search_results.html', results=results, search_term=search_term)
    else:
        return render_template('search.html')


if __name__ == '__main__':
    app.debug = True
    # app.run()
    manager.run()
