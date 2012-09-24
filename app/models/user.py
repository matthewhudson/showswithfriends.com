from app.models import db

CAN_VIEW = 1

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column('id', db.Integer, primary_key=True)
    sg_id = db.Column('sg_id', db.Integer)
    name = db.Column(db.String(60))
    permission_mask = db.Column(db.Integer, default=15)
    access_token = db.Column(db.String(200))

    def __init__(self, sg_id = None):
        self.sg_id = sg_id

    def can_view(self):
    	return self.permission_mask & CAN_VIEW
