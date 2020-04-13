import csv
import io
from datetime import datetime
from typing import List, Dict

import hug

from conftest import ADMIN, USER
from db.model import User, TimeSlot, Appointment, Booking


def parse_csv(csv_string: str) -> List[Dict]:
    return list(csv.DictReader(io.StringIO(csv_string), delimiter='\t'))


def test_get_coupon_state(testing_db):
    response_1 = hug.test.cli('get_coupon_state', module='main', collect_output=True)
    out_1 = parse_csv(response_1)
    assert len(out_1) == 2
    admin_1 = next(a for a in out_1 if a['name'] == ADMIN)
    user_1 = next(a for a in out_1 if a['name'] == USER)
    assert int(admin_1['num_bookings']) == 0
    assert int(user_1['num_bookings']) == 0
    assert int(admin_1['coupons']) == 10
    assert int(user_1['coupons']) == 10

    u = User.get(User.user_name == 'user')
    u.coupons += 11
    u.save()

    response_2 = hug.test.cli('get_coupon_state', module='main', collect_output=True)
    out_2 = parse_csv(response_2)
    assert len(out_2) == 2
    admin_2 = next(a for a in out_2 if a['name'] == ADMIN)
    user_2 = next(a for a in out_2 if a['name'] == USER)
    assert int(admin_2['num_bookings']) == 0
    assert int(user_2['num_bookings']) == 0
    assert int(admin_2['coupons']) == 10
    assert int(user_2['coupons']) == 21

    b = Booking.create(
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

    response_3 = hug.test.cli('get_coupon_state', module='main', collect_output=True)
    out_3 = parse_csv(response_3)
    assert len(out_3) == 2
    admin_3 = next(a for a in out_3 if a['name'] == ADMIN)
    user_3 = next(a for a in out_3 if a['name'] == USER)
    assert int(admin_3['num_bookings']) == 0
    assert int(user_3['num_bookings']) == 1
    assert int(admin_3['coupons']) == 10
    assert int(user_3['coupons']) == 21
