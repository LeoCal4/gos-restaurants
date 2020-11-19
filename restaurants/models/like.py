import datetime

from sqlalchemy.orm import relationship

from restaurants import db


class Like(db.Model):
    __tablename__ = 'Like'

    liker_id = db.Column(
        db.Integer,
        primary_key=True
    )

    restaurant_id = db.Column(
        db.Integer,
        db.ForeignKey(
            'Restaurant.id',
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    restaurant = relationship(
        'Restaurant',
        back_populates='likes'
    )

    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, *args, **kw):
        super(Like, self).__init__(*args, **kw)
    
    def serialize(self):
        return dict([(k,v) for k,v in self.__dict__.items() if k[0] != '_'])
