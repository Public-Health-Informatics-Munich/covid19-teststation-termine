from datetime import datetime

from peewee import Model, CharField, DatabaseProxy, ForeignKeyField, BooleanField, DateTimeField, IntegerField, \
    CompositeKey, DateField

from playhouse.postgres_ext import JSONField

from config import config

db_proxy = DatabaseProxy()


class Migration(Model):
    version = IntegerField()

    class Meta:
        database = db_proxy


class TimeSlot(Model):
    start_date_time = DateTimeField()
    length_min = IntegerField()

    class Meta:
        database = db_proxy


class Appointment(Model):
    claim_token = CharField(null=True)
    claimed_at = DateTimeField(null=True)
    booked = BooleanField()
    time_slot = ForeignKeyField(TimeSlot, backref='appointments')

    class Meta:
        database = db_proxy


class Booking(Model):
    surname = CharField()
    first_name = CharField()
    phone = CharField()
    street = CharField(null=True)
    street_number = CharField(null=True)
    post_code = CharField(null=True)
    city = CharField(null=True)
    birthday = DateField(null=True)
    reason = CharField(null=True)
    appointment = ForeignKeyField(Appointment)
    office = CharField()
    secret = CharField()
    booked_by = CharField()
    booked_at = DateTimeField(null=True, default=lambda: datetime.now(tz=config.Settings.tz).replace(tzinfo=None))

    class Meta:
        database = db_proxy


class User(Model):
    user_name = CharField(unique=True)
    salt = CharField()
    password = CharField()
    role = CharField()
    coupons = IntegerField()
    type = CharField(null=False, default='internal')

    class Meta:
        database = db_proxy


class SlotCode(Model):
    date = DateField()
    secret = CharField()

    class Meta:
        database = db_proxy
        primary_key = CompositeKey('date', 'secret')


class FrontendConfig(Model):
    config = JSONField()

    class Meta:
        database = db_proxy

tables = [TimeSlot, Appointment, Booking, User, SlotCode, FrontendConfig, Migration]
