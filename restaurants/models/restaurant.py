from datetime import datetime

from geopy.geocoders import Nominatim
from restaurants import db
from sqlalchemy.orm import relationship

geolocator = Nominatim(user_agent="ASE-GOOUTSAFE-S4")


class Restaurant(db.Model):
    __tablename__ = 'Restaurant'

    MAX_STRING_LENGTH = 100

    # taken from Google Maps bounds
    MAX_LAT = 90
    MIN_LAT = -90
    MAX_LON = 180
    MIN_LON = -180

    MAX_PHONE_LEN = 25

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    name = db.Column(
        db.String(length=MAX_STRING_LENGTH)
    )
    address = db.Column(
        db.String(length=MAX_STRING_LENGTH)
    )
    city = db.Column(
        db.String(length=MAX_STRING_LENGTH)
    )
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    phone = db.Column(
        db.String(length=MAX_PHONE_LEN)
    )
    menu_type = db.Column(
        db.String(length=MAX_STRING_LENGTH)
    )
    measures = db.Column(db.Unicode(), default="")
    is_open = db.Column(
        db.Boolean,
        default=False
    )
    owner_id = db.Column(
        db.Integer,
    )
    avg_stay = db.Column(
        db.Integer,
    )
    tables = relationship("Table", back_populates="restaurant")
    availabilities = relationship("RestaurantAvailability", back_populates="restaurant")
    ratings = relationship('RestaurantRating', back_populates='restaurant')
    likes = relationship('Like', back_populates='restaurant')

    def serialize(self):
        return dict([(k,v) for k,v in self.__dict__.items() if k[0] != '_'])

    def __init__(self, name, address, city, lat, lon, phone, menu_type):
        Restaurant.check_phone_number(phone)
        self.name = name
        self.address = address
        self.city = city
        self.lat = lat
        self.lon = lon
        self.phone = phone
        self.menu_type = menu_type
        self.avg_stay = 0
        # this can be set to False by LHA
        self.is_open = True

    @staticmethod
    def check_phone_number(phone):
        if len(phone) > Restaurant.MAX_PHONE_LEN or len(phone) <= 0:
            raise ValueError("Invalid phone number")

    @staticmethod
    def check_string_attribute(string_attribute):
        if len(string_attribute) > Restaurant.MAX_STRING_LENGTH or len(string_attribute) <= 0:
            raise ValueError("Invalid attribute length")

    def set_name(self, name):
        Restaurant.check_string_attribute(name)
        self.name = name

    def set_address(self, address):
        Restaurant.check_string_attribute(address)
        self.address = address
        location = geolocator.geocode(address + " " + self.city)
        lat = 0
        lon = 0
        if location is not None:
            lat = location.latitude
            lon = location.longitude
        self.set_lat(lat)
        self.set_lon(lon)

    def set_city(self, city):
        Restaurant.check_string_attribute(city)
        self.city = city
        location = geolocator.geocode(self.address + " " + city)
        lat = 0
        lon = 0
        if location is not None:
            lat = location.latitude
            lon = location.longitude
        self.set_lat(lat)
        self.set_lon(lon)

    def set_lat(self, lat):
        if self.MIN_LAT <= lat <= self.MAX_LAT:
            self.lat = lat
        else:
            raise ValueError("Invalid latitude value")

    def set_lon(self, lon):
        if self.MIN_LON <= lon <= self.MAX_LON:
            self.lon = lon
        else:
            raise ValueError("Invalid longitude value")

    def set_phone(self, phone):
        Restaurant.check_phone_number(phone)
        self.phone = phone

    def set_menu_type(self, menu_type):
        Restaurant.check_string_attribute(menu_type)
        self.menu_type = menu_type

    def set_measures(self, measure):
        self.measures = measure

    def set_is_open(self, is_open):
        self.is_open = is_open

    def likes_count(self):
        return len(self.likes)

    def set_avg_stay(self, avg_stay):
        self.avg_stay = avg_stay

    def is_open_date(self, when=datetime.now()):
        for av in self.availabilities:
            if av.day == av.week_days[when.weekday()]:
                if av.start_time < when.time() < av.end_time:
                    return self.is_open
        return False
