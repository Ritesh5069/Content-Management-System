from project import db

# creating database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    full_name = db.Column(db.String(40), nullable=False)
    phone_number = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(60))
    city = db.Column(db.String(20))
    state = db.Column(db.String(20))
    country = db.Column(db.String(20))
    admin = db.Column(db.Boolean)
    token_key = db.Column(db.String(80))


    def __repr__(self):
        return f"User('{self.full_name}','{self.email}','{self.phone_number}')"

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    summary = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer)

    def __repr__(self):
        return f"User('{self.title}','{self.summary}')"