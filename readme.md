Flask Full Text Search using Postgres
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
```
