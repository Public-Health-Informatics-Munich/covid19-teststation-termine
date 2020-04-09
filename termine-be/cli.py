import logging
import sys
from datetime import datetime, timedelta

import hug

from peewee import fn

from access_control.access_control import UserRoles
from db.directives import PeeweeContext, PeeweeSession, init_database
from db.migration import migrate_db
from db.model import TimeSlot, Appointment, User, Booking
from secret_token.secret_token import get_random_string, hash_pw

log = logging.getLogger('cli')


@hug.cli()
def create_appointments(
        db: PeeweeSession,
        day: hug.types.number,
        month: hug.types.number,
        year: hug.types.number = 2020,
        start_hour: hug.types.number = 8,
        start_min: hug.types.number = 30,
        num_slots: hug.types.number = 13,
        num_appointment_per_slot: hug.types.number = 8,
        slot_duration_min: hug.types.number = 30
):
    with db.atomic():
        for i in range(num_slots):
            ts = TimeSlot.create(
                start_date_time=datetime(year, month, day, start_hour, start_min, tzinfo=None) + timedelta(
                    minutes=i * slot_duration_min),
                length_min=slot_duration_min)
            for _ in range(num_appointment_per_slot):
                Appointment.create(booked=False, time_slot=ts)
            ts.save()


@hug.cli()
def delete_timeslots(
        year: hug.types.number,
        month: hug.types.number,
        day: hug.types.number,
        start_hour: hug.types.number,
        start_min: hug.types.number,
        num_slots: hug.types.number,
        for_real: hug.types.boolean = False
):
    with db.atomic():
        dto = datetime(year, month, day, start_hour, start_min, tzinfo=None)
        tomorrow = datetime(year, month, day, tzinfo=None) + timedelta(days=1)
        ts = TimeSlot.select().where(
            (TimeSlot.start_date_time >= dto) & (TimeSlot.start_date_time < tomorrow)).order_by(
            TimeSlot.start_date_time).limit(num_slots)
        if not for_real:
            log.info(f"I would delete the following time slots - run with --for_real if these are correct")
        else:
            log.info(f"Deleting the following time slots")
        tsids_to_delete = []
        for t in ts:
            tsids_to_delete.append(t.id)
            log.info(f"ID: {t.id} - {t.start_date_time}")
        if not tsids_to_delete:
            log.error("No matching timeslots found! Exiting.")
            sys.exit(1)
        apts = Appointment.select().where(Appointment.time_slot.in_(tsids_to_delete))
        log.info(f"this {'will' if for_real else 'would'} affect the following appointments")
        apts_to_delete = []
        for apt in apts:
            apts_to_delete.append(apt)
            log.info(f"ID: {apt.id} - {apt.time_slot.start_date_time}: {'booked!' if apt.booked else 'free'}")
        if all(not apt.booked for apt in apts_to_delete):
            log.info(f"none of these appointments are booked, so I {'will' if for_real else 'would'} delete them")
            if for_real:
                aq = Appointment.delete().where(Appointment.id.in_([a.id for a in apts_to_delete]))
                tq = TimeSlot.delete().where(TimeSlot.id.in_(tsids_to_delete))
                aq.execute()
                tq.execute()
                log.info("Done!")
        else:
            log.error(f"Some of these appointments are already booked, {'will' if for_real else 'would'} not delete!")


@hug.cli()
def create_initial_appointments():
    create_appointments(27, 3)
    create_appointments(30, 3)
    create_appointments(31, 3)
    create_appointments(1, 4)
    create_appointments(2, 4)
    create_appointments(3, 4)
    create_appointments(6, 4)
    create_appointments(7, 4)
    create_appointments(8, 4)
    create_appointments(9, 4)
    create_appointments(10, 4)


@hug.cli()
def init_db(for_real: hug.types.smart_boolean = False):
    if not for_real:
        print('this will create the database (potentially destroying data), run with --for_real, if you are sure '
              '*and* have a backup')
        sys.exit(1)
    else:
        init_database()


@hug.cli()
def add_user(db: PeeweeSession, username: hug.types.text, role: hug.types.one_of(UserRoles.user_roles()) = UserRoles.USER,
             coupons: hug.types.number = 10):
    with db.atomic():
        name = username.lower()
        salt = get_random_string(2)
        secret_password = get_random_string(12)
        hashed_password = hash_pw(name, salt, secret_password)
        user = User.create(user_name=name, role=role, salt=salt, password=hashed_password, coupons=coupons)
        user.save()
        print(f'{user.user_name}\t{secret_password}')


@hug.cli()
def add_users(filename: hug.types.text, role: hug.types.one_of(['admin', 'doctor']) = 'doctor'):
    with open(filename) as f:
        for line in f:
            add_user(line.strip(), role=role)


@hug.cli()
def run_migrations():
    migrate_db()


@hug.cli()
def get_coupon_state():
    """
    SELECT u.user_name, u.coupons, COUNT(b.id)
    FROM "user" u
    JOIN booking b ON b.booked_by = u.user_name
    GROUP BY u.user_name, u.coupons
    """
    print(f'Username\tTotal Bookings\tNumber of coupons')
    for user in User.select():
        bookings = Booking.select().where(
            user.user_name == Booking.booked_by)
        print(f'{user.user_name}\t{len(bookings)}\t{user.coupons}')


@hug.cli()
def set_coupon_count(db: PeeweeSession, user_name: hug.types.text, value: hug.types.number):
    with db.atomic():
        user = User.get(User.user_name == user_name)
        user.coupons = value
        user.save()


@hug.cli()
def inc_coupon_count(db: PeeweeSession, user_name: hug.types.text, increment: hug.types.number):
    with db.atomic():
        user = User.get(User.user_name == user_name)
        user.coupons += increment
        user.save()


@hug.context_factory()
def create_context(*args, **kwargs):
    return PeeweeContext()
