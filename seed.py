from app import app
from models import db, User, Feedback
app.app_context().push()


db.drop_all()
db.create_all()

p1 = User(
    username = "testUser1",
    password = "pw1234",
    email = "emailTest1@gmail.com",
    first_name = "fn1",
    last_name = "ln1"
)

p2 = User(
    username = "testUser2",
    password = "pw1234",
    email = "emailTest2@gmail.com",
    first_name = "fn2",
    last_name = "ln2"
)


db.session.add_all([p1, p2])
db.session.commit()