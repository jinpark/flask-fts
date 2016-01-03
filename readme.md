Flask Full Text Search with nearby search using Postgres and PostGIS
---

1. `pip install -r requirements.txt`

2. Change `SQLALCHEMY_DATABASE_URI`

3. run before you start
```
from app import db
from sqlalchemy.orm.mapper import configure_mappers
configure_mappers()
db.create_all()
```

4. `python app.py`

Test data
```
a = Document('cat', 'meow purr hiss growl')
b = Document('dog', 'bark growl')
c = Document('growl', 'cat dog')

db.session.add(a)
db.session.add(b)
db.session.add(c)
db.session.commit()

d = Place('dcamp', 'study coworking', 37.50789, 127.04529)
e = Place('maru180', 'party space', 37.495419, 127.038849)
f = Place('brians coffee', 'cafe cool', 37.48391, 127.046063)

db.session.add(d)
db.session.add(e)
db.session.add(f)
db.session.commit()


```
