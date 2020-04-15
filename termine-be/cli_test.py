import csv
import io
import pytest
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

import hug

from conftest import ADMIN, USER
from db.model import User, TimeSlot, Appointment, Booking
from peewee import DoesNotExist

def parse_csv(csv_string: str) -> List[Dict]:
    return list(csv.DictReader(io.StringIO(csv_string), delimiter='\t'))




def test_get_coupon_state(testing_db):
    def get_admin_and_user_data() -> Tuple[Dict, Dict]:
        response = hug.test.cli('get_coupon_state', module='main', collect_output=True)
        out = parse_csv(response)
        a: Dict = next(a for a in out if a['name'] == ADMIN)
        u: Dict = next(a for a in out if a['name'] == USER)
        assert len(out) == 2
        return a, u
    admin_1, user_1 = get_admin_and_user_data()
    assert int(admin_1['num_bookings']) == 0
    assert int(user_1['num_bookings']) == 0
    assert int(admin_1['coupons']) == 10
    assert int(user_1['coupons']) == 10

    User.update({User.coupons: User.coupons + 11}).where(User.user_name == USER).execute()

    admin_2, user_2 = get_admin_and_user_data()
    assert int(admin_2['num_bookings']) == 0
    assert int(user_2['num_bookings']) == 0
    assert int(admin_2['coupons']) == 10
    assert int(user_2['coupons']) == 21

    Booking.create(
        surname="Mustermann",
        first_name="Marianne",
        phone="0123456789",
        office="MusterOffice",
        secret="SECRET",
        booked_by=USER,
        booked_at=datetime.now(),
        appointment=(
            Appointment.create(
                booked=True,
                time_slot=(
                    TimeSlot.create(
                        start_date_time=datetime.now(),
                        length_min=15)
                )
            )
        ),
    )
    User.update({User.coupons: User.coupons - 1}).where(User.user_name == USER).execute()

    admin_3, user_3 = get_admin_and_user_data()
    assert int(admin_3['num_bookings']) == 0
    assert int(user_3['num_bookings']) == 1
    assert int(admin_3['coupons']) == 10
    assert int(user_3['coupons']) == 20

def test_cancel_booking(testing_db):
    now = datetime.now()
    duration = 15

    def get_booking_data(secret):
        return {
            "surname": "Mustermann",
            "first_name": "Marianne",
            "phone": "0123456789",
            "office": "MusterOffice",
            "secret": secret,
            "booked_by": USER,
            "booked_at": now
        }

    slot1 = TimeSlot.create(start_date_time=now, length_min=duration)
    slot2 = TimeSlot.create(start_date_time=now + timedelta(minutes=duration),
                            length_min=duration)

    appointment1 = Appointment.create(booked=False, time_slot=slot1)
    appointment2 = Appointment.create(booked=False, time_slot=slot1)
    appointment3 = Appointment.create(booked=False, time_slot=slot2)
    appointment4 = Appointment.create(booked=False, time_slot=slot2)

    appointment5 = Appointment.create(booked=True, time_slot=slot1)
    appointment6 = Appointment.create(booked=True, time_slot=slot1)
    appointment7 = Appointment.create(booked=True, time_slot=slot2)
    appointment8 = Appointment.create(booked=True, time_slot=slot2)

    booking1 = Booking.create(**get_booking_data("SECRET1"), appointment=appointment5)
    booking2 = Booking.create(**get_booking_data("SECRET2"), appointment=appointment6)
    booking3 = Booking.create(**get_booking_data("SECRET3"), appointment=appointment7)
    booking4 = Booking.create(**get_booking_data("SECRET4"), appointment=appointment8)

    not_cancel_booking = booking1
    cancel_booking = booking3

    fail_cancel_args = {
        "secret": not_cancel_booking.secret,
        "start_date_time": cancel_booking.appointment.time_slot.start_date_time,
    }

    assert Booking.select().count() == 4
    assert TimeSlot.select().count() == 2
    assert Appointment.select().count() == 8
    assert Appointment.get_by_id(cancel_booking.appointment.id).booked == True

    hug.test.cli('cancel_booking', module='main', **fail_cancel_args)

    assert Booking.select().count() == 4
    assert TimeSlot.select().count() == 2
    assert Appointment.select().count() == 8
    assert Appointment.get_by_id(cancel_booking.appointment.id).booked == True

    hug.test.cli('cancel_booking', module='main', **fail_cancel_args, for_real=True)

    assert Booking.select().count() == 4
    assert TimeSlot.select().count() == 2
    assert Appointment.select().count() == 8
    assert Appointment.get_by_id(cancel_booking.appointment.id).booked == True

    success_cancel_args = {
        "secret": cancel_booking.secret,
        "start_date_time": cancel_booking.appointment.time_slot.start_date_time,
    }

    hug.test.cli('cancel_booking', module='main', **success_cancel_args, for_real=True)

    assert Booking.select().count() == 3
    assert TimeSlot.select().count() == 2
    assert Appointment.select().count() == 8
    assert Appointment.get_by_id(cancel_booking.appointment.id).booked == False
