from application import db, app
from application import models

db.drop_all()
db.create_all()
testuser = models.Users(first_name='Kelly',last_name='Felix',city='London',tel='384849',cohort='Cohort23',pathway='DevOps',email='ed@hot.com',password='password',) # Extra: this section populates the table with an example entry
db.session.add(testuser)
db.session.commit()