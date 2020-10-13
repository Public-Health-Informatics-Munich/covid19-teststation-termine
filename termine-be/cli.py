import csv
import io
import json
import logging
import sys
from datetime import datetime, timedelta

import hug
from peewee import DatabaseError

from access_control.access_control import UserRoles
from db import directives
from db.migration import migrate_db, init_database
from db.model import TimeSlot, Appointment, User, Booking, Migration, FrontendConfig
from secret_token.secret_token import get_random_string, hash_pw

log = logging.getLogger('cli')


@hug.default_output_format(apply_globally=False, cli=True, http=False)
def cli_output(data):
    result = io.StringIO()
    writer = csv.DictWriter(result, fieldnames=data[0].keys(), delimiter='\t')
    writer.writeheader()
    writer.writerows(data)
    return result.getvalue().encode('utf8')


@hug.cli()
def create_appointments(
        db: directives.PeeweeSession,
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
        db: directives.PeeweeSession,
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


def _add_one_user(db: directives.PeeweeSession, username: hug.types.text, password: hug.types.text = None,
                  role: hug.types.one_of(UserRoles.user_roles()) = UserRoles.USER,
                  coupons: hug.types.number = 10):
    with db.atomic():
        name = username.lower()
        salt = get_random_string(2)
        secret_password = password or get_random_string(12)
        hashed_password = hash_pw(name, salt, secret_password)
        user = User.create(user_name=name, role=role, salt=salt, password=hashed_password, coupons=coupons)
        user.save()
        return {"name": user.user_name, "password": secret_password}


@hug.cli()
def add_user(db: directives.PeeweeSession, username: hug.types.text, password: hug.types.text = None,
             role: hug.types.one_of(UserRoles.user_roles()) = UserRoles.USER,
             coupons: hug.types.number = 10):
    return [_add_one_user(db, username, password, role, coupons)]


@hug.cli()
def add_users(db: directives.PeeweeSession, filename: hug.types.text,
              role: hug.types.one_of(UserRoles.user_roles()) = UserRoles.USER):
    with open(filename) as f:
        return [_add_one_user(db, line.strip(), role=role) for line in f]


@hug.cli()
def change_user_pw(db: directives.PeeweeSession, username: hug.types.text, password: hug.types.text, for_real: hug.types.smart_boolean = False):
    if not for_real:
        print(f"this would change {username}'s pw to {password}. Run with --for_real if you're sure.")
        sys.exit(1)
    with db.atomic():
        name = username.lower()
        salt = get_random_string(2)
        secret_password = password
        hashed_password = hash_pw(name, salt, secret_password)
        user = User.get(User.user_name == username)
        user.salt = salt
        user.password = hashed_password
        user.save()
        print(f"{user.user_name}'s pw successfully changed.")


@hug.cli()
def init_db(db: directives.PeeweeSession, for_real: hug.types.smart_boolean = False):
    if not for_real:
        print('this will create the database (potentially destroying data), run with --for_real, if you are sure '
              '*and* have a backup')
        sys.exit(1)
    else:
        with db.atomic():
            try:
                migration = Migration.get()
                print(f'Migration level is already set to version {migration.version} - implying the db has already been '
                      f'initialized. Run command `run_migrations` instead.')
                sys.exit(1)
            except DatabaseError:
                init_database()


@hug.cli()
def run_migrations(for_real: hug.types.smart_boolean = False):
    if not for_real:
        print('this will migrate the database (potentially destroying data), run with --for_real, if you are sure '
              '*and* have a backup')
        sys.exit(1)
    else:
        migrate_db()


@hug.cli()
def get_coupon_state():
    """
    SELECT u.user_name, u.coupons, COUNT(b.id)
    FROM "user" u
    JOIN booking b ON b.booked_by = u.user_name
    GROUP BY u.user_name, u.coupons
    """
    ret = []
    for user in User.select():
        bookings = Booking.select().where(
            user.user_name == Booking.booked_by)
        ret.append({
            "name": user.user_name,
            "num_bookings": len(bookings),
            "coupons": user.coupons
        })
    return ret


@hug.cli()
def set_coupon_count(db: directives.PeeweeSession, user_name: hug.types.text, value: hug.types.number):
    with db.atomic():
        user = User.get(User.user_name == user_name)
        user.coupons = value
        user.save()


@hug.cli()
def inc_coupon_count(db: directives.PeeweeSession, user_name: hug.types.text, increment: hug.types.number):
    with db.atomic():
        user = User.get(User.user_name == user_name)
        user.coupons += increment
        user.save()


@hug.cli()
def cancel_booking(db: directives.PeeweeSession, secret: hug.types.text, start_date_time: hug.types.text, for_real: hug.types.smart_boolean = False):
    with db.atomic():
        sdt = datetime.fromisoformat(start_date_time).replace(tzinfo=None)
        timeslot = TimeSlot.get(TimeSlot.start_date_time == sdt)
        booking = Booking.select(Booking).join(Appointment).where(
            (Booking.secret == secret) &
            (Appointment.time_slot == timeslot)).get()

        if not for_real:
            print(f"This would delete the booking with id '{booking.id}' and secret '{booking.secret}'. Run with "
                  f"--for_real if you are sure.")
            sys.exit(1)
        else:
            print(f"Deleting the booking with id '{booking.id}' and secret '{booking.secret}'.")
            booking.appointment.booked = False
            booking.appointment.save()
            q = Booking.delete().where(Booking.id == booking.id)
            q.execute()
            print("Done.")


@hug.cli()
def set_frontend_config(db: directives.PeeweeSession, instance_name: hug.types.text, long_instance_name: hug.types.text,
                        contact_info_bookings: hug.types.text, contact_info_appointments: hug.types.text = None,
                        form_fields: hug.types.text = "base,address,dayOfBirth,reason",
                        for_real: hug.types.smart_boolean = False):
    with db.atomic():
        if "@" in contact_info_bookings:
            bookings_contact = f"<a href=\"mailto:{contact_info_bookings}\">{contact_info_bookings}</a>"
        else:
            bookings_contact = contact_info_bookings

        if not contact_info_appointments:
            appointments_contact = bookings_contact
        else:
            if "@" in contact_info_appointments:
                appointments_contact = f"<a href=\"mailto:{contact_info_appointments}\">{contact_info_appointments}</a>"
            else:
                appointments_contact = contact_info_appointments

        template = {
            "instanceName": f"{instance_name}",
            "longInstanceName": f"{long_instance_name}",
            "contactInfoCoupons": f"<span class=\"hintLabel\">Um mehr Termine vergeben zu können wenden Sie sich an "
                                  f"{bookings_contact}</span>",
            "contactInfoAppointment": f"<span class=\"hintLabel\">Kontaktieren Sie {appointments_contact}</span>",
            "formFields": form_fields.split(","),
        }

        if not for_real:
            print(f"This would update the config with '{json.dumps(template, indent=2)}'. Run with --for_real if you "
                  f"are sure.")
            sys.exit(1)
        else:
            print(f"Updating the config with '{json.dumps(template, indent=2)}'.")
            try:
                config = FrontendConfig.get()
                config.config = template
            except FrontendConfig.DoesNotExist:
                config = FrontendConfig.create(config=template)

            config.save()
            print("Done.")
