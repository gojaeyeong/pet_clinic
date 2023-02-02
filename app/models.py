from app import db

class User(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.Integer, nullable=True)
    user_id = db.Column(db.String(200), nullable=False)
    corporate_registration_number = db.Column(db.Integer, nullable=True)
    clinic_name = db.Column(db.String(150), nullable=True)
    name = db.Column(db.String(200), nullable=False)
    profile_img = db.Column(db.Text(), nullable=True)
    specialist_license_number = db.Column(db.Integer, nullable=True)
    specialist_img = db.Column(db.Text(), nullable=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)

class Profile(db.Model):
    idx = db.Column(db.Integer, primary_key=True)
    idx_user = db.Column(db.Integer,db.ForeignKey('user.idx', ondelete='CASCADE'))
    profile_name = db.Column(db.String(200), nullable=True)
    profile_img = db.Column(db.Text(), nullable=True)
    create_date = db.Column(db.DateTime(), nullable=False)